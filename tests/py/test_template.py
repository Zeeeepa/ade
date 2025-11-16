"""Tests for Template class."""

import pytest
from mat3ra.ade import ContextProvider, Template


class TestContextProvider:
    """Test suite for ContextProvider class."""

    def test_context_provider_creation(self):
        """Test basic ContextProvider creation."""
        provider = ContextProvider(name="material")
        assert provider.name == "material"

    def test_context_provider_validation(self):
        """Test that name is required."""
        with pytest.raises(Exception):
            ContextProvider()  # Should raise validation error for missing name


class TestTemplate:
    """Test suite for Template class."""

    def test_template_creation(self):
        """Test basic template creation."""
        tmpl = Template(name="pw_scf.in", content="&CONTROL\n  calculation='scf'\n/")
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n  calculation='scf'\n/"
        assert tmpl.rendered is None
        assert tmpl.application_name is None
        assert tmpl.application_version is None
        assert tmpl.executable_name is None
        assert tmpl.context_providers == []
        assert tmpl.is_manually_changed is False
        assert tmpl.schema_version is None

    def test_template_with_all_fields(self):
        """Test template creation with all fields."""
        tmpl = Template(
            name="pw_scf.in",
            content="&CONTROL\n  calculation='scf'\n/",
            rendered="&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
            application_name="espresso",
            application_version="7.2",
            executable_name="pw.x",
            context_providers=[ContextProvider(name="material")],
            is_manually_changed=True,
            schema_version="1.0.0",
        )
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n  calculation='scf'\n/"
        assert tmpl.rendered == "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/"
        assert tmpl.application_name == "espresso"
        assert tmpl.application_version == "7.2"
        assert tmpl.executable_name == "pw.x"
        assert len(tmpl.context_providers) == 1
        assert tmpl.context_providers[0].name == "material"
        assert tmpl.is_manually_changed is True
        assert tmpl.schema_version == "1.0.0"

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
            application_name="espresso",
        )
        tmpl_dict = tmpl.model_dump()
        assert isinstance(tmpl_dict, dict)
        assert tmpl_dict["name"] == "pw_scf.in"
        assert tmpl_dict["content"] == "&CONTROL\n/"
        assert tmpl_dict["application_name"] == "espresso"

    def test_template_from_dict(self):
        """Test creating template from dictionary."""
        tmpl_dict = {
            "name": "pw_scf.in",
            "content": "&CONTROL\n/",
            "application_name": "espresso",
            "executable_name": "pw.x",
            "context_providers": [{"name": "material"}],
        }
        tmpl = Template(**tmpl_dict)
        assert tmpl.name == "pw_scf.in"
        assert tmpl.content == "&CONTROL\n/"
        assert tmpl.application_name == "espresso"
        assert tmpl.executable_name == "pw.x"
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
