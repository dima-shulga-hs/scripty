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

account_id = 'exeter'
req_id = 'EQXJR-144193'
ENV = 'production'
os.environ['HIREDSCORE_ENVIRONMENT'] = ENV
#os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'

fetch_api = FastFetchAPI(
    ProblemsOnlyLoggingService(), ENV,
)

kwargs = {
    # 'diversity_groups_configuration': {'value': {"race": [{"key": "White", "is_underepresented": false, "is_undisclosed": false}, {"key": "Asian", "is_underepresented": true, "is_undisclosed": false}, {"key": "Black or African American", "is_underepresented": true, "is_undisclosed": false}, {"key": "Hispanic or Latino", "is_underepresented": true, "is_undisclosed": false}, {"key": "American Indian or Alaska Native", "is_underepresented": true, "is_undisclosed": false}, {"key": "Native Hawaiian or Other Pacific Islander", "is_underepresented": true, "is_undisclosed": false}, {"key": "Two or More Races", "is_underepresented": true, "is_undisclosed": false}, {"key": "decline to identify", "is_underepresented": false, "is_undisclosed": true}, {"key": "__none__", "is_underepresented": false, "is_undisclosed": true}], "gender": [{"key": "Male", "is_underepresented": false, "is_undisclosed": false}, {"key": "Female", "is_underepresented": true, "is_undisclosed": false}, {"key": "decline to identify", "is_underepresented": False, "is_undisclosed": True},
    # 'consider_past_applied_locations_as_candidate_locations': {'value': True},
    # 'diversity_groups_to_db_fields_mapping': {'value': '{"race": "local_race"}'},
    # 'filter_by_fields': {'value': []},
   #  'for_hiring_potential_data': {'value': True, 'is_mandatory': True},
     'max_apply_since_days': {'value': 30},
    # 'max_distance': {'value': 50},
    # 'min_degree_level': {'value': 'associates'},
    # 'min_years_of_industry_experience': {'value': 0.0},
    # 'min_years_of_management_experience': {'value': 5.0},
  #   'min_years_of_relevant_experience': {'value': 4.0},
    # 'preferred_skills': {'value': ['security']},
    # 'title': {'value': 'Senior Manager, Physical Security Operations'}
}
interactive_input = get_interactive_input_from_put_request(kwargs, account_id, req_id)
recommendations = fetch_api.do_fast_fetch(interactive_input)
print()
print(recommendations['total_count'])