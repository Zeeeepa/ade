from typing import Any, Dict, Optional

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
    def name_str(self) -> str:
        return self.name.value if hasattr(self.name, 'value') else str(self.name)

    @property
    def extra_data_key(self) -> str:
        return f"{self.name_str}ExtraData"

    @property
    def is_edited_key(self) -> str:
        return f"is{self.name_str}Edited"

    @property
    def is_unit_context_provider(self) -> bool:
        return self.entityName == "unit"

    @property
    def is_subworkflow_context_provider(self) -> bool:
        return self.entityName == "subworkflow"

    def _get_data_from_context(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not context:
            return {}
        data = context.get(self.name_str)
        is_edited = context.get(self.is_edited_key)
        extra_data = context.get(self.extra_data_key)
        result = {}
        if data is not None:
            result["data"] = data
        if is_edited is not None:
            result["isEdited"] = is_edited
        if extra_data is not None:
            result["extraData"] = extra_data
        return result

    def _get_effective_data(self, context: Optional[Dict[str, Any]] = None) -> Any:
        context_data = self._get_data_from_context(context or self.context)
        return context_data.get("data", self.data)

    def _get_effective_is_edited(self, context: Optional[Dict[str, Any]] = None) -> bool:
        context_data = self._get_data_from_context(context or self.context)
        return context_data.get("isEdited", self.isEdited)

    def _get_effective_extra_data(self, context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        context_data = self._get_data_from_context(context or self.context)
        return context_data.get("extraData", self.extraData)

    def yield_data(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = self._get_effective_data(context)
        is_edited = self._get_effective_is_edited(context)
        extra_data = self._get_effective_extra_data(context)
        result = {
            self.name_str: data,
            self.is_edited_key: is_edited,
        }
        if extra_data:
            result[self.extra_data_key] = extra_data
        return result

    def yield_data_for_rendering(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.yield_data(context)

