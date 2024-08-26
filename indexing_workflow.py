from hs_gimme.logging_service.logging_service import LoggingService
from hs_fetch.utils.fetch_accounts_config_objects import get_fetch_config
from datetime import datetime
from hs_tree_blenders_creation.batch_runners.batch_runs_data_layer import get_fetch_data_layer
from hs_fetch.data_access.potential_candidate_loading.loader_strategies import DataLayerLoaderStrategy
from hs_fetch.workflows.factories.past_candidates_workflows_factory import PastCandidatesWorkflowsFactory

workflow_factory = PastCandidatesWorkflowsFactory(LoggingService(), 'production_brain', 'moscow')


ACCOUNT = 'moscow'
ENV = 'production'
TALENT_ID = 'c99bd0e8-ecd7-46a1-b435-688a6e3890aa'
account_config = get_fetch_config(ACCOUNT, country=None)

dl = get_fetch_data_layer(
        ACCOUNT,
        environment=ENV,
    )


indexing_workflow = workflow_factory.create_index_candidates_for_fast_fetch_workflow(
                account_config.get_max_days_since_apply_for_load(),
                datetime.today(), '',
                logging_service=LoggingService(),
                loader_strategy=DataLayerLoaderStrategy(dl))


res = indexing_workflow.get_candidate_data([TALENT_ID], req=None)
print(sum([bool(r) for r in res]))


x = get_recommendations_api_client()