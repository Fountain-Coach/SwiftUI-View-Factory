from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.layout_node_type import LayoutNodeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LayoutNode")


@_attrs_define
class LayoutNode:
    """
    Example:
        {'type': 'VStack', 'children': [{'type': 'Text', 'text': 'Hello'}]}

    Attributes:
        type_ (LayoutNodeType): SwiftUI component type
        id (Union[Unset, str]): A unique node identifier
        role (Union[None, Unset, str]): Semantic role (e.g., "header", "submit")
        tag (Union[None, Unset, str]): Developer hint or custom logic
        text (Union[None, Unset, str]):
        children (Union[None, Unset, list['LayoutNode']]): Child layout nodes rendered inside container views. Multiple
            entries are typically used for ``VStack``, ``HStack``, ``ZStack``, ``Form`` or ``NavigationStack`` groups.
        condition (Union[None, Unset, str]): Condition expression controlling the branch
        then (Union[Unset, LayoutNode]):  Example: {'type': 'VStack', 'children': [{'type': 'Text', 'text': 'Hello'}]}.
        else_ (Union[Unset, LayoutNode]):  Example: {'type': 'VStack', 'children': [{'type': 'Text', 'text': 'Hello'}]}.
    """

    type_: LayoutNodeType
    id: Union[Unset, str] = UNSET
    role: Union[None, Unset, str] = UNSET
    tag: Union[None, Unset, str] = UNSET
    text: Union[None, Unset, str] = UNSET
    children: Union[None, Unset, list["LayoutNode"]] = UNSET
    condition: Union[None, Unset, str] = UNSET
    then: Union[Unset, "LayoutNode"] = UNSET
    else_: Union[Unset, "LayoutNode"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        id = self.id

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        tag: Union[None, Unset, str]
        if isinstance(self.tag, Unset):
            tag = UNSET
        else:
            tag = self.tag

        text: Union[None, Unset, str]
        if isinstance(self.text, Unset):
            text = UNSET
        else:
            text = self.text

        children: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.children, Unset):
            children = UNSET
        elif isinstance(self.children, list):
            children = []
            for children_type_0_item_data in self.children:
                children_type_0_item = children_type_0_item_data.to_dict()
                children.append(children_type_0_item)

        else:
            children = self.children

        condition: Union[None, Unset, str]
        if isinstance(self.condition, Unset):
            condition = UNSET
        else:
            condition = self.condition

        then: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.then, Unset):
            then = self.then.to_dict()

        else_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.else_, Unset):
            else_ = self.else_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if role is not UNSET:
            field_dict["role"] = role
        if tag is not UNSET:
            field_dict["tag"] = tag
        if text is not UNSET:
            field_dict["text"] = text
        if children is not UNSET:
            field_dict["children"] = children
        if condition is not UNSET:
            field_dict["condition"] = condition
        if then is not UNSET:
            field_dict["then"] = then
        if else_ is not UNSET:
            field_dict["else"] = else_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = LayoutNodeType(d.pop("type"))

        id = d.pop("id", UNSET)

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_tag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tag = _parse_tag(d.pop("tag", UNSET))

        def _parse_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text = _parse_text(d.pop("text", UNSET))

        def _parse_children(data: object) -> Union[None, Unset, list["LayoutNode"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                children_type_0 = []
                _children_type_0 = data
                for children_type_0_item_data in _children_type_0:
                    children_type_0_item = LayoutNode.from_dict(children_type_0_item_data)

                    children_type_0.append(children_type_0_item)

                return children_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["LayoutNode"]], data)

        children = _parse_children(d.pop("children", UNSET))

        def _parse_condition(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        condition = _parse_condition(d.pop("condition", UNSET))

        _then = d.pop("then", UNSET)
        then: Union[Unset, LayoutNode]
        if isinstance(_then, Unset):
            then = UNSET
        else:
            then = LayoutNode.from_dict(_then)

        _else_ = d.pop("else", UNSET)
        else_: Union[Unset, LayoutNode]
        if isinstance(_else_, Unset):
            else_ = UNSET
        else:
            else_ = LayoutNode.from_dict(_else_)

        layout_node = cls(
            type_=type_,
            id=id,
            role=role,
            tag=tag,
            text=text,
            children=children,
            condition=condition,
            then=then,
            else_=else_,
        )

        layout_node.additional_properties = d
        return layout_node

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
