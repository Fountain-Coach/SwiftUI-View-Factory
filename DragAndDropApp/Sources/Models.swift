/// Codable models corresponding to the View Factory API.
import Foundation

final class LayoutNode: Codable {
    var id: String?
    var role: String?
    var tag: String?
    var type: String
    var text: String?
    var children: [LayoutNode]?
    var condition: String?
    var then: LayoutNode?
    var else_: LayoutNode?

    enum CodingKeys: String, CodingKey {
        case id, role, tag, type, text, children, condition, then
        case else_ = "else"
    }
}

struct LayoutInterpretationResponse: Codable {
    var structured: LayoutNode
    var description: String?
    var version: String
}

struct GenerateResponse: Codable {
    var swift: String
}
