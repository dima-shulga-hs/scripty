from hs_fetch.data_access.fast_fetch.fast_fetch_batch_indexing import index_all_data
from hs_gimme.logging_service.problems_only_logging_service import ProblemsOnlyLoggingService

x = index_all_data(ProblemsOnlyLoggingService(), 'randstad_preprod_de', 'production_de')