from hs_gimme.account_settings_manager import get_account_settings
from hs_gimme.address_info_service.address_info_service import get_address_info_service
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db
from hs_gimme.google_translate_api.google_translate_api import GoogleTranslateApi, get_default_mongo_db_for_caching
from hs_gimme.logging_service.logging_service import LoggingService
from hs_gimme.organization.company_retrieval import CompanyRetrieval
from hs_req_processor.req_enricher.req_enriching_workflow import ReqEnrichmentWorkflow
from hs_req_processor.req_parser.req_parsing_workflow import ReqParsingWorkflow
from hs_req_processor.req_processor import ReqProcessor


logging_service = LoggingService()


def _get_req_processor(account_id, account, environment):
    address_info_service = get_address_info_service(environment, account_id, logging_service)

    translate_api = GoogleTranslateApi(get_default_mongo_db_for_caching(environment, account_id), logging_service)
    company_retrieval = CompanyRetrieval(
        mongo_client_db=None,
        account_settings=account,
        logging_service=logging_service
    )

    req_parsing_workflow = ReqParsingWorkflow(logging_service, translate_api)
    req_enrichment_workflow = ReqEnrichmentWorkflow(
        logging_service, address_info_service, company_retrieval
    )

    return ReqProcessor(req_parsing_workflow, req_enrichment_workflow, logging_service)


account_id = 'rotterdam_preprod'
environment = 'production_de'
req_id = 'RSP101725458556428998'

mongo = get_mongo_client_db(environment, account_id)
req = mongo.req.find_one(req_id)
account = get_account_settings(account_id)
req_processor = _get_req_processor(account_id, account, environment)

req_processor.process_req(req, account)