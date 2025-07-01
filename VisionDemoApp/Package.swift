// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "VisionDemoApp",
    platforms: [
        .visionOS(.v1)
    ],
    products: [
        .executable(name: "VisionDemoApp", targets: ["VisionDemoApp"])
    ],
    targets: [
        .executableTarget(
            name: "VisionDemoApp",
            path: "Sources"
        )
    ]
)
