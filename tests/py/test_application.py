from mat3ra.ade import Application
from mat3ra.utils import assertion


def test_application_creation():
    config = {"name": "espresso"}
    app = Application(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, app.model_dump(exclude_unset=True))


def test_application_with_all_fields():
    config = {
        "name": "vasp",
        "version": "5.4.4",
        "build": "standard",
        "shortName": "VASP",
        "summary": "Vienna Ab initio Simulation Package",
        "hasAdvancedComputeOptions": True,
        "isLicensed": True,
        "isDefault": True,
        "schemaVersion": "1.0.0",
    }
    app = Application(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, app.model_dump(exclude_unset=True))


def test_is_using_material_property():
    vasp = Application(name="vasp")
    assert vasp.is_using_material is True

    nwchem = Application(name="nwchem")
    assert nwchem.is_using_material is True

    espresso = Application(name="espresso")
    assert espresso.is_using_material is True

    other = Application(name="other_app")
    assert other.is_using_material is False


def test_get_short_name():
    app_with_short = Application(name="espresso", shortName="QE")
    assert app_with_short.get_short_name() == "QE"

    app_without_short = Application(name="espresso")
    assert app_without_short.get_short_name() == "espresso"


def test_application_to_dict():
    config = {"name": "espresso", "version": "7.2"}
    app = Application(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, app.model_dump(exclude_unset=True))


def test_application_from_dict():
    config = {
        "name": "espresso",
        "version": "7.2",
        "build": "openmpi",
        "shortName": "QE",
    }
    app = Application(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, app.model_dump(exclude_unset=True))
