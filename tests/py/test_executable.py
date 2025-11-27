from mat3ra.ade import Executable


def test_executable_creation():
    executable = Executable(name="pw.x")
    assert executable.name == "pw.x"
    assert executable.applicationId is None
    assert executable.hasAdvancedComputeOptions is None
    assert executable.isDefault is False
    assert executable.preProcessors is None
    assert executable.postProcessors is None
    assert executable.monitors is None
    assert executable.results is None


def test_executable_with_all_fields():
    executable = Executable(
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
    assert executable.name == "pw.x"
    assert executable.applicationId == ["app1", "app2"]
    assert executable.hasAdvancedComputeOptions is True
    assert executable.isDefault is True
    assert executable.schemaVersion == "1.0.0"
    assert len(executable.preProcessors) == 1
    assert len(executable.postProcessors) == 1
    assert len(executable.monitors) == 1
    assert len(executable.results) == 1


def test_executable_application_id_setter():
    executable = Executable(name="pw.x")
    assert executable.applicationId is None

    executable.applicationId = ["app1", "app2"]
    assert executable.applicationId == ["app1", "app2"]


def test_executable_to_dict():
    executable = Executable(name="pw.x", applicationId=["app1"])
    executable_dict = executable.model_dump()
    assert isinstance(executable_dict, dict)
    assert executable_dict["name"] == "pw.x"
    assert executable_dict["applicationId"] == ["app1"]


def test_executable_from_dict():
    executable_dict = {
        "name": "pw.x",
        "applicationId": ["app1"],
        "isDefault": True,
        "monitors": [{"name": "convergence"}],
        "results": [{"name": "total_energy"}],
    }
    executable = Executable(**executable_dict)
    assert executable.name == "pw.x"
    assert executable.applicationId == ["app1"]
    assert executable.isDefault is True
    assert len(executable.monitors) == 1
    assert len(executable.results) == 1

