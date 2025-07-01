/// Reads environment variables for app configuration.
import Foundation

final class AppConfig {
    @MainActor static let shared = AppConfig()

    /// Base URL for the backend API.
    let baseURL: URL

    private init() {
        if let env = ProcessInfo.processInfo.environment["FACTORY_BASE_URL"], let url = URL(string: env) {
            baseURL = url
        } else {
            baseURL = URL(string: "http://localhost:8000/api/v1")!
        }
    }
}
