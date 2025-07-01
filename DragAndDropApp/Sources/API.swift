/// Networking layer for communicating with the View Factory backend.
import Foundation
import AppKit

final class API {
    @MainActor static let shared = API()

    let baseURL: URL
    private let session: URLSession

    @MainActor
    init(baseURL: URL = AppConfig.shared.baseURL, session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
    }

    /// Uploads an image to the `/factory/interpret` endpoint.
    func interpret(image: NSImage) async throws -> LayoutInterpretationResponse {
        guard let data = image.tiffRepresentation else {
            throw URLError(.cannotDecodeContentData)
        }

        var request = URLRequest(url: baseURL.appendingPathComponent("factory/interpret"))
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.png\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/png\r\n\r\n".data(using: .utf8)!)
        body.append(NSBitmapImageRep(data: data)?.representation(using: .png, properties: [:]) ?? data)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        request.httpBody = body

        let (responseData, _) = try await session.data(for: request)
        return try JSONDecoder().decode(LayoutInterpretationResponse.self, from: responseData)
    }

    /// Sends a layout to the `/factory/generate` endpoint.
    func generate(from layout: LayoutNode) async throws -> String {
        var request = URLRequest(url: baseURL.appendingPathComponent("factory/generate"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(layout)

        let (data, _) = try await session.data(for: request)
        let result = try JSONDecoder().decode(GenerateResponse.self, from: data)
        return result.swift
    }
}
