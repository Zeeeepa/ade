"""Tests for Executable class."""

import pytest
from mat3ra.ade import Executable


class TestExecutable:
    """Test suite for Executable class."""

    def test_executable_creation(self):
        """Test basic executable creation."""
        exe = Executable(name="pw.x")
        assert exe.name == "pw.x"
        assert exe.application_id == []
        assert exe.has_advanced_compute_options is None
        assert exe.is_default is None
        assert exe.pre_processors == []
        assert exe.post_processors == []
        assert exe.monitors == []
        assert exe.results == []

    def test_executable_with_all_fields(self):
        """Test executable creation with all fields."""
        exe = Executable(
            name="pw.x",
            application_id=["app1", "app2"],
            has_advanced_compute_options=True,
            is_default=True,
            schema_version="1.0.0",
            pre_processors=[{"name": "prep1"}],
            post_processors=[{"name": "post1"}],
            monitors=[{"name": "mon1"}],
            results=[{"name": "res1"}],
        )
        assert exe.name == "pw.x"
        assert exe.application_id == ["app1", "app2"]
        assert exe.has_advanced_compute_options is True
        assert exe.is_default is True
        assert exe.schema_version == "1.0.0"
        assert len(exe.pre_processors) == 1
        assert len(exe.post_processors) == 1
        assert len(exe.monitors) == 1
        assert len(exe.results) == 1

    def test_executable_application_id_setter(self):
        """Test setting application_id."""
        exe = Executable(name="pw.x")
        assert exe.application_id == []

        exe.application_id = ["app1", "app2"]
        assert exe.application_id == ["app1", "app2"]

    def test_executable_to_dict(self):
        """Test converting executable to dictionary."""
        exe = Executable(name="pw.x", application_id=["app1"])
        exe_dict = exe.model_dump()
        assert isinstance(exe_dict, dict)
        assert exe_dict["name"] == "pw.x"
        assert exe_dict["application_id"] == ["app1"]

    def test_executable_from_dict(self):
        """Test creating executable from dictionary."""
        exe_dict = {
            "name": "pw.x",
            "application_id": ["app1"],
            "is_default": True,
            "monitors": [{"name": "convergence"}],
            "results": [{"name": "total_energy"}],
        }
        exe = Executable(**exe_dict)
        assert exe.name == "pw.x"
        assert exe.application_id == ["app1"]
        assert exe.is_default is True
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
