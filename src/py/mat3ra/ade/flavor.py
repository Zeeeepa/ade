"""Flavor class definition."""

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FlavorInput(BaseModel):
    """Input template reference for a flavor."""

    template_id: Optional[str] = Field(default=None, description="Template ID")
    template_name: Optional[str] = Field(default=None, description="Template name")
    name: Optional[str] = Field(
        default=None, description="Name of the resulting input file, if different than template name"
    )


class Flavor(BaseModel):
    """
    Flavor class representing a flavor of an executable.

    Attributes:
        name: Flavor name (required)
        executable_id: ID of the executable this flavor belongs to
        executable_name: Name of the executable this flavor belongs to
        application_name: Name of the application this flavor belongs to
        input: List of input templates for this flavor
        supported_application_versions: List of application versions this flavor supports
        disable_render_materials: Whether to disable rendering materials
        is_default: Identifies that entity is defaultable
        schema_version: Entity's schema version
        pre_processors: Names of the pre-processors for this calculation
        post_processors: Names of the post-processors for this calculation
        monitors: Names of the monitors for this calculation
        results: Names of the results for this calculation
    """

    name: str = Field(..., description="Flavor name")
    executable_id: Optional[str] = Field(default="", description="ID of the executable this flavor belongs to")
    executable_name: Optional[str] = Field(default="", description="Name of the executable this flavor belongs to")
    application_name: Optional[str] = Field(default="", description="Name of the application this flavor belongs to")
    input: List[FlavorInput] = Field(default_factory=list, description="Input templates for this flavor")
    supported_application_versions: Optional[List[str]] = Field(
        default=None, description="List of application versions this flavor supports"
    )
    disable_render_materials: bool = Field(default=False, description="Whether to disable rendering materials")
    is_default: Optional[bool] = Field(default=None, description="Identifies that entity is defaultable")
    schema_version: Optional[str] = Field(
        default=None, description="Entity's schema version. Used to distinct between different schemas"
    )
    pre_processors: List[Any] = Field(
        default_factory=list, description="Names of the pre-processors for this calculation"
    )
    post_processors: List[Any] = Field(
        default_factory=list, description="Names of the post-processors for this calculation"
    )
    monitors: List[Any] = Field(default_factory=list, description="Names of the monitors for this calculation")
    results: List[Any] = Field(default_factory=list, description="Names of the results for this calculation")

    model_config = ConfigDict(validate_assignment=True, extra="allow")
