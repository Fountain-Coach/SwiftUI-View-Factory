from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateSwiftUIViewBodyStyle")


@_attrs_define
class GenerateSwiftUIViewBodyStyle:
    """
    Attributes:
        indent (Union[Unset, int]):  Default: 2.
        header_comment (Union[Unset, bool]):  Default: True.
        font (Union[Unset, str]): Font applied to Text and Button views
        color (Union[Unset, str]): Foreground color name
        spacing (Union[Unset, int]): Spacing value for stacks
        bold (Union[Unset, bool]): Apply bold styling to Text and Button views
        italic (Union[Unset, bool]): Apply italic styling to Text and Button views
        padding (Union[Unset, int]): Padding value applied to leaf views
        background_color (Union[Unset, str]): Background color name
        corner_radius (Union[Unset, int]): Corner radius for leaf views
    """

    indent: Union[Unset, int] = 2
    header_comment: Union[Unset, bool] = True
    font: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    spacing: Union[Unset, int] = UNSET
    bold: Union[Unset, bool] = UNSET
    italic: Union[Unset, bool] = UNSET
    padding: Union[Unset, int] = UNSET
    background_color: Union[Unset, str] = UNSET
    corner_radius: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        indent = self.indent

        header_comment = self.header_comment

        font = self.font

        color = self.color

        spacing = self.spacing

        bold = self.bold

        italic = self.italic

        padding = self.padding

        background_color = self.background_color

        corner_radius = self.corner_radius

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if indent is not UNSET:
            field_dict["indent"] = indent
        if header_comment is not UNSET:
            field_dict["header_comment"] = header_comment
        if font is not UNSET:
            field_dict["font"] = font
        if color is not UNSET:
            field_dict["color"] = color
        if spacing is not UNSET:
            field_dict["spacing"] = spacing
        if bold is not UNSET:
            field_dict["bold"] = bold
        if italic is not UNSET:
            field_dict["italic"] = italic
        if padding is not UNSET:
            field_dict["padding"] = padding
        if background_color is not UNSET:
            field_dict["background_color"] = background_color
        if corner_radius is not UNSET:
            field_dict["corner_radius"] = corner_radius

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        indent = d.pop("indent", UNSET)

        header_comment = d.pop("header_comment", UNSET)

        font = d.pop("font", UNSET)

        color = d.pop("color", UNSET)

        spacing = d.pop("spacing", UNSET)

        bold = d.pop("bold", UNSET)

        italic = d.pop("italic", UNSET)

        padding = d.pop("padding", UNSET)

        background_color = d.pop("background_color", UNSET)

        corner_radius = d.pop("corner_radius", UNSET)

        generate_swift_ui_view_body_style = cls(
            indent=indent,
            header_comment=header_comment,
            font=font,
            color=color,
            spacing=spacing,
            bold=bold,
            italic=italic,
            padding=padding,
            background_color=background_color,
            corner_radius=corner_radius,
        )

        generate_swift_ui_view_body_style.additional_properties = d
        return generate_swift_ui_view_body_style

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
