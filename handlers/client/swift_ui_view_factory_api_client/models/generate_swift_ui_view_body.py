from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.generate_swift_ui_view_body_style import GenerateSwiftUIViewBodyStyle
    from ..models.layout_node import LayoutNode


T = TypeVar("T", bound="GenerateSwiftUIViewBody")


@_attrs_define
class GenerateSwiftUIViewBody:
    """
    Attributes:
        layout (Union[Unset, LayoutNode]):  Example: {'type': 'VStack', 'children': [{'type': 'Text', 'text':
            'Hello'}]}.
        name (Union[Unset, str]): Optional name for the generated SwiftUI view (e.g., HomeView)
        style (Union[Unset, GenerateSwiftUIViewBodyStyle]):
        backend_hooks (Union[Unset, bool]): If true, the generated SwiftUI view includes an `.onAppear`
            block where analytics or network logic can be invoked.
             Default: False.
    """

    layout: Union[Unset, "LayoutNode"] = UNSET
    name: Union[Unset, str] = UNSET
    style: Union[Unset, "GenerateSwiftUIViewBodyStyle"] = UNSET
    backend_hooks: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        layout: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.layout, Unset):
            layout = self.layout.to_dict()

        name = self.name

        style: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.to_dict()

        backend_hooks = self.backend_hooks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if layout is not UNSET:
            field_dict["layout"] = layout
        if name is not UNSET:
            field_dict["name"] = name
        if style is not UNSET:
            field_dict["style"] = style
        if backend_hooks is not UNSET:
            field_dict["backend_hooks"] = backend_hooks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.generate_swift_ui_view_body_style import GenerateSwiftUIViewBodyStyle
        from ..models.layout_node import LayoutNode

        d = dict(src_dict)
        _layout = d.pop("layout", UNSET)
        layout: Union[Unset, LayoutNode]
        if isinstance(_layout, Unset):
            layout = UNSET
        else:
            layout = LayoutNode.from_dict(_layout)

        name = d.pop("name", UNSET)

        _style = d.pop("style", UNSET)
        style: Union[Unset, GenerateSwiftUIViewBodyStyle]
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = GenerateSwiftUIViewBodyStyle.from_dict(_style)

        backend_hooks = d.pop("backend_hooks", UNSET)

        generate_swift_ui_view_body = cls(
            layout=layout,
            name=name,
            style=style,
            backend_hooks=backend_hooks,
        )

        generate_swift_ui_view_body.additional_properties = d
        return generate_swift_ui_view_body

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
