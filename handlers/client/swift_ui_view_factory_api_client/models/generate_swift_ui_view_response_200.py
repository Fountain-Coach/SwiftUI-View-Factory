from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateSwiftUIViewResponse200")


@_attrs_define
class GenerateSwiftUIViewResponse200:
    """
    Attributes:
        swift (Union[Unset, str]):  Example: struct GeneratedView: View {
                var body: some View {
                    Text("Hello")
                }
            }
            .
    """

    swift: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        swift = self.swift

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if swift is not UNSET:
            field_dict["swift"] = swift

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        swift = d.pop("swift", UNSET)

        generate_swift_ui_view_response_200 = cls(
            swift=swift,
        )

        generate_swift_ui_view_response_200.additional_properties = d
        return generate_swift_ui_view_response_200

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
