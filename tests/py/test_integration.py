"""Integration tests demonstrating usage of all classes together."""

from mat3ra.ade import Application, ContextProvider, Executable, Flavor, FlavorInput, Template


class TestIntegration:
    """Integration tests for the ade Python package."""

    def test_end_to_end_workflow(self):
        """Test creating and using all classes together."""
        # Create an application
        app = Application(
            name="espresso",
            version="7.2",
            build="standard",
            short_name="QE",
            summary="Quantum ESPRESSO",
            has_advanced_compute_options=True,
            is_licensed=False,
        )

        # Verify application properties
        assert app.name == "espresso"
        assert app.get_short_name() == "QE"
        assert app.is_using_material is True

        # Create an executable
        executable = Executable(
            name="pw.x",
            application_id=[app.name],
            is_default=True,
            monitors=[{"name": "convergence"}],
            results=[{"name": "total_energy"}, {"name": "band_gap"}],
        )

        # Verify executable properties
        assert executable.name == "pw.x"
        assert executable.application_id == ["espresso"]
        assert len(executable.results) == 2

        # Create a template
        template = Template(
            name="pw_scf.in",
            content="&CONTROL\n  calculation='scf'\n/",
            application_name=app.name,
            executable_name=executable.name,
            context_providers=[ContextProvider(name="material")],
        )

        # Verify template properties
        assert template.name == "pw_scf.in"
        assert template.get_rendered() == "&CONTROL\n  calculation='scf'\n/"
        assert len(template.context_providers) == 1

        # Create a flavor
        flavor = Flavor(
            name="scf",
            executable_name=executable.name,
            application_name=app.name,
            input=[FlavorInput(template_name=template.name, name="pw_scf.in")],
            supported_application_versions=["7.0", "7.1", "7.2"],
            is_default=True,
        )

        # Verify flavor properties
        assert flavor.name == "scf"
        assert flavor.application_name == app.name
        assert flavor.executable_name == executable.name
        assert len(flavor.input) == 1
        assert flavor.input[0].template_name == template.name

    def test_serialization_workflow(self):
        """Test serialization and deserialization of all classes."""
        # Create instances
        app = Application(name="vasp", version="5.4.4")
        executable = Executable(name="vasp_std", application_id=["vasp"])
        template = Template(name="INCAR", content="SYSTEM = Test")
        flavor = Flavor(
            name="standard",
            application_name="vasp",
            executable_name="vasp_std",
        )

        # Serialize to dict
        app_dict = app.model_dump()
        exe_dict = executable.model_dump()
        tmpl_dict = template.model_dump()
        flv_dict = flavor.model_dump()

        # Verify all are dictionaries
        assert isinstance(app_dict, dict)
        assert isinstance(exe_dict, dict)
        assert isinstance(tmpl_dict, dict)
        assert isinstance(flv_dict, dict)

        # Deserialize from dict
        app_restored = Application(**app_dict)
        exe_restored = Executable(**exe_dict)
        tmpl_restored = Template(**tmpl_dict)
        flv_restored = Flavor(**flv_dict)

        # Verify restored objects
        assert app_restored.name == app.name
        assert exe_restored.name == executable.name
        assert tmpl_restored.name == template.name
        assert flv_restored.name == flavor.name

    def test_import_all_from_package(self):
        """Test that all classes can be imported from the package."""
        from mat3ra.ade import (
            Application,
            ContextProvider,
            Executable,
            Flavor,
            FlavorInput,
            Template,
        )

        # Verify all are importable and are classes
        assert Application is not None
        assert Executable is not None
        assert Flavor is not None
        assert FlavorInput is not None
        assert Template is not None
        assert ContextProvider is not None
