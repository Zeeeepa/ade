from mat3ra.ade import Flavor, FlavorInput


def test_flavor_input_creation():
    input = FlavorInput(name="input.in")
    assert input.name == "input.in"
    assert input.templateId is None
    assert input.templateName is None


def test_flavor_input_with_all_fields():
    input = FlavorInput(templateId="tmpl_123", templateName="pw_scf", name="pw_scf.in")
    assert input.templateId == "tmpl_123"
    assert input.templateName == "pw_scf"
    assert input.name == "pw_scf.in"


def test_flavor_creation():
    """Test basic flavor creation."""
    flavor = Flavor(name="scf")
    assert flavor.name == "scf"
    assert flavor.executableId is None
    assert flavor.executableName is None
    assert flavor.applicationName is None
    assert flavor.input == []
    assert flavor.supportedApplicationVersions is None
    assert flavor.isDefault is False
    assert flavor.preProcessors is None
    assert flavor.postProcessors is None
    assert flavor.monitors is None
    assert flavor.results is None


def test_flavor_with_all_fields():
    flavor = Flavor(
        name="scf",
        executableId="exe_123",
        executableName="pw.x",
        applicationName="espresso",
        input=[FlavorInput(name="pw_scf.in", templateName="pw_scf")],
        supportedApplicationVersions=["7.0", "7.1", "7.2"],
        isDefault=True,
        schemaVersion="1.0.0",
        preProcessors=[{"name": "prep1"}],
        postProcessors=[{"name": "post1"}],
        monitors=[{"name": "convergence"}],
        results=[{"name": "total_energy"}],
    )
    assert flavor.name == "scf"
    assert flavor.executableId == "exe_123"
    assert flavor.executableName == "pw.x"
    assert flavor.applicationName == "espresso"
    assert len(flavor.input) == 1
    assert flavor.input[0].name == "pw_scf.in"
    assert flavor.supportedApplicationVersions == ["7.0", "7.1", "7.2"]
    assert flavor.isDefault is True
    assert flavor.schemaVersion == "1.0.0"
    assert len(flavor.preProcessors) == 1
    assert len(flavor.postProcessors) == 1
    assert len(flavor.monitors) == 1
    assert len(flavor.results) == 1


def test_flavor_to_dict():
    flavor = Flavor(
        name="scf",
        executableName="pw.x",
        applicationName="espresso",
    )
    flavor_dict = flavor.model_dump()
    assert isinstance(flavor_dict, dict)
    assert flavor_dict["name"] == "scf"
    assert flavor_dict["executableName"] == "pw.x"
    assert flavor_dict["applicationName"] == "espresso"


def test_flavor_from_dict():
    flavor_dict = {
        "name": "scf",
        "executableName": "pw.x",
        "applicationName": "espresso",
        "input": [{"name": "pw_scf.in", "templateName": "pw_scf"}],
        "supportedApplicationVersions": ["7.0", "7.1"],
    }
    flavor = Flavor(**flavor_dict)
    assert flavor.name == "scf"
    assert flavor.executableName == "pw.x"
    assert flavor.applicationName == "espresso"
    assert len(flavor.input) == 1
    assert flavor.supportedApplicationVersions == ["7.0", "7.1"]


def test_flavor_with_extra_fields():
    flavor = Flavor(name="scf", custom_field="custom_value")
    assert flavor.name == "scf"
    assert hasattr(flavor, "custom_field")
