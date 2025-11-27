from mat3ra.ade import JinjaContextProvider, JSONSchemaDataProvider

from mat3ra.esse.models.context_provider import Name


def test_jinja_context_provider_creation():
    provider = JinjaContextProvider(name=Name.KGridFormDataManager)
    assert provider.name == Name.KGridFormDataManager
    assert provider.is_using_jinja_variables is False


def test_jinja_context_provider_with_jinja_variables():
    provider = JinjaContextProvider(name=Name.KGridFormDataManager, is_using_jinja_variables=True)
    assert provider.is_using_jinja_variables is True


def test_jinja_context_provider_inherits_context_provider():
    provider = JinjaContextProvider(
        name=Name.KGridFormDataManager,
        domain="custom",
        entityName="subworkflow",
        is_using_jinja_variables=True,
    )
    assert provider.domain == "custom"
    assert provider.entityName == "subworkflow"
    assert provider.is_using_jinja_variables is True
    assert provider.is_subworkflow_context_provider is True


def test_json_schema_data_provider_creation():
    provider = JSONSchemaDataProvider(name=Name.KGridFormDataManager)
    assert provider.name == Name.KGridFormDataManager
    assert provider.json_schema is None


def test_json_schema_data_provider_with_schema():
    schema = {"type": "object", "properties": {"value": {"type": "number"}}}
    provider = JSONSchemaDataProvider(name=Name.KGridFormDataManager, json_schema=schema)
    assert provider.json_schema == schema


def test_json_schema_data_provider_inherits_jinja():
    provider = JSONSchemaDataProvider(
        name=Name.KGridFormDataManager,
        is_using_jinja_variables=True,
        json_schema={"type": "object"},
    )
    assert provider.is_using_jinja_variables is True
    assert provider.json_schema == {"type": "object"}
