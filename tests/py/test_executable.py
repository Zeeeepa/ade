from mat3ra.ade import Executable
from mat3ra.utils import assertion


def test_executable_creation():
    config = {"name": "pw.x"}
    executable = Executable(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, executable.model_dump(exclude_unset=True))


def test_executable_with_all_fields():
    config = {
        "name": "pw.x",
        "applicationId": ["app1", "app2"],
        "hasAdvancedComputeOptions": True,
        "isDefault": True,
        "schemaVersion": "1.0.0",
        "preProcessors": [{"name": "prep1"}],
        "postProcessors": [{"name": "post1"}],
        "monitors": [{"name": "mon1"}],
        "results": [{"name": "res1"}],
    }
    executable = Executable(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, executable.model_dump(exclude_unset=True))


def test_executable_application_id_setter():
    executable = Executable(name="pw.x")
    assert executable.applicationId is None

    executable.applicationId = ["app1", "app2"]
    assert executable.applicationId == ["app1", "app2"]


def test_executable_to_dict():
    config = {"name": "pw.x", "applicationId": ["app1"]}
    executable = Executable(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, executable.model_dump(exclude_unset=True))


def test_executable_from_dict():
    config = {
        "name": "pw.x",
        "applicationId": ["app1"],
        "isDefault": True,
        "monitors": [{"name": "convergence"}],
        "results": [{"name": "total_energy"}],
    }
    executable = Executable(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, executable.model_dump(exclude_unset=True))
