from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.layout_node import LayoutNode


T = TypeVar("T", bound="LayoutInterpretationResponse")


@_attrs_define
class LayoutInterpretationResponse:
    """
    Example:
        {'structured': {'type': 'VStack', 'children': [{'type': 'Text', 'text': 'Hello'}]}, 'description': 'Simple
            VStack with Hello text', 'version': 'layout-v1'}

    Attributes:
        structured (LayoutNode):  Example: {'type': 'VStack', 'children': [{'type': 'Text', 'text': 'Hello'}]}.
        description (Union[Unset, str]): Optional natural language summary
        version (Union[Unset, str]):  Example: layout-v1.
        log (Union[Unset, str]): Raw communication log between the service and OpenAI
    """

    structured: "LayoutNode"
    description: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    log: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        structured = self.structured.to_dict()

        description = self.description

        version = self.version

        log = self.log

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "structured": structured,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if version is not UNSET:
            field_dict["version"] = version
        if log is not UNSET:
            field_dict["log"] = log

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.layout_node import LayoutNode

        d = dict(src_dict)
        structured = LayoutNode.from_dict(d.pop("structured"))

        description = d.pop("description", UNSET)

        version = d.pop("version", UNSET)

        log = d.pop("log", UNSET)

        layout_interpretation_response = cls(
            structured=structured,
            description=description,
            version=version,
            log=log,
        )

        layout_interpretation_response.additional_properties = d
        return layout_interpretation_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
