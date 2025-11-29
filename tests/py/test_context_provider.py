import pytest
from mat3ra.ade import ContextProvider
from mat3ra.esse.models.context_provider import Name
from mat3ra.utils import assertion


def test_context_provider_creation():
    config = {"name": Name.KGridFormDataManager}
    provider = ContextProvider(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, provider.model_dump(exclude_unset=True))


def test_context_provider_validation():
    with pytest.raises(Exception):
        ContextProvider()


def test_context_provider_full_creation():
    config = {
        "name": Name.KGridFormDataManager,
        "domain": "test_domain",
        "entityName": "subworkflow",
        "data": {"key": "value"},
        "extraData": {"extraKey": "extraValue"},
        "isEdited": True,
        "context": {"contextKey": "contextValue"},
    }
    provider = ContextProvider(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, provider.model_dump(exclude_unset=True))


def test_context_provider_default_values():
    config = {"name": Name.KGridFormDataManager}
    provider = ContextProvider(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, provider.model_dump(exclude_unset=True))


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
    provider = ContextProvider(
        name=Name.KPathFormDataManager,
        data={"default": "value"},
        isEdited=False,
        extraData={"extra": "data"}
    )
    external_context = {
        "KPathFormDataManager": {"override": "value"},
        "isKPathFormDataManagerEdited": True,
        "KPathFormDataManagerExtraData": {"extra_override": "data"}
    }
    result = provider.yield_data_for_rendering(external_context)
    assert result["KPathFormDataManager"] == {"override": "value"}
    assert result["isKPathFormDataManagerEdited"] is True
    assert result["KPathFormDataManagerExtraData"] == {"extra_override": "data"}


def test_context_provider_yield_data_with_stored_context():
    provider = ContextProvider(
        name=Name.KPathFormDataManager,
        data={"default": "value"},
        isEdited=False,
        context={
            "KPathFormDataManager": {"stored": "value"},
            "isKPathFormDataManagerEdited": True
        }
    )
    result = provider.yield_data_for_rendering()
    assert result["KPathFormDataManager"] == {"stored": "value"}
    assert result["isKPathFormDataManagerEdited"] is True

