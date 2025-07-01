/// Displays generated SwiftUI source code.
import SwiftUI

struct CodePreviewView: View {
    var code: String

    var body: some View {
        ScrollView {
            Text(code.isEmpty ? "Generated code will appear here" : code)
                .font(.system(.body, design: .monospaced))
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
        }
    }
}

#Preview {
    CodePreviewView(code: "")
}
