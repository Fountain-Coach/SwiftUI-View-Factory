// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "iOSDemoApp",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .executable(name: "iOSDemoApp", targets: ["iOSDemoApp"])
    ],
    targets: [
        .executableTarget(
            name: "iOSDemoApp",
            path: "Sources"
        )
    ]
)
