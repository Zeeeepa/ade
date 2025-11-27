import pytest
from mat3ra.ade import ContextProvider, Template
from mat3ra.esse.models.context_provider import Name
from mat3ra.utils import assertion


def test_template_creation():
    config = {
        "name": "pw_scf.in",
        "content": "&CONTROL\n  calculation='scf'\n/",
    }
    template = Template(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, template.model_dump(exclude_unset=True))


def test_template_with_all_fields():
    config = {
        "name": "pw_scf.in",
        "content": "&CONTROL\n  calculation='scf'\n/",
        "rendered": "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
        "applicationName": "espresso",
        "applicationVersion": "7.2",
        "executableName": "pw.x",
        "context_providers": [ContextProvider(name=Name.KGridFormDataManager)],
        "isManuallyChanged": True,
        "schemaVersion": "1.0.0",
    }
    template = Template(**config)
    expected = {
        **config,
        "context_providers": [{"name": Name.KGridFormDataManager}],
    }
    assertion.assert_deep_almost_equal(expected, template.model_dump(exclude_unset=True))


def test_get_rendered():
    config_with_rendered = {"name": "test.in", "content": "original content", "rendered": "rendered content"}
    template_with_rendered = Template(**config_with_rendered)
    assert template_with_rendered.get_rendered() == "rendered content"

    config_without_rendered = {"name": "test.in", "content": "original content"}
    template_without_rendered = Template(**config_without_rendered)
    assert template_without_rendered.get_rendered() == "original content"


def test_template_to_dict():
    config = {
        "name": "pw_scf.in",
        "content": "&CONTROL\n/",
        "applicationName": "espresso",
    }
    template = Template(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, template.model_dump(exclude_unset=True))


def test_template_from_dict():
    config = {
        "name": "pw_scf.in",
        "content": "&CONTROL\n/",
        "applicationName": "espresso",
        "executableName": "pw.x",
        "context_providers": [{"name": Name.KGridFormDataManager}],
    }
    template = Template(**config)
    expected = {**config}
    assertion.assert_deep_almost_equal(expected, template.model_dump(exclude_unset=True))


def test_template_with_extra_fields():
    config = {"name": "test.in", "content": "content", "custom_field": "custom_value"}
    template = Template(**config)
    assert template.name == "test.in"
    assert hasattr(template, "custom_field")


def test_template_validation():
    with pytest.raises(Exception):
        Template()

    with pytest.raises(Exception):
        Template(name="test.in")

    with pytest.raises(Exception):
        Template(content="content")


def test_set_content():
    config = {"name": "test.in", "content": "original"}
    template = Template(**config)
    template.set_content("new content")
    assert template.content == "new content"


def test_set_rendered():
    config = {"name": "test.in", "content": "original"}
    template = Template(**config)
    template.set_rendered("rendered")
    assert template.rendered == "rendered"


def test_add_context_provider():
    config = {"name": "test.in", "content": "content"}
    template = Template(**config)
    provider = ContextProvider(name=Name.KGridFormDataManager)
    template.add_context_provider(provider)
    assert len(template.context_providers) == 1
    assert template.context_providers[0].name == Name.KGridFormDataManager


def test_remove_context_provider():
    provider1 = ContextProvider(name=Name.KGridFormDataManager, domain="test")
    provider2 = ContextProvider(name=Name.KPathFormDataManager, domain="test")
    config = {"name": "test.in", "content": "content", "context_providers": [provider1, provider2]}
    template = Template(**config)
    template.remove_context_provider(provider1)
    assert len(template.context_providers) == 1
    assert template.context_providers[0].name == Name.KPathFormDataManager


def test_render():
    config = {"name": "test.in", "content": "Hello {{ name }}!"}
    template = Template(**config)
    template.render({"name": "World"})
    assert template.rendered == "Hello World!"


def test_render_with_context_provider():
    provider = ContextProvider(name=Name.KGridFormDataManager, data={"value": 42}, isEdited=True)
    config = {
        "name": "test.in",
        "content": "Value is {{ KGridFormDataManager.value }}",
        "context_providers": [provider],
    }
    template = Template(**config)
    template.render()
    assert "42" in template.rendered or "value" in template.rendered


def test_render_manually_changed():
    config = {"name": "test.in", "content": "Hello {{ name }}!", "isManuallyChanged": True}
    template = Template(**config)
    template.render({"name": "World"})
    assert template.rendered is None


def test_get_rendered_json():
    config = {"name": "test.in", "content": "Hello {{ name }}!"}
    template = Template(**config)
    result = template.get_rendered_json({"name": "World"})
    assert result["name"] == config["name"]
    assert result["content"] == config["content"]
    assert result["rendered"] == "Hello World!"
    assert result["schemaVersion"] == "2022.8.16"
