"""Integration tests demonstrating usage of all classes together."""

from mat3ra.ade import Application, ContextProvider, Executable, Flavor, FlavorInput, Template
from mat3ra.esse.models.context_provider import Name


def test_end_to_end_workflow():
    """Test creating and using all classes together."""
    app = Application(
        name="espresso",
        version="7.2",
        build="standard",
        shortName="QE",
        summary="Quantum ESPRESSO",
        hasAdvancedComputeOptions=True,
        isLicensed=False,
    )

    assert app.name == "espresso"
    assert app.get_short_name() == "QE"
    assert app.is_using_material is True

    executable = Executable(
        name="pw.x",
        applicationId=[app.name],
        isDefault=True,
        monitors=[{"name": "convergence"}],
        results=[{"name": "total_energy"}, {"name": "band_gap"}],
    )

    assert executable.name == "pw.x"
    assert executable.applicationId == ["espresso"]
    assert len(executable.results) == 2

    template = Template(
        name="pw_scf.in",
        content="&CONTROL\n  calculation='scf'\n/",
        applicationName=app.name,
        executableName=executable.name,
        context_providers=[ContextProvider(name=Name.KGridFormDataManager)],
    )

    assert template.name == "pw_scf.in"
    assert template.get_rendered() == "&CONTROL\n  calculation='scf'\n/"
    assert len(template.context_providers) == 1

    flavor = Flavor(
        name="scf",
        executableName=executable.name,
        applicationName=app.name,
        input=[FlavorInput(templateName=template.name, name="pw_scf.in")],
        supportedApplicationVersions=["7.0", "7.1", "7.2"],
        isDefault=True,
    )

    assert flavor.name == "scf"
    assert flavor.applicationName == app.name
    assert flavor.executableName == executable.name
    assert len(flavor.input) == 1
    assert flavor.input[0].templateName == template.name


def test_serialization_workflow():
    """Test serialization and deserialization of all classes."""
    app = Application(name="vasp", version="5.4.4")
    executable = Executable(name="vasp_std", applicationId=["vasp"])
    template = Template(name="INCAR", content="SYSTEM = Test")
    flavor = Flavor(
        name="standard",
        applicationName="vasp",
        executableName="vasp_std",
    )

    app_dict = app.model_dump()
    exe_dict = executable.model_dump()
    tmpl_dict = template.model_dump()
    flv_dict = flavor.model_dump()

    assert isinstance(app_dict, dict)
    assert isinstance(exe_dict, dict)
    assert isinstance(tmpl_dict, dict)
    assert isinstance(flv_dict, dict)

    app_restored = Application(**app_dict)
    exe_restored = Executable(**exe_dict)
    tmpl_restored = Template(**tmpl_dict)
    flv_restored = Flavor(**flv_dict)

    assert app_restored.name == app.name
    assert exe_restored.name == executable.name
    assert tmpl_restored.name == template.name
    assert flv_restored.name == flavor.name
