
import pytest
from mat3ra.ade import ContextProvider

from mat3ra.esse.models.context_provider import Name


def test_context_provider_creation():
    provider = ContextProvider(name=Name.KGridFormDataManager)
    assert provider.name == Name.KGridFormDataManager


def test_context_provider_validation():
    with pytest.raises(Exception):
        ContextProvider()


def test_context_provider_full_creation():
    provider = ContextProvider(
        name=Name.KGridFormDataManager,
        domain="test_domain",
        entityName="subworkflow",
        data={"key": "value"},
        extraData={"extraKey": "extraValue"},
        isEdited=True,
        context={"contextKey": "contextValue"},
    )
    assert provider.name == Name.KGridFormDataManager
    assert provider.domain == "test_domain"
    assert provider.entityName == "subworkflow"
    assert provider.data == {"key": "value"}
    assert provider.extraData == {"extraKey": "extraValue"}
    assert provider.isEdited is True
    assert provider.context == {"contextKey": "contextValue"}


def test_context_provider_default_values():
    provider = ContextProvider(name=Name.KGridFormDataManager)
    assert provider.domain is None
    assert provider.entityName is None
    assert provider.data is None
    assert provider.extraData is None
    assert provider.isEdited is None
    assert provider.context is None


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

