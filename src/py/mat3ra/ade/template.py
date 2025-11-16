"""Template class definition."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ContextProvider(BaseModel):
    """Context provider for a template."""

    name: str = Field(..., description="The name of this item. e.g. scf_accuracy")


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
