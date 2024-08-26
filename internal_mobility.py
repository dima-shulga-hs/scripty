from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_gimme.logging_service.logging_service import LoggingService
from hs_recommendations_api_client.fetch_match_utils import FetchMatchUtils

ACCOUNT = 'jaipur'
ENV = 'production'


def main():
    fetch = FetchMatchUtils(ACCOUNT, ENV, logging_service=LoggingService())

    mongo = get_mongo_client_db(ENV, ACCOUNT)

    employees = list(mongo.employee.find({'samurai_json.contact_info.postal_address.country_code': {'$ne': None}}).limit(5))

    talent_ids_to_talent_dict = {e['current_talent_id']: e['samurai_json'] for e in employees}
    fetch.match_positions(talent_ids_to_talent_dict,
                          filter_countries=[],
                          minimum_req_posted_date=None,
                          exclude_req_phases=['hire', 'offer'],
                          req_statuses=['Open', 'open'],
                          req_query_additional={},
                          req_projection={},
                          min_fetch_grade=0.8,
                          max_fetch_rank=20)


if __name__ == '__main__':
    main()
