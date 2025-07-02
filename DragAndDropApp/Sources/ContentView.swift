/// Main application view hosting the drag/drop area and code preview.
import SwiftUI
import AppKit
#if canImport(ExampleSDK)
import ExampleSDK
#endif

struct ContentView: View {
    @State private var selectedImage: NSImage? = nil
    @State private var generatedCode: String = ""
    @State private var isLoading: Bool = false
#if canImport(ExampleSDK)
    private let sdk = ExampleClient()
#endif

    var body: some View {
        HStack {
            DragDropAreaView(image: $selectedImage, isLoading: $isLoading)
                .frame(width: 300, height: 300)
            Divider()
            CodePreviewView(code: generatedCode)
        }
        .padding()
        .task(id: selectedImage) {
            await processImage()
        }
    }

    /// Sends the image to the backend and updates the code preview.
    @MainActor
    func processImage() async {
        guard let image = selectedImage else { return }
        isLoading = true
        do {
            let layoutResponse = try await API.shared.interpret(image: image)
            generatedCode = try await API.shared.generate(from: layoutResponse.structured)
#if canImport(ExampleSDK)
            sdk.logMessage()
#endif
        } catch {
            generatedCode = "Error: \(error.localizedDescription)"
        }
        isLoading = false
    }
}

#Preview {
    ContentView()
}
