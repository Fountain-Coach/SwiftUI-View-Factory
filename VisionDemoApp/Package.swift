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
    dependencies: [
        .package(path: "../SDK/ExampleSDK")
    ],
    targets: [
        .executableTarget(
            name: "VisionDemoApp",
            dependencies: ["ExampleSDK"],
            path: "Sources"
        )
    ]
)
