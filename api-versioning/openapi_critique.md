# Critique of `api/openapi.yml`

The current API specification focuses on generic actions for interpreting UI
mockups and generating SwiftUI code. However, it does not explicitly state that
the interpretation step relies on OpenAI's GPT-4o vision capabilities. The
`/secret` endpoint merely exposes the API key through an additional route,
burdening clients with retrieving a constant secret that should normally be
injected via environment variables.

## Issues

1. **Lack of explicit contract with GPT-4o**
   - `/factory/interpret` only mentions uploading a mockup. It does not make it
     clear that the backend sends the image to GPT-4o for vision analysis.
   - Consumers cannot easily know which model or version is used, so they cannot
     reason about costs or capabilities.

2. **Unnecessary `/secret` endpoint**
   - Fetching the OpenAI API key over HTTP is insecure and complicates the API.
   - The key is constant for a deployment and should be injected via
     configuration rather than fetched at runtime.

3. **Versioning**
   - The spec version is `1.2.0`, but the change history is unclear.
   - There is no place for experimenting with new versions.

## Suggested Update

- Make the dependency on GPT-4o explicit in the description and in the
  `interpret` endpoint.
- Add an optional `gpt_model` parameter allowing clients to specify the desired
  OpenAI model (defaulting to `gpt-4o`).
- Remove the `/secret` endpoint and rely on environment variables for API key
  management.
- Increment the spec version to `1.3.0` and store updated specs under the new
  `api-versioning` directory for clarity.

The file [`openapi_v1.3.yml`](openapi_v1.3.yml) reflects these changes.
