"""Executable class definition."""

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class NamedItem(BaseModel):
    """Named item for pre/post processors, monitors, and results."""

    name: str


class Executable(BaseModel):
    """
    Executable class representing an executable of an application.

    Attributes:
        name: The name of the executable (required)
        application_id: IDs of the application this executable belongs to
        has_advanced_compute_options: Whether advanced compute options are present
        is_default: Identifies that entity is defaultable
        schema_version: Entity's schema version
        pre_processors: Names of the pre-processors for this calculation
        post_processors: Names of the post-processors for this calculation
        monitors: Names of the monitors for this calculation
        results: Names of the results for this calculation
    """

    name: str = Field(..., description="The name of the executable. e.g. pw.x")
    application_id: List[str] = Field(
        default_factory=list, description="IDs of the application this executable belongs to"
    )
    has_advanced_compute_options: Optional[bool] = Field(
        default=None, description="Whether advanced compute options are present"
    )
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
