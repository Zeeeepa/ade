"""Template class definition."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ContextProviderName(str, Enum):
    """Enum for context provider names matching ESSE schema."""

    PlanewaveCutoffDataManager = "PlanewaveCutoffDataManager"
    KGridFormDataManager = "KGridFormDataManager"
    QGridFormDataManager = "QGridFormDataManager"
    IGridFormDataManager = "IGridFormDataManager"
    QPathFormDataManager = "QPathFormDataManager"
    IPathFormDataManager = "IPathFormDataManager"
    KPathFormDataManager = "KPathFormDataManager"
    ExplicitKPathFormDataManager = "ExplicitKPathFormDataManager"
    ExplicitKPath2PIBAFormDataManager = "ExplicitKPath2PIBAFormDataManager"
    HubbardJContextManager = "HubbardJContextManager"
    HubbardUContextManager = "HubbardUContextManager"
    HubbardVContextManager = "HubbardVContextManager"
    HubbardContextManagerLegacy = "HubbardContextManagerLegacy"
    NEBFormDataManager = "NEBFormDataManager"
    BoundaryConditionsFormDataManager = "BoundaryConditionsFormDataManager"
    MLSettingsDataManager = "MLSettingsDataManager"
    MLTrainTestSplitDataManager = "MLTrainTestSplitDataManager"
    IonDynamicsContextProvider = "IonDynamicsContextProvider"
    CollinearMagnetizationDataManager = "CollinearMagnetizationDataManager"
    NonCollinearMagnetizationDataManager = "NonCollinearMagnetizationDataManager"
    QEPWXInputDataManager = "QEPWXInputDataManager"
    QENEBInputDataManager = "QENEBInputDataManager"
    VASPInputDataManager = "VASPInputDataManager"
    VASPNEBInputDataManager = "VASPNEBInputDataManager"
    NWChemInputDataManager = "NWChemInputDataManager"


class ContextProvider(BaseModel):
    """
    Context provider for a template.

    This is a standalone class that contains "data" for a property with "name".
    Helps facilitate UI logic. Can be initialized from context when user edits are present:
    - user edits the corresponding property, eg. "kpath"
    - isKpathEdited is set to True
    - context property is updated for the parent entity (eg. Unit) in a way that persists in Redux state
    - new entity inherits the "data" through "context" field in config
    - extraData field is used to store any other data that should be passed from one instance of provider
      to next one, for example data about material to track when it is changed.

    Attributes:
        name: The name of this item (required)
        domain: Domain of the context provider
        entity_name: Entity name associated with the context provider
        data: Data object for the context provider
        extra_data: Additional data object for the context provider
        is_edited: Flag indicating if the context provider has been edited
        context: Context object for the context provider
    """

    name: str = Field(..., description="The name of this item. e.g. scf_accuracy")
    domain: Optional[str] = Field(default="default", description="Domain of the context provider")
    entity_name: Optional[str] = Field(
        default="unit", description="Entity name associated with the context provider, eg. 'unit', 'subworkflow'"
    )
    data: Optional[Dict[str, Any]] = Field(default=None, description="Data object for the context provider")
    extra_data: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional data object for the context provider"
    )
    is_edited: Optional[bool] = Field(
        default=None, description="Flag indicating if the context provider has been edited"
    )
    context: Optional[Dict[str, Any]] = Field(default=None, description="Context object for the context provider")

    model_config = ConfigDict(validate_assignment=True, extra="allow")

    @property
    def extra_data_key(self) -> str:
        """Get the key for extra data."""
        return f"{self.name}ExtraData"

    @property
    def is_edited_key(self) -> str:
        """Get the key for isEdited flag."""
        return f"is{self.name.capitalize()}Edited"

    @property
    def is_unit_context_provider(self) -> bool:
        """Check if this is a unit context provider."""
        return self.entity_name == "unit"

    @property
    def is_subworkflow_context_provider(self) -> bool:
        """Check if this is a subworkflow context provider."""
        return self.entity_name == "subworkflow"


class JinjaContextProvider(ContextProvider):
    """
    Context provider with Jinja variable support.

    Extends ContextProvider with isUsingJinjaVariables flag.
    """

    is_using_jinja_variables: bool = Field(
        default=False, description="Whether this provider uses Jinja variables"
    )


class JSONSchemaDataProvider(JinjaContextProvider):
    """
    Provides jsonSchema only.

    Extends JinjaContextProvider with jsonSchema property.
    """

    json_schema: Optional[Dict[str, Any]] = Field(default=None, description="JSON schema for this provider")


class JSONSchemaFormDataProvider(JSONSchemaDataProvider):
    """
    Provides jsonSchema and uiSchema for generating react-jsonschema-form.

    See https://github.com/mozilla-services/react-jsonschema-form for Form UI.
    """

    ui_schema: Optional[Dict[str, Any]] = Field(default=None, description="UI schema for form rendering")
    fields: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom fields")
    default_field_styles: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Default styles for form fields"
    )


class Template(BaseModel):
    """
    Template class representing a template for application input files.

    Attributes:
        name: Input file name (required)
        content: Content of the input file (required)
        rendered: Rendered content of the input file
        application_name: Name of the application this template belongs to
        application_version: Version of the application this template belongs to
        executable_name: Name of the executable this template belongs to
        context_providers: List of context providers for this template
        is_manually_changed: Whether the template has been manually changed
        schema_version: Entity's schema version
    """

    name: str = Field(..., description="Input file name. e.g. pw_scf.in")
    content: str = Field(..., description="Content of the input file. e.g. &CONTROL    calculation='scf' ...")
    rendered: Optional[str] = Field(
        default=None, description="Rendered content of the input file. e.g. &CONTROL    calculation='scf' ..."
    )
    application_name: Optional[str] = Field(default=None, description="Name of the application")
    application_version: Optional[str] = Field(default=None, description="Version of the application")
    executable_name: Optional[str] = Field(default=None, description="Name of the executable")
    context_providers: List[ContextProvider] = Field(
        default_factory=list, description="List of context providers for this template"
    )
    is_manually_changed: bool = Field(default=False, description="Whether the template has been manually changed")
    schema_version: Optional[str] = Field(
        default=None, description="Entity's schema version. Used to distinct between different schemas"
    )

    def get_rendered(self) -> str:
        """Get rendered content, defaulting to content if not set."""
        return self.rendered if self.rendered is not None else self.content

    model_config = ConfigDict(validate_assignment=True, extra="allow")
