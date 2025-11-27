from typing import List, Optional

from mat3ra.esse.models.software.flavor import FlavorSchema, \
    ExecutionUnitInputIdItemSchemaForPhysicsBasedSimulationEngines
from pydantic import Field


class FlavorInput(ExecutionUnitInputIdItemSchemaForPhysicsBasedSimulationEngines):
    """Input template reference for a flavor."""

    template_id: Optional[str] = Field(default=None, description="Template ID")
    template_name: Optional[str] = Field(default=None, description="Template name")
    name: Optional[str] = Field(
        default=None, description="Name of the resulting input file, if different than template name"
    )


class Flavor(FlavorSchema):
    """
    Flavor class representing a flavor of an executable.

    Attributes:
        name: Flavor name (required)
        executableId: ID of the executable this flavor belongs to
        executableName: Name of the executable this flavor belongs to
        applicationName: Name of the application this flavor belongs to
        input: List of input templates for this flavor
        supportedApplicationVersions: List of application versions this flavor supports
        disableRenderMaterials: Whether to disable rendering materials
        isDefault: Identifies that entity is defaultable
        schemaVersion: Entity's schema version
        preProcessors: Names of the pre-processors for this calculation
        postProcessors: Names of the post-processors for this calculation
        monitors: Names of the monitors for this calculation
        results: Names of the results for this calculation
    """

    input: List[FlavorInput] = Field(default_factory=list, description="Input templates for this flavor")
