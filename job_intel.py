import os
from hs_recommendations_api.job_intel.job_intel_api import get_job_intel_data
from hs_recommendations_api.job_intel.job_intel_evaluation_utils import get_all_measures_data_input_items, \
    get_client_test_phases

account_id = 'exeter'
req_id = 'EQXJR-144193'
ENV = 'production'
os.environ['HIREDSCORE_ENVIRONMENT'] = ENV

input_items = get_all_measures_data_input_items(get_client_test_phases(account_id, ENV))
input_items = get_all_measures_data_input_items(input_items)
data = get_job_intel_data(account_id, ENV, req_id, input_items)

print(data)