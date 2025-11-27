from typing import List

from mat3ra.esse.models.software.template import TemplateSchema
from pydantic import Field

from .context.context_provider import ContextProvider


class Template(TemplateSchema):
    """
    Template class representing a template for application input files.

    Attributes:
        name: Input file name (required)
        content: Content of the input file (required)
        rendered: Rendered content of the input file
        applicationName: Name of the application this template belongs to
        applicationVersion: Version of the application this template belongs to
        executableName: Name of the executable this template belongs to
        contextProviders: List of context providers for this template
        isManuallyChanged: Whether the template has been manually changed
        schemaVersion: Entity's schema version
    """

    context_providers: List[ContextProvider] = Field(
        default_factory=list, description="List of context providers for this template"
    )

    def get_rendered(self) -> str:
        return self.rendered if self.rendered is not None else self.content

