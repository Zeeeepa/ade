import pytest
from mat3ra.ade import ContextProvider, Template
from mat3ra.esse.models.context_provider import Name
from mat3ra.utils import assertion

CONTEXT_PROVIDER_DEFAULT_FIELDS = {
    "domain": None,
    "entityName": None,
    "data": None,
    "extraData": None,
    "isEdited": None,
    "context": None,
}

TEMPLATE_DEFAULT_FIELDS = {
    "rendered": None,
    "applicationName": None,
    "applicationVersion": None,
    "executableName": None,
    "contextProviders": [],
    "isManuallyChanged": None,
    "schemaVersion": "2022.8.16",
    "systemName": None,
    "slug": None,
    "field_id": None,
}

TEMPLATE_MINIMAL_CONFIG = {
    "name": "pw_scf.in",
    "content": "&CONTROL\n  calculation='scf'\n/",
}

TEMPLATE_FULL_CONFIG = {
    "name": "pw_scf.in",
    "content": "&CONTROL\n  calculation='scf'\n/",
    "rendered": "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
    "applicationName": "espresso",
    "applicationVersion": "7.2",
    "executableName": "pw.x",
    "contextProviders": [ContextProvider(name=Name.KGridFormDataManager)],
    "isManuallyChanged": True,
    "schemaVersion": "1.0.0",
}

TEMPLATE_WITH_RENDERED_CONFIG = {
    "name": "test.in",
    "content": "original content",
    "rendered": "rendered content",
}

TEMPLATE_WITHOUT_RENDERED_CONFIG = {
    "name": "test.in",
    "content": "original content",
}

TEMPLATE_TO_DICT_CONFIG = {
    "name": "pw_scf.in",
    "content": "&CONTROL\n/",
    "applicationName": "espresso",
}

TEMPLATE_FROM_DICT_CONFIG = {
    "name": "pw_scf.in",
    "content": "&CONTROL\n/",
    "applicationName": "espresso",
    "executableName": "pw.x",
    "contextProviders": [{"name": Name.KGridFormDataManager}],
}

TEMPLATE_WITH_EXTRA_FIELDS_CONFIG = {
    "name": "test.in",
    "content": "content",
    "custom_field": "custom_value",
}

TEMPLATE_SET_CONTENT_CONFIG = {
    "name": "test.in",
    "content": "original",
}

TEMPLATE_WITH_JINJA_CONFIG = {
    "name": "test.in",
    "content": "Hello {{ name }}!",
}

TEMPLATE_MANUALLY_CHANGED_CONFIG = {
    "name": "test.in",
    "content": "Hello {{ name }}!",
    "isManuallyChanged": True,
}

TEMPLATE_WITH_PROVIDER_RENDERING_CONFIG = {
    "name": "test.in",
    "content": "Value is {{ KGridFormDataManager.value }}",
    "contextProviders": [ContextProvider(name=Name.KGridFormDataManager, data={"value": 42}, isEdited=True)],
}

TEMPLATE_WITH_TWO_PROVIDERS_CONFIG = {
    "name": "test.in",
    "content": "content",
    "contextProviders": [
        ContextProvider(name=Name.KGridFormDataManager, domain="test"),
        ContextProvider(name=Name.KPathFormDataManager, domain="test"),
    ],
}

TEMPLATE_FOR_EXTERNAL_CONTEXT_CONFIG = {
    "name": "test_template.in",
    "content": "kpath: {{ KPathFormDataManager.key }}",
}

EXTERNAL_CONTEXT_FOR_RENDERING = {
    "KPathFormDataManager": {"key": "external_value"},
    "isKPathFormDataManagerEdited": True,
}


def test_template_creation():
    config = TEMPLATE_MINIMAL_CONFIG
    template = Template(**config)
    expected = {
        **config,
        **TEMPLATE_DEFAULT_FIELDS,
    }
    assertion.assert_deep_almost_equal(expected, template.to_dict())


def test_template_with_all_fields():
    config = TEMPLATE_FULL_CONFIG
    template = Template(**config)
    expected = {
        **TEMPLATE_DEFAULT_FIELDS,
        "name": "pw_scf.in",
        "content": "&CONTROL\n  calculation='scf'\n/",
        "rendered": "&CONTROL\n  calculation='scf'\n  prefix='pwscf'\n/",
        "applicationName": "espresso",
        "applicationVersion": "7.2",
        "executableName": "pw.x",
        "contextProviders": [{
            "name": Name.KGridFormDataManager,
            **CONTEXT_PROVIDER_DEFAULT_FIELDS,
        }],
        "isManuallyChanged": True,
        "schemaVersion": "1.0.0",
    }
    assertion.assert_deep_almost_equal(expected, template.to_dict())


def test_get_rendered():
    config_with_rendered = TEMPLATE_WITH_RENDERED_CONFIG
    template_with_rendered = Template(**config_with_rendered)
    assert template_with_rendered.get_rendered() == "rendered content"

    config_without_rendered = TEMPLATE_WITHOUT_RENDERED_CONFIG
    template_without_rendered = Template(**config_without_rendered)
    assert template_without_rendered.get_rendered() == "original content"


def test_template_to_dict():
    config = TEMPLATE_TO_DICT_CONFIG
    template = Template(**config)
    expected = {
        **TEMPLATE_DEFAULT_FIELDS,
        **config,
    }
    assertion.assert_deep_almost_equal(expected, template.to_dict())


def test_template_from_dict():
    config = TEMPLATE_FROM_DICT_CONFIG
    template = Template(**config)
    expected = {
        **TEMPLATE_DEFAULT_FIELDS,
        "name": "pw_scf.in",
        "content": "&CONTROL\n/",
        "applicationName": "espresso",
        "executableName": "pw.x",
        "contextProviders": [{
            "name": Name.KGridFormDataManager,
            **CONTEXT_PROVIDER_DEFAULT_FIELDS,
        }],
    }
    assertion.assert_deep_almost_equal(expected, template.to_dict())


def test_template_validation():
    with pytest.raises(Exception):
        Template()

    with pytest.raises(Exception):
        Template(name="test.in")

    with pytest.raises(Exception):
        Template(content="content")


def test_set_content():
    config = TEMPLATE_SET_CONTENT_CONFIG
    template = Template(**config)
    template.set_content("new content")
    assert template.content == "new content"


def test_set_rendered():
    config = TEMPLATE_SET_CONTENT_CONFIG
    template = Template(**config)
    template.set_rendered("rendered")
    assert template.rendered == "rendered"


def test_add_context_provider():
    config = TEMPLATE_WITHOUT_RENDERED_CONFIG
    template = Template(**config)
    provider = ContextProvider(name=Name.KGridFormDataManager)
    template.add_context_provider(provider)
    assert len(template.contextProviders) == 1
    assert template.contextProviders[0].name == Name.KGridFormDataManager


def test_remove_context_provider():
    config = TEMPLATE_WITH_TWO_PROVIDERS_CONFIG
    template = Template(**config)
    provider1 = config["contextProviders"][0]
    template.remove_context_provider(provider1)
    assert len(template.contextProviders) == 1
    assert template.contextProviders[0].name == Name.KPathFormDataManager


def test_render():
    config = TEMPLATE_WITH_JINJA_CONFIG
    template = Template(**config)
    template.render({"name": "World"})
    assert template.rendered == "Hello World!"


def test_render_with_context_provider():
    config = TEMPLATE_WITH_PROVIDER_RENDERING_CONFIG
    template = Template(**config)
    template.render()
    assert "42" in template.rendered or "value" in template.rendered


def test_render_manually_changed():
    config = TEMPLATE_MANUALLY_CHANGED_CONFIG
    template = Template(**config)
    template.render({"name": "World"})
    assert template.rendered is None


def test_get_rendered_json():
    config = TEMPLATE_WITH_JINJA_CONFIG
    template = Template(**config)
    result = template.get_rendered_json({"name": "World"})
    expected_subset = {
        "name": "test.in",
        "content": "Hello {{ name }}!",
        "rendered": "Hello World!",
        "schemaVersion": "2022.8.16"
    }
    for key, value in expected_subset.items():
        assertion.assert_deep_almost_equal(value, result[key])


def test_render_with_external_context_and_provider():
    provider = ContextProvider(
        name=Name.KPathFormDataManager,
        data={"default": "value"}
    )
    template = Template(**TEMPLATE_FOR_EXTERNAL_CONTEXT_CONFIG)
    template.add_context_provider(provider)
    external_context = EXTERNAL_CONTEXT_FOR_RENDERING
    template.render(external_context)
    expected_rendered = "kpath: external_value"
    assertion.assert_deep_almost_equal(expected_rendered, template.get_rendered())


def test_template_with_extra_fields():
    config = TEMPLATE_WITH_EXTRA_FIELDS_CONFIG
    template = Template(**config)
    assert template.name == "test.in"
    assert not hasattr(template, "custom_field")
