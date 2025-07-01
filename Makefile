.PHONY: generate test build

generate:
	docker run --rm -v $(PWD):/app -e OPENAI_API_KEY=$$OPENAI_API_KEY \
		swiftui-factory vi generate draganddrop-starter/draganddrop.layout.json \
		> DragAndDropApp/DragDropAreaView.swift

test:
	docker run --rm -v $(PWD):/app swiftui-factory pytest -q

build:
	open DragAndDropApp/DragAndDropApp.xcodeproj
