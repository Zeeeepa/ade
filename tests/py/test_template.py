"""Tests for Template class."""

import pytest
from mat3ra.ade import ContextProvider, Template

from mat3ra.esse.models.context_provider import Name


def test_template_creation():
    template = Template(name="pw_scf.in", content="&CONTROL\n  calculation='scf'\n/")
    assert template.name == "pw_scf.in"
    assert template.content == "&CONTROL\n  calculation='scf'\n/"
    assert template.rendered is None
    assert template.applicationName is None
    assert template.applicationVersion is None
    assert template.executableName is None
    assert template.context_providers == []
    assert template.isManuallyChanged is None
    assert template.schemaVersion == "2022.8.16"


def test_template_with_all_fields():
    template = Template(
        name="pw_scf.in",
        content="&CONTROL\n  calculation='scf'\n/",
        rendered="&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
        applicationName="espresso",
        applicationVersion="7.2",
        executableName="pw.x",
        context_providers=[ContextProvider(name=Name.KGridFormDataManager)],
        isManuallyChanged=True,
        schemaVersion="1.0.0",
    )
    assert template.name == "pw_scf.in"
    assert template.content == "&CONTROL\n  calculation='scf'\n/"
    assert template.rendered == "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/"
    assert template.applicationName == "espresso"
    assert template.applicationVersion == "7.2"
    assert template.executableName == "pw.x"
    assert len(template.context_providers) == 1
    assert template.context_providers[0].name == Name.KGridFormDataManager
    assert template.isManuallyChanged is True
    assert template.schemaVersion == "1.0.0"


def test_get_rendered():
    template_with_rendered = Template(name="test.in", content="original content", rendered="rendered content")
    assert template_with_rendered.get_rendered() == "rendered content"

    template_without_rendered = Template(name="test.in", content="original content")
    assert template_without_rendered.get_rendered() == "original content"


def test_template_to_dict():
    template = Template(
        name="pw_scf.in",
        content="&CONTROL\n/",
        applicationName="espresso",
    )
    template_dict = template.model_dump()
    assert isinstance(template_dict, dict)
    assert template_dict["name"] == "pw_scf.in"
    assert template_dict["content"] == "&CONTROL\n/"
    assert template_dict["applicationName"] == "espresso"


def test_template_from_dict():
    template_dict = {
        "name": "pw_scf.in",
        "content": "&CONTROL\n/",
        "applicationName": "espresso",
        "executableName": "pw.x",
        "context_providers": [{"name": Name.KGridFormDataManager}],
    }
    template = Template(**template_dict)
    assert template.name == "pw_scf.in"
    assert template.content == "&CONTROL\n/"
    assert template.applicationName == "espresso"
    assert template.executableName == "pw.x"
    assert len(template.context_providers) == 1


def test_template_with_extra_fields():
    template = Template(name="test.in", content="content", custom_field="custom_value")
    assert template.name == "test.in"
    assert hasattr(template, "custom_field")


def test_template_validation():
    with pytest.raises(Exception):
        Template()

    with pytest.raises(Exception):
        Template(name="test.in")

    with pytest.raises(Exception):
        Template(content="content")
