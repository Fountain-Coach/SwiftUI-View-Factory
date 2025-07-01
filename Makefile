build:
	docker build -t swiftui-factory .

vi:
	docker run --rm -v $(PWD):/app -e OPENAI_API_KEY=$(OPENAI_API_KEY) swiftui-factory

mockup1:
	make build
	docker run --rm -v $(PWD):/app -e OPENAI_API_KEY=$(OPENAI_API_KEY) swiftui-factory interpret examples/mockup1.jpeg \
	  | docker run --rm -i -v $(PWD):/app -e OPENAI_API_KEY=$(OPENAI_API_KEY) swiftui-factory generate - \
	  | tee GeneratedView.swift \
	  | docker run --rm -i -v $(PWD):/app -e OPENAI_API_KEY=$(OPENAI_API_KEY) swiftui-factory test -
