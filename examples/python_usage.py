"""
Example usage of the mat3ra-ade Python package.

This example demonstrates how to create and use Application, Executable, Flavor, and Template objects.
"""

from mat3ra.ade import Application, ContextProvider, Executable, Flavor, FlavorInput, Template


def main():
    """Demonstrate basic usage of the ade package."""
    print("Creating an Application...")
    app = Application(
        name="espresso",
        version="7.2",
        build="standard",
        short_name="QE",
        summary="Quantum ESPRESSO - integrated suite for electronic-structure calculations",
        has_advanced_compute_options=True,
    )
    print(f"Application: {app.name} ({app.get_short_name()}) v{app.version}")
    print(f"Uses material: {app.is_using_material}")

    print("\nCreating an Executable...")
    executable = Executable(
        name="pw.x",
        application_id=[app.name],
        is_default=True,
        monitors=[{"name": "convergence"}],
        results=[{"name": "total_energy"}, {"name": "band_gap"}],
    )
    print(f"Executable: {executable.name}")
    print(f"Results: {len(executable.results)} configured")

    print("\nCreating a Template...")
    template = Template(
        name="pw_scf.in",
        content="""&CONTROL
  calculation='scf'
  restart_mode='from_scratch'
  prefix='pwscf'
/""",
        application_name=app.name,
        executable_name=executable.name,
        context_providers=[ContextProvider(name="material")],
    )
    print(f"Template: {template.name}")
    print(f"Context providers: {len(template.context_providers)}")

    print("\nCreating a Flavor...")
    flavor = Flavor(
        name="scf",
        executable_name=executable.name,
        application_name=app.name,
        input=[FlavorInput(template_name=template.name, name="pw_scf.in")],
        supported_application_versions=["7.0", "7.1", "7.2"],
        is_default=True,
    )
    print(f"Flavor: {flavor.name}")
    print(f"Supports versions: {', '.join(flavor.supported_application_versions)}")

    print("\nSerializing to JSON...")
    print(f"Application: {app.model_dump_json(indent=2, exclude_unset=True)}")

    print("\nDone!")


if __name__ == "__main__":
    main()
