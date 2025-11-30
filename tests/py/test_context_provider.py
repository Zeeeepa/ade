import pytest
from mat3ra.ade import ContextProvider
from mat3ra.esse.models.context_provider import Name
from mat3ra.utils import assertion

CONTEXT_PROVIDER_DEFAULT_FIELDS = {
    "domain": None,
    "entityName": None,
    "data": None,
    "extraData": None,
    "isEdited": None,
    "context": None,
}

CONTEXT_PROVIDER_MINIMAL_CONFIG = {
    "name": Name.KGridFormDataManager,
}

CONTEXT_PROVIDER_FULL_CONFIG = {
    "name": Name.KGridFormDataManager,
    "domain": "test_domain",
    "entityName": "subworkflow",
    "data": {"key": "value"},
    "extraData": {"extraKey": "extraValue"},
    "isEdited": True,
    "context": {"contextKey": "contextValue"},
}

CONTEXT_PROVIDER_WITH_DEFAULT_DATA = {
    "name": Name.KPathFormDataManager,
    "data": {"default": "value"},
    "isEdited": False,
    "extraData": {"extra": "data"},
}

EXTERNAL_CONTEXT_OVERRIDE = {
    "KPathFormDataManager": {"override": "value"},
    "isKPathFormDataManagerEdited": True,
    "KPathFormDataManagerExtraData": {"extra_override": "data"},
}

EXPECTED_YIELD_DATA_WITH_EXTERNAL = {
    "KPathFormDataManager": {"override": "value"},
    "isKPathFormDataManagerEdited": True,
    "KPathFormDataManagerExtraData": {"extra_override": "data"},
}

CONTEXT_PROVIDER_WITH_STORED_CONTEXT = {
    "name": Name.KPathFormDataManager,
    "data": {"default": "value"},
    "isEdited": False,
    "context": {
        "KPathFormDataManager": {"stored": "value"},
        "isKPathFormDataManagerEdited": True,
    },
}

EXPECTED_YIELD_DATA_WITH_STORED = {
    "KPathFormDataManager": {"stored": "value"},
    "isKPathFormDataManagerEdited": True,
}


def test_context_provider_creation():
    config = CONTEXT_PROVIDER_MINIMAL_CONFIG
    provider = ContextProvider(**config)
    expected = {
        **config,
        **CONTEXT_PROVIDER_DEFAULT_FIELDS,
    }
    assertion.assert_deep_almost_equal(expected, provider.to_dict())


def test_context_provider_validation():
    with pytest.raises(Exception):
        ContextProvider()


def test_context_provider_full_creation():
    config = CONTEXT_PROVIDER_FULL_CONFIG
    provider = ContextProvider(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, provider.to_dict())


def test_context_provider_default_values():
    config = CONTEXT_PROVIDER_MINIMAL_CONFIG
    provider = ContextProvider(**config)
    expected = {
        **config,
        **CONTEXT_PROVIDER_DEFAULT_FIELDS,
    }
    assertion.assert_deep_almost_equal(expected, provider.to_dict())


def test_context_provider_extra_data_key():
    provider = ContextProvider(name=Name.KPathFormDataManager)
    assert provider.extra_data_key == "KPathFormDataManagerExtraData"


def test_context_provider_is_edited_key():
    provider = ContextProvider(name=Name.KPathFormDataManager)
    assert provider.is_edited_key == "isKPathFormDataManagerEdited"


def test_context_provider_is_unit_context_provider():
    unit_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="unit")
    assert unit_provider.is_unit_context_provider is True
    subworkflow_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="subworkflow")
    assert subworkflow_provider.is_unit_context_provider is False


def test_context_provider_is_subworkflow_context_provider():
    unit_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="unit")
    assert unit_provider.is_subworkflow_context_provider is False
    subworkflow_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="subworkflow")
    assert subworkflow_provider.is_subworkflow_context_provider is True


def test_context_provider_yield_data_with_external_context():
    provider = ContextProvider(**CONTEXT_PROVIDER_WITH_DEFAULT_DATA)
    external_context = EXTERNAL_CONTEXT_OVERRIDE
    result = provider.yield_data_for_rendering(external_context)
    expected = EXPECTED_YIELD_DATA_WITH_EXTERNAL
    assertion.assert_deep_almost_equal(expected, result)


def test_context_provider_yield_data_with_stored_context():
    provider = ContextProvider(**CONTEXT_PROVIDER_WITH_STORED_CONTEXT)
    result = provider.yield_data_for_rendering()
    expected = EXPECTED_YIELD_DATA_WITH_STORED
    assertion.assert_deep_almost_equal(expected, result)

