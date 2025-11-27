import pytest
from mat3ra.ade import (
    ContextProvider,
    JinjaContextProvider,
    JSONSchemaDataProvider,
    Template,
)

from mat3ra.esse.models.context_provider import Name


class TestContextProvider:
    """Test suite for ContextProvider class."""

    def test_context_provider_creation(self):
        """Test basic ContextProvider creation."""
        provider = ContextProvider(name=Name.KGridFormDataManager)
        assert provider.name == Name.KGridFormDataManager

    def test_context_provider_validation(self):
        """Test that name is required."""
        with pytest.raises(Exception):
            ContextProvider()  # Should raise validation error for missing name

    def test_context_provider_full_creation(self):
        """Test ContextProvider creation with all fields."""
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

    def test_context_provider_default_values(self):
        """Test ContextProvider default values."""
        provider = ContextProvider(name=Name.KGridFormDataManager)
        assert provider.domain == "default"
        assert provider.entityName == "unit"
        assert provider.data is None
        assert provider.extraData is None
        assert provider.isEdited is None
        assert provider.context is None

    def test_context_provider_extra_data_key(self):
        """Test extra_data_key property."""
        provider = ContextProvider(name=Name.KPathFormDataManager)
        assert provider.extra_data_key == "KPathFormDataManagerExtraData"

    def test_context_provider_is_edited_key(self):
        """Test is_edited_key property."""
        provider = ContextProvider(name=Name.KPathFormDataManager)
        assert provider.is_edited_key == "isKPathFormDataManagerEdited"

    def test_context_provider_is_unit_context_provider(self):
        """Test is_unit_context_provider property."""
        unit_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="unit")
        assert unit_provider.is_unit_context_provider is True
        subworkflow_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="subworkflow")
        assert subworkflow_provider.is_unit_context_provider is False

    def test_context_provider_is_subworkflow_context_provider(self):
        """Test is_subworkflow_context_provider property."""
        unit_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="unit")
        assert unit_provider.is_subworkflow_context_provider is False
        subworkflow_provider = ContextProvider(name=Name.KGridFormDataManager, entityName="subworkflow")
        assert subworkflow_provider.is_subworkflow_context_provider is True


class TestJinjaContextProvider:
    """Test suite for JinjaContextProvider class."""

    def test_jinja_context_provider_creation(self):
        """Test JinjaContextProvider creation."""
        provider = JinjaContextProvider(name=Name.KGridFormDataManager)
        assert provider.name == Name.KGridFormDataManager
        assert provider.is_using_jinja_variables is False

    def test_jinja_context_provider_with_jinja_variables(self):
        """Test JinjaContextProvider with is_using_jinja_variables set."""
        provider = JinjaContextProvider(name=Name.KGridFormDataManager, is_using_jinja_variables=True)
        assert provider.is_using_jinja_variables is True

    def test_jinja_context_provider_inherits_context_provider(self):
        """Test that JinjaContextProvider inherits from ContextProvider."""
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


class TestJSONSchemaDataProvider:
    """Test suite for JSONSchemaDataProvider class."""

    def test_json_schema_data_provider_creation(self):
        """Test JSONSchemaDataProvider creation."""
        provider = JSONSchemaDataProvider(name=Name.KGridFormDataManager)
        assert provider.name == Name.KGridFormDataManager
        assert provider.json_schema is None

    def test_json_schema_data_provider_with_schema(self):
        """Test JSONSchemaDataProvider with json_schema set."""
        schema = {"type": "object", "properties": {"value": {"type": "number"}}}
        provider = JSONSchemaDataProvider(name=Name.KGridFormDataManager, json_schema=schema)
        assert provider.json_schema == schema

    def test_json_schema_data_provider_inherits_jinja(self):
        """Test that JSONSchemaDataProvider inherits from JinjaContextProvider."""
        provider = JSONSchemaDataProvider(
            name=Name.KGridFormDataManager,
            is_using_jinja_variables=True,
            json_schema={"type": "object"},
        )
        assert provider.is_using_jinja_variables is True
        assert provider.json_schema == {"type": "object"}



class TestTemplate:
    """Test suite for Template class."""

    def test_template_creation(self):
        """Test basic template creation."""
        tmpl = Template(name="pw_scf.in", content="&CONTROL\n  calculation='scf'\n/")
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n  calculation='scf'\n/"
        assert tmpl.rendered is None
        assert tmpl.applicationName is None
        assert tmpl.applicationVersion is None
        assert tmpl.executableName is None
        assert tmpl.context_providers == []
        assert tmpl.isManuallyChanged is None
        assert tmpl.schemaVersion is None

    def test_template_with_all_fields(self):
        """Test template creation with all fields."""
        tmpl = Template(
            name="pw_scf.in",
            content="&CONTROL\n  calculation='scf'\n/",
            rendered="&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
            applicationName="espresso",
            applicationVersion="7.2",
            executableName="pw.x",
            context_providers=[ContextProvider(name=Name.KGridFormDataManager)],
            isManuallyChanged=True,
            schemaVersion="1.0.0",
        )
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n  calculation='scf'\n/"
        assert tmpl.rendered == "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/"
        assert tmpl.applicationName == "espresso"
        assert tmpl.applicationVersion == "7.2"
        assert tmpl.executableName == "pw.x"
        assert len(tmpl.context_providers) == 1
        assert tmpl.context_providers[0].name == Name.KGridFormDataManager
        assert tmpl.isManuallyChanged is True
        assert tmpl.schemaVersion == "1.0.0"

    def test_get_rendered(self):
        """Test get_rendered method."""
        # With rendered set
        tmpl_with_rendered = Template(name="test.in", content="original content", rendered="rendered content")
        assert tmpl_with_rendered.get_rendered() == "rendered content"

        # Without rendered set
        tmpl_without_rendered = Template(name="test.in", content="original content")
        assert tmpl_without_rendered.get_rendered() == "original content"

    def test_template_to_dict(self):
        """Test converting template to dictionary."""
        tmpl = Template(
            name="pw_scf.in",
            content="&CONTROL\n/",
            applicationName="espresso",
        )
        tmpl_dict = tmpl.model_dump()
        assert isinstance(tmpl_dict, dict)
        assert tmpl_dict["name"] == "pw_scf.in"
        assert tmpl_dict["content"] == "&CONTROL\n/"
        assert tmpl_dict["applicationName"] == "espresso"

    def test_template_from_dict(self):
        """Test creating template from dictionary."""
        tmpl_dict = {
            "name": "pw_scf.in",
            "content": "&CONTROL\n/",
            "applicationName": "espresso",
            "executableName": "pw.x",
            "context_providers": [{"name": Name.KGridFormDataManager}],
        }
        tmpl = Template(**tmpl_dict)
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n/"
        assert tmpl.applicationName == "espresso"
        assert tmpl.executableName == "pw.x"
        assert len(tmpl.context_providers) == 1

    def test_template_with_extra_fields(self):
        """Test that extra fields are allowed."""
        tmpl = Template(name="test.in", content="content", custom_field="custom_value")
        assert tmpl.name == "test.in"
        assert hasattr(tmpl, "custom_field")

    def test_template_validation(self):
        """Test that name and content are required."""
        with pytest.raises(Exception):
            Template()  # Should raise validation error for missing name and content

        with pytest.raises(Exception):
            Template(name="test.in")  # Should raise validation error for missing content

        with pytest.raises(Exception):
            Template(content="content")  # Should raise validation error for missing name
