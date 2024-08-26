from mock.mock import MagicMock
from hs_fetch.fast_fetch.ioc_resolver import IocResolver
from hs_fetch.fast_fetch.recipes.base_recipe import BaseFetchRecipe
from hs_gimme.logging_service.logging_service import LoggingService


def value(value2):
    return value2


def return_value(value=3):
    return value


recipe = {'applied_recipes': 'test'}
BaseFetchRecipe().apply_recipe(base_recipe=recipe,
                               account_id='test',
                               req_id='test',
                               interactive_input={},
                               fetch_config=None,
                               environment='test',
                               es_tag='test')

factory = IocResolver(logging_service=LoggingService(), config=recipe, test_mode=True)
print(factory.resolve('grader'))