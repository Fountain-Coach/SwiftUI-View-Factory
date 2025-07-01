# service/codegen.py
from app.models.layout import LayoutNode

def generate_swift(layout: LayoutNode) -> str:
    return "struct GeneratedView: View { var body: some View { VStack { Text(\"Hello\") } } }"
