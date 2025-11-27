from mat3ra.esse.models.context_provider import ContextProviderSchema

class ContextProvider(ContextProviderSchema):
    """
    Context provider for a template.

    - user edits the corresponding property, eg. "kpath"
    - isKpathEdited is set to True
    - context property is updated for the parent entity (eg. Unit) in a way that persists in Redux state
    - new entity inherits the "data" through "context" field in config
    - extraData field is used to store any other data that should be passed from one instance of provider
      to next one, for example data about material to track when it is changed.

    Attributes:
        name: The name of this item (required)
        domain: Domain of the context provider
        entityName: Entity name associated with the context provider
        data: Data object for the context provider
        extraData: Additional data object for the context provider
        isEdited: Flag indicating if the context provider has been edited
        context: Context object for the context provider
    """

    @property
    def extra_data_key(self) -> str:
        return f"{self.name}ExtraData"

    @property
    def is_edited_key(self) -> str:
        return f"is{str(self.name).capitalize()}Edited"

    @property
    def is_unit_context_provider(self) -> bool:
        return self.entity_name == "unit"

    @property
    def is_subworkflow_context_provider(self) -> bool:
        return self.entity_name == "subworkflow"

