// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "ExampleApp",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .executable(name: "ExampleApp", targets: ["ExampleApp"])
    ],
    dependencies: [
        .package(path: "../SDK/ExampleSDK")
    ],
    targets: [
        .executableTarget(
            name: "ExampleApp",
            dependencies: ["ExampleSDK"],
            path: "Sources"
        )
    ]
)
