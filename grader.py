import os
from hs_gimme.account_settings_manager import get_account_settings
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_tree_blenders_creation.eeo_analysis.eeo_analysis_utils import ApplicationGrader
from hs_application_service_client import get_application_service_client

environment = 'production'
os.environ['HIREDSCORE_ENVIRONMENT'] = environment
account_id = 'wd_sales_hs_gms02'
app_id = "WSBR-00545_WSBCAND-3592"
req_id = "WSBR-00545"
app_collection = 'application'

app_service = get_application_service_client(env=environment, call_external_services=True, strict_errors=False)
grader = ApplicationGrader(account_id, environment, use_grading_service=False)

mongo = get_mongo_client_db(environment, account_id)

app = mongo[app_collection].find_one(app_id)
req = mongo.req.find_one(req_id)
account = get_account_settings(account_id)

papp = app#app_service.process_application(app, req, account=account)
brain_result = grader.calculate_grade(papp, req, account)

print(len(brain_result))
print()