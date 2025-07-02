// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "ExampleSDK",
    platforms: [
        .macOS(.v13),
        .iOS(.v17),
        .visionOS(.v1)
    ],
    products: [
        .library(name: "ExampleSDK", targets: ["ExampleSDK"])
    ],
    targets: [
        .target(name: "ExampleSDK", path: "Sources")
    ]
)
