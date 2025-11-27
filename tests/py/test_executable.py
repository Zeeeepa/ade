"""Tests for Executable class."""

import pytest
from mat3ra.ade import Executable


class TestExecutable:
    """Test suite for Executable class."""

    def test_executable_creation(self):
        """Test basic executable creation."""
        exe = Executable(name="pw.x")
        assert exe.name == "pw.x"
        assert exe.applicationId is None
        assert exe.hasAdvancedComputeOptions is None
        assert exe.isDefault is None
        assert exe.preProcessors is None
        assert exe.postProcessors is None
        assert exe.monitors is None
        assert exe.results is None

    def test_executable_with_all_fields(self):
        """Test executable creation with all fields."""
        exe = Executable(
            name="pw.x",
            applicationId=["app1", "app2"],
            hasAdvancedComputeOptions=True,
            isDefault=True,
            schemaVersion="1.0.0",
            preProcessors=[{"name": "prep1"}],
            postProcessors=[{"name": "post1"}],
            monitors=[{"name": "mon1"}],
            results=[{"name": "res1"}],
        )
        assert exe.name == "pw.x"
        assert exe.applicationId == ["app1", "app2"]
        assert exe.hasAdvancedComputeOptions is True
        assert exe.isDefault is True
        assert exe.schemaVersion == "1.0.0"
        assert len(exe.preProcessors) == 1
        assert len(exe.postProcessors) == 1
        assert len(exe.monitors) == 1
        assert len(exe.results) == 1

    def test_executable_application_id_setter(self):
        """Test setting applicationId."""
        exe = Executable(name="pw.x")
        assert exe.applicationId is None

        exe.applicationId = ["app1", "app2"]
        assert exe.applicationId == ["app1", "app2"]

    def test_executable_to_dict(self):
        """Test converting executable to dictionary."""
        exe = Executable(name="pw.x", applicationId=["app1"])
        exe_dict = exe.model_dump()
        assert isinstance(exe_dict, dict)
        assert exe_dict["name"] == "pw.x"
        assert exe_dict["applicationId"] == ["app1"]

    def test_executable_from_dict(self):
        """Test creating executable from dictionary."""
        exe_dict = {
            "name": "pw.x",
            "applicationId": ["app1"],
            "isDefault": True,
            "monitors": [{"name": "convergence"}],
            "results": [{"name": "total_energy"}],
        }
        exe = Executable(**exe_dict)
        assert exe.name == "pw.x"
        assert exe.applicationId == ["app1"]
        assert exe.isDefault is True
        assert len(exe.monitors) == 1
        assert len(exe.results) == 1

    def test_executable_with_extra_fields(self):
        """Test that extra fields are allowed."""
        exe = Executable(name="pw.x", custom_field="custom_value")
        assert exe.name == "pw.x"
        assert hasattr(exe, "custom_field")

    def test_executable_validation(self):
        """Test that name is required."""
        with pytest.raises(Exception):
            Executable()  # Should raise validation error for missing name
