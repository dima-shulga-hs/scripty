from collections import Counter
import os
from hs_fetch.fast_fetch.fast_fetch_filtering_queries_base import TitlesSimilarityFeaturesFilter
from hs_fetch.fast_fetch.reqs_fetch.fast_fetch_reqs_search_input import get_recommended_reqs_input
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_gimme.logging_service.logging_service import LoggingService
from hs_gimme.logging_service.problems_only_logging_service import ProblemsOnlyLoggingService
from hs_recommendations_api.fast_fetch.fast_fetch_api import FastFetchAPI
from hs_fetch.fast_fetch.fast_fetch_interactive_input import get_interactive_input_from_put_request
from hs_tree_blenders_creation.fast_fetch_evaluation.evaluate_dataset import get_all_filters
from hs_fetch.fast_fetch.fast_fetch_filtering_query_builder import SpecificTalentIdsQueryFilter, \
    CurrentSeniorityQueryFilter, ProfessionsQueryFilter, DetailedProfessionsQueryFilter

#
# ACCOUNT = 'sofia'
# PAIRS =[('SBY156649', '4251c037-ec23-4b13-9a9d-de01dcfbcf75'),
#         ('SBY38361', '52e5ea2c-2dda-4943-94b9-0ffc140136d0')]
account_id = 'berlin'
ENV = 'production_de'

os.environ['HIREDSCORE_ENVIRONMENT'] = ENV
os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'


fetch_api = FastFetchAPI(
    ProblemsOnlyLoggingService(), ENV,
)



kwargs = {
   # 'account_id': account_id,
    'talent_ids': ['2336f58f-d3e3-43f8-aa66-2560763e1bc3'],
    # 'extended_coverage': False,
    # 'is_redeployment': False,
   # 'max_recommendations': 20,
   # 'max_distance': 5000000000,
  #  'compute_insights': True,
     'specific_req_ids': ['BCHbbe8840e-2af4-4ef0-86ec-f66ccdde348c',
'BCHe1071707-ec82-47dc-a6c0-024f158fd2d8', 'BCH43074708-567c-4022-a65c-46d86033e16e',
    'BCH51a8a0cb-d050-4249-9c1a-37e717d8fcc5'],
    # 'filters_to_use': ['SpecificReqIdsQueryFilter']
}

recommended_reqs_input = get_recommended_reqs_input(kwargs, account_id)
res = fetch_api.recommended_reqs(recommended_reqs_input)

print()
print('RESULTS:')

for x in res['candidates_outputs']:
    print(x['candidate_id'], len(x['recommended_reqs']))
    for r in x['recommended_reqs']:
        print(r['req_id'])
    print()


