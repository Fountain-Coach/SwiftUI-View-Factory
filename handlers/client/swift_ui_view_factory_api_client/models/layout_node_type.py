from enum import Enum


class LayoutNodeType(str, Enum):
    BUTTON = "Button"
    CONDITIONAL = "Conditional"
    FORM = "Form"
    HSTACK = "HStack"
    IMAGE = "Image"
    LIST = "List"
    NAVIGATIONSTACK = "NavigationStack"
    SCROLLVIEW = "ScrollView"
    SECTION = "Section"
    SPACER = "Spacer"
    TEXT = "Text"
    TEXTFIELD = "TextField"
    VSTACK = "VStack"
    ZSTACK = "ZStack"

    def __str__(self) -> str:
        return str(self.value)
