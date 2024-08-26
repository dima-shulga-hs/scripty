from fetch.hs_fetch.fast_fetch.fast_fetch_candidate_transformers import CandidateIndustryYearsTransformer
from hs_gimme.db_facade.db_facade_factory import get_mongo_client_db

mongo = get_mongo_client_db('production', 'antalya')


cand = mongo.application.find_one({'current_talent_id': '65968293-aa54-4364-b8b9-48243183dd48'})

tr = CandidateIndustryYearsTransformer()

tr.transform({}, cand, {})