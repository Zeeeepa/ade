from mat3ra.esse.models.software.application import ApplicationSchemaBase
from pydantic import ConfigDict


class Application(ApplicationSchemaBase):
    """
    Application class representing a software application.

    Attributes:
        name: Application name (required)
        version: Application version
        build: Application build
        shortName: Short name of the application
        summary: Application's short description
        hasAdvancedComputeOptions: Whether advanced compute options are present
        isLicensed: Whether licensing is present
        isDefault: Identifies that entity is defaultable
        schemaVersion: Entity's schema version
    """

    @property
    def is_using_material(self) -> bool:
        material_using_applications = ["vasp", "nwchem", "espresso"]
        return self.name in material_using_applications

    def get_short_name(self) -> str:
        return self.shortName if self.shortName else self.name

    model_config = ConfigDict(validate_assignment=True, extra="allow")
