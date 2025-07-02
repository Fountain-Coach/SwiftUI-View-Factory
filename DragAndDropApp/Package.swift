// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "DragAndDropApp",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "DragAndDropApp", targets: ["DragAndDropApp"])
    ],
    dependencies: [
        .package(path: "../SDK/ExampleSDK")
    ],
    targets: [
        .executableTarget(
            name: "DragAndDropApp",
            dependencies: ["ExampleSDK"],
            path: "Sources"
        )
    ]
)
