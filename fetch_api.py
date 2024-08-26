from collections import Counter
import os
from hs_fetch.fast_fetch.fast_fetch_filtering_queries_base import TitlesSimilarityFeaturesFilter
from hs_gimme.logging_service.logging_service import LoggingService
from hs_gimme.logging_service.problems_only_logging_service import ProblemsOnlyLoggingService
from hs_recommendations_api.fast_fetch.fast_fetch_api import FastFetchAPI
from hs_fetch.fast_fetch.fast_fetch_interactive_input import get_interactive_input_from_put_request
from hs_tree_blenders_creation.fast_fetch_evaluation.evaluate_dataset import get_all_filters
from hs_fetch.fast_fetch.fast_fetch_filtering_query_builder import SpecificTalentIdsQueryFilter, \
    CurrentSeniorityQueryFilter, ProfessionsQueryFilter, DetailedProfessionsQueryFilter, \
    get_talent_fast_fetch_query_builder, get_employee_fast_fetch_query_builder

#
# ACCOUNT = 'sofia'
# PAIRS =[('SBY156649', '4251c037-ec23-4b13-9a9d-de01dcfbcf75'),
#         ('SBY38361', '52e5ea2c-2dda-4943-94b9-0ffc140136d0')]
ENV = 'production'
os.environ['HIREDSCORE_ENVIRONMENT'] = ENV
#os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'

fetch_api = FastFetchAPI(ProblemsOnlyLoggingService(), ENV)

req_id = 'ADV24008653'
account_id = 'antalya'

kwargs = {'account_id': {'value': account_id},
          'req_id': {'value': req_id},
          "fetch_mode": {"value": "talent_fetch"},
      #    "external_pool_id": {"value": "randstad_preprod_de"},
      #    "is_contingent":  {"value": True},
        #  "external_pool_id": {"value": "randstad_preprod_de"},
          # "include_internals": {"value": False},
          # "include_externals": {"value": True},
           'size': {'value': 20, 'is_mandatory': True},
          # "allow_already_applied_req": {"value": True},
          # "allow_candidates_with_offer": {"value": True},
        #  'max_distance': {'value': 25, 'is_mandatory': True},
        #  'fetch_mode': {'value': 'talent_fetch', 'is_mandatory': True},
        #  'include_agency': {'value': "exclude", 'is_mandatory': True},
        #  'include_externals': {'value': "exclude", 'is_mandatory': True},
          'specific_talent_ids': {'value': ['957aa71d-d11d-439a-a886-c63889b0e763'], 'is_mandatory': True},
        #  'consider_past_applied_locations_as_candidate_locations': {'value': False, 'is_mandatory': True},
        #  'max_distance': {'value': 25000, 'is_mandatory': True},
          #'filters_to_remove': {'value': ['IndustryYearsQueryFilter']},
        #  'min_years_of_industry_experience': {'value': 5},
        #   'filters_to_use': {'value': ['CandidateRecordQueryFilter',
        #                                'SpecificTalentIdsQueryFilter',
        #                                'CountryQueryFilter'
        #                      ]}
        #  'filters_to_use': {'value': ['CandidateRecordQueryFilter']}
          }

if False:
    all_filters = get_talent_fast_fetch_query_builder(True).filters

    results = {}

    for fil in all_filters:

        fil_name = fil.__class__.__name__
        kwargs['filters_to_use'] = {'value': ['CandidateRecordQueryFilter', fil_name]}

        interactive_input = get_interactive_input_from_put_request(kwargs, account_id, req_id)
        recommendations = fetch_api.do_fast_fetch(interactive_input)

        results[fil_name] = recommendations['total_count']

    print()
    print()
    for k, v in sorted(results.items(), key=lambda x: x[1]):
        print(k, v)

else:
    interactive_input = get_interactive_input_from_put_request(kwargs, account_id, req_id)
    recommendations = fetch_api.do_fast_fetch(interactive_input)
    print()
    print(recommendations['total_count'])

