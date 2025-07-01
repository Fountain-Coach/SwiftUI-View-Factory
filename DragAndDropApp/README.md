# DragAndDropApp

This sample macOS SwiftUI application demonstrates how to interact with the SwiftUI View Factory service.

The `DragDropAreaView` was bootstrapped using the factory itself. A small layout description (`DragDropArea.layout.json`) was fed into the CLI which produced the initial SwiftUI skeleton. The generated code was then extended with drag and drop logic and file selection support.

```
# Example generation command
python cli/vi.py generate DragDropArea.layout.json
```

The app performs the following steps:

1. Users drop or select an image.
2. The image is uploaded to `/api/v1/factory/interpret`.
3. The returned layout JSON is passed to `/api/v1/factory/generate`.
4. The resulting Swift code is shown in a preview pane.

Configure the backend URL via the `FACTORY_BASE_URL` environment variable. Defaults to `http://localhost:8000/api/v1`.

Open the package with Xcode (`File > Open Package`) and run the `DragAndDropApp` target on macOS 13 or later.
