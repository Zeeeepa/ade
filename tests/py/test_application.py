"""Tests for Application class."""

import pytest
from mat3ra.ade import Application


class TestApplication:
    """Test suite for Application class."""

    def test_application_creation(self):
        """Test basic application creation."""
        app = Application(name="espresso")
        assert app.name == "espresso"
        assert app.version is None
        assert app.build is None
        assert app.hasAdvancedComputeOptions is None
        assert app.isLicensed is None

    def test_application_with_all_fields(self):
        """Test application creation with all fields."""
        app = Application(
            name="vasp",
            version="5.4.4",
            build="standard",
            shortName="VASP",
            summary="Vienna Ab initio Simulation Package",
            hasAdvancedComputeOptions=True,
            isLicensed=True,
            isDefault=True,
            schemaVersion="1.0.0",
        )
        assert app.name == "vasp"
        assert app.version == "5.4.4"
        assert app.build == "standard"
        assert app.shortName == "VASP"
        assert app.summary == "Vienna Ab initio Simulation Package"
        assert app.hasAdvancedComputeOptions is True
        assert app.isLicensed is True
        assert app.isDefault is True
        assert app.schemaVersion == "1.0.0"

    def test_is_using_material_property(self):
        """Test is_using_material property."""
        # Material using applications
        vasp = Application(name="vasp")
        assert vasp.is_using_material is True

        nwchem = Application(name="nwchem")
        assert nwchem.is_using_material is True

        espresso = Application(name="espresso")
        assert espresso.is_using_material is True

        # Non-material using application
        other = Application(name="other_app")
        assert other.is_using_material is False

    def test_get_short_name(self):
        """Test get_short_name method."""
        # With shortName set
        app_with_short = Application(name="espresso", shortName="QE")
        assert app_with_short.get_short_name() == "QE"

        # Without shortName set
        app_without_short = Application(name="espresso")
        assert app_without_short.get_short_name() == "espresso"

    def test_application_to_dict(self):
        """Test converting application to dictionary."""
        app = Application(name="espresso", version="7.2")
        app_dict = app.model_dump()
        assert isinstance(app_dict, dict)
        assert app_dict["name"] == "espresso"
        assert app_dict["version"] == "7.2"

    def test_application_from_dict(self):
        """Test creating application from dictionary."""
        app_dict = {
            "name": "espresso",
            "version": "7.2",
            "build": "openmpi",
            "shortName": "QE",
        }
        app = Application(**app_dict)
        assert app.name == "espresso"
        assert app.version == "7.2"
        assert app.build == "openmpi"
        assert app.shortName == "QE"

    def test_application_with_extra_fields(self):
        """Test that extra fields are allowed."""
        app = Application(name="espresso", custom_field="custom_value")
        assert app.name == "espresso"
        # Extra fields are stored in the model
        assert hasattr(app, "custom_field")

    def test_application_validation(self):
        """Test that name is required."""
        with pytest.raises(Exception):
            Application()  # Should raise validation error for missing name
