"""Application class definition."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Application(BaseModel):
    """
    Application class representing a software application.

    Attributes:
        name: Application name (required)
        version: Application version
        build: Application build
        short_name: Short name of the application
        summary: Application's short description
        has_advanced_compute_options: Whether advanced compute options are present
        is_licensed: Whether licensing is present
        is_default: Identifies that entity is defaultable
        schema_version: Entity's schema version
    """

    name: str = Field(..., description="Application name")
    version: Optional[str] = Field(default="", description="Application version. e.g. 5.3.5")
    build: Optional[str] = Field(default=None, description="Application build. e.g. VTST")
    short_name: Optional[str] = Field(default=None, description="The short name of the application. e.g. qe")
    summary: Optional[str] = Field(default=None, description="Application's short description")
    has_advanced_compute_options: bool = Field(
        default=False, description="Whether advanced compute options are present"
    )
    is_licensed: bool = Field(default=False, description="Whether licensing is present")
    is_default: Optional[bool] = Field(default=None, description="Identifies that entity is defaultable")
    schema_version: Optional[str] = Field(
        default=None, description="Entity's schema version. Used to distinct between different schemas"
    )

    @property
    def is_using_material(self) -> bool:
        """Check if the application uses material."""
        material_using_applications = ["vasp", "nwchem", "espresso"]
        return self.name in material_using_applications

    def get_short_name(self) -> str:
        """Get short name, defaulting to name if not set."""
        return self.short_name if self.short_name else self.name

    model_config = ConfigDict(validate_assignment=True, extra="allow")
