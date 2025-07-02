import SwiftUI
#if canImport(ExampleSDK)
import ExampleSDK
#endif

@main
struct ExampleApp: App {
#if canImport(ExampleSDK)
    private let sdk = ExampleClient()
#endif
    init() {
#if canImport(ExampleSDK)
        sdk.logMessage()
#endif
    }
    var body: some Scene {
        WindowGroup {
            GeneratedView()
        }
    }
}
