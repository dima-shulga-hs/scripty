from datetime import datetime
import pandas as pd
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_gimme.application_status_history_classifier.machine_learning_status_classifier import \
    get_machine_learning_status_classifier
from collections import defaultdict
from datetime import timedelta
import copy
import numpy as np

ENV = 'production'
ACCOUNT = 'dallas'
REFERENCE_DATE = datetime(2023, 11, 1)
APP_FIELDS = ['req_id', 'ats_application', 'is_internal', 'grade_data.explainable_score_data']
REQ_FIELDS = ['job_department',
              'country',
              'external_job_band',
              'external_recruiters',
              'top_category',
              'sub_category',
              'job_education',
              'seniority_level',
              'min_years_of_relevant_experience',
              'max_years_of_relevant_experience',
              'max_salary',
              'job_type',
              'is_visa_required',
              'is_remote_location',
              'external_status',
              'industry',
              'open_date',
              'past_candidates_distribution_date',
              'is_recent_grad',
              'is_intern',
              '_created_at',
              'date_posted',
              'job_create_date',
              'last_edit_date',
              'status_history',
              'recruiter_roles',
              'recruiting_type']


def get_data_for_req(req, req_to_apps):
    req_apps = req_to_apps[req['_id']]
    req_dates = {s: v[0] for s, v in req['status_history'].items()}
    if req_apps:
        req_dates['First apply'] = min(a['ats_application']['date_applied'] for a in req_apps)
        for status in ['interview', 'offer']:
            req_dates['First ' + status] = min(a['phases_dates'].get(status, datetime.now()) for a in req_apps)

        try:
            req_dates['First Interview Worthy Apply'] = min(
                a['ats_application']['date_applied'] for a in req_apps if a['max_status'] >= 2)
            req_dates['First Interview Worthy Interview'] = min(
                a['phases_dates']['interview'] for a in req_apps if a['max_status'] >= 2)

            req_dates['First Offer Worthy Apply'] = min(
                a['ats_application']['date_applied'] for a in req_apps if a['max_status'] >= 3)
            req_dates['First Offer Worthy Interview'] = min(
                a['phases_dates']['interview'] for a in req_apps if a['max_status'] >= 3)
        except:
            pass

    return req_dates


def get_app_waiting_time(app):
    try:
        first_response = min(d for k, d in app['phases_dates'].items() if k in {'rejected', 'interview'})
        return (first_response - app['ats_application']['date_applied']).days
    except:
        raise


def simulate_best(req_apps):
    new_apps = copy.deepcopy(req_apps)

    offer_days = None

    for app in new_apps:
        if 'offer' in app['phases_dates'] and 'interview' in app['phases_dates']:
            offer_days = (app['phases_dates']['offer'] - app['phases_dates']['interview']).days
        elif 'offer' in app['phases_dates'] and 'interview' not in app['phases_dates']:
            raise
            offer_days = (app['phases_dates']['offer'] - app['ats_application']['date_applied']).days
        elif 'interview' not in app['phases_dates'] and 'offer' not in app['phases_dates']:
            app['phases_dates']['rejected'] = app['ats_application']['date_applied'] + timedelta(days=1)
        elif 'offer' not in app['phases_dates']:
            app['phases_dates']['interview'] = app['ats_application']['date_applied'] + timedelta(days=1)
            app['phases_dates']['rejected'] = app['ats_application']['date_applied'] + timedelta(days=2)
        else:
            app['phases_dates']['interview'] = app['ats_application']['date_applied'] + timedelta(days=1)
            app['phases_dates']['offer'] = app['ats_application']['date_applied'] + timedelta(days=offer_days)
    return new_apps


def simulate_req(req, simulated_req_apps, print_pipes=False):
    date = req['status_history']['Post'][0]
    has_offer = False
    days = []
    while not has_offer:
        day_actions = 0
        if print_pipes:
            print(date.date(), end=' ')
        for app in simulated_req_apps:
            if app['ats_application']['date_applied'].date() == date.date():
                if print_pipes:
                    print('\033[1m\033[33mA\033[0m', end=' ')
            elif app['phases_dates'].get('rejected', datetime.now()).date() == date.date():
                if print_pipes:
                    print('\033[1m\033[31mR\033[0m', end=' ')
                day_actions += 1
            elif app['phases_dates'].get('interview', datetime.now()).date() == date.date():
                if print_pipes:
                    print('\033[1m\033[34mV\033[0m', end=' ')
                day_actions += 1
            elif app['phases_dates'].get('offer', datetime.now()).date() == date.date():
                has_offer = True
                day_actions += 1
                if print_pipes:
                    print('\033[1m\033[32mO\033[0m', end=' ')
            else:
                if print_pipes:
                    print('|', end=' ')

        if print_pipes:
            print()

        date = date + timedelta(days=1)
        days.append(day_actions)
        if date.date() == req['status_history']['Filled'][0].date():
            break

    return {
        'post_to_offer': (date - req['status_history']['Post'][0]).days,
        'waiting_days': [get_app_waiting_time(a) for a in simulated_req_apps],
        'num_of_actions': days,
    }


def main():
    mongo = get_mongo_client_db(ENV, ACCOUNT)
    status_cls = get_machine_learning_status_classifier(ENV, ACCOUNT)
    reqs = list(mongo.req.find({'_created_at': {'$gt': REFERENCE_DATE}, 'date_posted':
        {'$gt': REFERENCE_DATE}, 'external_status': 'Filled'
                                }, REQ_FIELDS))
    print('Num of reqs:', len(reqs))

    for r in reqs:
        r['time_to_fill'] = (r['status_history']['Filled'][0] - r['status_history']['Post'][0]).days

    req_ids = [r['_id'] for r in reqs]

    apps = list(mongo.application.find({'req_id': {'$in': req_ids}}, APP_FIELDS))
    print('Num of apps:', len(apps))

    req_to_apps = defaultdict(list)
    for app in apps:
        app['phases_dates'] = status_cls.get_phases_reach_dates(app)
        app['max_status'] = status_cls.get_max_status(app)
        if 'offer' in app['phases_dates'] and 'interview' not in app['phases_dates']:
            pass
        else:
            req_to_apps[app['req_id']].append(app)

    user_to_reqs = defaultdict(list)
    for req in reqs:
        user_to_reqs[req['recruiter_roles']['recruiter']].append(req)

    data = []
    for user, user_reqs in user_to_reqs.items():

        orig_vals = []
        best_vals = []

        for req in user_reqs:
            req_apps = req_to_apps[req['_id']]
            orig_req_vals = simulate_req(req, req_apps)

            simulated_req_apps = simulate_best(req_apps)
            best_req_vals = simulate_req(req, simulated_req_apps)

            orig_vals.append(orig_req_vals)
            best_vals.append(best_req_vals)

            orig_post_to_offer = [v['post_to_offer'] for v in orig_vals]
            best_post_to_offer = [v['post_to_offer'] for v in best_vals]

        d = {
            'user_id': user,
            'num_of_reqs': len(user_reqs),
            'original_post_to_ofer_mean': np.mean(orig_post_to_offer),
            'original_post_to_ofer_max': np.max(orig_post_to_offer),
            'best_post_to_ofer_mean': np.mean(best_post_to_offer),
            'best_post_to_ofer_max': np.max(best_post_to_offer),
        }

        data.append(d)

    df = pd.DataFrame(data)

    print('Done')


if __name__ == '__main__':
    main()
