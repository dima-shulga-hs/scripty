from hs_fetch.utils.is_for_fetch_decider import IsForFetchDecider
from hs_fetch.workflows.dependencies.fetch_run_by_stage_decider import FetchRunByStageDecider
from hs_fetch.workflows.dependencies.target_req_validators.active_req_validator import ActiveReqValidator
from hs_fetch.workflows.dependencies.target_req_validators.basic_data_req_validator import BasicDataReqValidator
from hs_fetch.workflows.dependencies.target_req_validators.single_execution_validator import SingleExecutionValidator
from hs_gimme.constants.objects.account_settings import PastCandidates
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_gimme.hs_utils.dict_manipulations.dict_factories import remove_nones_from_dict
from hs_gimme.logging_service.logging_service import LoggingService

fetch_run_by_stage_decider = FetchRunByStageDecider('guatemala', LoggingService(),
                                                            ignore_already_ran_stages=True)
custom_validators = remove_nones_from_dict({
    'only_active_reqs': ActiveReqValidator(IsForFetchDecider(), ['Frozen', 'Open']),
    'req_basic_data': BasicDataReqValidator(),
    'only_licensed_recruiters_in_recruiter_role': None,
    'single_run_validator': SingleExecutionValidator(fetch_run_by_stage_decider),
})

mongo = get_mongo_client_db('production', 'guatemala')
req = mongo.req.find_one('DMNR01280')

for v, f in custom_validators.items():
    print(v, f.validate_req_for_fetch(req))
pass