/// Area that accepts dragged images or allows selecting via file dialog.
import SwiftUI
import AppKit
import UniformTypeIdentifiers

struct DragDropAreaView: View {
    @Binding var image: NSImage?
    @Binding var isLoading: Bool
    @State private var hovering: Bool = false

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 8)
                .strokeBorder(style: StrokeStyle(lineWidth: 2, dash: [5]))
                .background(Color.gray.opacity(0.1))
            if let image {
                Image(nsImage: image)
                    .resizable()
                    .scaledToFit()
            } else {
                VStack {
                    Image(systemName: "photo")
                        .font(.largeTitle)
                    Text("Drop Image Here")
                        .font(.headline)
                    Button("Choose File", action: selectFile)
                }
            }
            if isLoading {
                ProgressView()
            }
        }
        .onDrop(of: [UTType.fileURL], isTargeted: $hovering) { providers in
            loadImage(from: providers)
            return true
        }
    }

    /// Presents an open panel for manual image selection.
    func selectFile() {
        let panel = NSOpenPanel()
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        panel.allowedContentTypes = [.image]
        if panel.runModal() == .OK, let url = panel.url, let img = NSImage(contentsOf: url) {
            image = img
        }
    }

    /// Extracts an image from dropped providers.
    func loadImage(from providers: [NSItemProvider]) {
        for provider in providers {
            if provider.hasItemConformingToTypeIdentifier(UTType.image.identifier) {
                _ = provider.loadObject(ofClass: URL.self) { url, _ in
                    if let url, let img = NSImage(contentsOf: url) {
                        DispatchQueue.main.async {
                            self.image = img
                        }
                    }
                }
                break
            }
        }
    }
}

#Preview {
    DragDropAreaView(image: .constant(nil), isLoading: .constant(false))
        .frame(width: 300, height: 300)
}
