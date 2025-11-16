"""Tests for Flavor class."""

import pytest
from mat3ra.ade import Flavor, FlavorInput


class TestFlavorInput:
    """Test suite for FlavorInput class."""

    def test_flavor_input_creation(self):
        """Test basic FlavorInput creation."""
        inp = FlavorInput(name="input.in")
        assert inp.name == "input.in"
        assert inp.template_id is None
        assert inp.template_name is None

    def test_flavor_input_with_all_fields(self):
        """Test FlavorInput creation with all fields."""
        inp = FlavorInput(template_id="tmpl_123", template_name="pw_scf", name="pw_scf.in")
        assert inp.template_id == "tmpl_123"
        assert inp.template_name == "pw_scf"
        assert inp.name == "pw_scf.in"


class TestFlavor:
    """Test suite for Flavor class."""

    def test_flavor_creation(self):
        """Test basic flavor creation."""
        flavor = Flavor(name="scf")
        assert flavor.name == "scf"
        assert flavor.executable_id == ""
        assert flavor.executable_name == ""
        assert flavor.application_name == ""
        assert flavor.input == []
        assert flavor.supported_application_versions is None
        assert flavor.disable_render_materials is False
        assert flavor.is_default is None
        assert flavor.pre_processors == []
        assert flavor.post_processors == []
        assert flavor.monitors == []
        assert flavor.results == []

    def test_flavor_with_all_fields(self):
        """Test flavor creation with all fields."""
        flavor = Flavor(
            name="scf",
            executable_id="exe_123",
            executable_name="pw.x",
            application_name="espresso",
            input=[FlavorInput(name="pw_scf.in", template_name="pw_scf")],
            supported_application_versions=["7.0", "7.1", "7.2"],
            disable_render_materials=True,
            is_default=True,
            schema_version="1.0.0",
            pre_processors=[{"name": "prep1"}],
            post_processors=[{"name": "post1"}],
            monitors=[{"name": "convergence"}],
            results=[{"name": "total_energy"}],
        )
        assert flavor.name == "scf"
        assert flavor.executable_id == "exe_123"
        assert flavor.executable_name == "pw.x"
        assert flavor.application_name == "espresso"
        assert len(flavor.input) == 1
        assert flavor.input[0].name == "pw_scf.in"
        assert flavor.supported_application_versions == ["7.0", "7.1", "7.2"]
        assert flavor.disable_render_materials is True
        assert flavor.is_default is True
        assert flavor.schema_version == "1.0.0"
        assert len(flavor.pre_processors) == 1
        assert len(flavor.post_processors) == 1
        assert len(flavor.monitors) == 1
        assert len(flavor.results) == 1

    def test_flavor_to_dict(self):
        """Test converting flavor to dictionary."""
        flavor = Flavor(
            name="scf",
            executable_name="pw.x",
            application_name="espresso",
        )
        flavor_dict = flavor.model_dump()
        assert isinstance(flavor_dict, dict)
        assert flavor_dict["name"] == "scf"
        assert flavor_dict["executable_name"] == "pw.x"
        assert flavor_dict["application_name"] == "espresso"

    def test_flavor_from_dict(self):
        """Test creating flavor from dictionary."""
        flavor_dict = {
            "name": "scf",
            "executable_name": "pw.x",
            "application_name": "espresso",
            "input": [{"name": "pw_scf.in", "template_name": "pw_scf"}],
            "supported_application_versions": ["7.0", "7.1"],
        }
        flavor = Flavor(**flavor_dict)
        assert flavor.name == "scf"
        assert flavor.executable_name == "pw.x"
        assert flavor.application_name == "espresso"
        assert len(flavor.input) == 1
        assert flavor.supported_application_versions == ["7.0", "7.1"]

    def test_flavor_with_extra_fields(self):
        """Test that extra fields are allowed."""
        flavor = Flavor(name="scf", custom_field="custom_value")
        assert flavor.name == "scf"
        assert hasattr(flavor, "custom_field")

    def test_flavor_validation(self):
        """Test that name is required."""
        with pytest.raises(Exception):
            Flavor()  # Should raise validation error for missing name
