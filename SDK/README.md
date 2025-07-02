# Client SDKs

Place custom Swift packages in this directory. Each package should contain a
`Package.swift` manifest so it can be built with Swift Package Manager.

The build script (`scripts/build_app.sh`) automatically discovers SDK packages
and compiles them before building the demo applications. Compiler diagnostics are
captured in `build.log` for inspection.
