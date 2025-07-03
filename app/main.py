from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import yaml
import base64
import json
import openai

load_dotenv()

app = FastAPI(title="SwiftUI View Factory API")


def custom_openapi():
    yaml_path = Path(__file__).resolve().parents[1] / "api" / "openapi.yml"
    with open(yaml_path, "r") as f:
        schema = yaml.safe_load(f)
    return schema


app.openapi = custom_openapi


class LayoutNode(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
    tag: Optional[str] = None
    type: str
    text: Optional[str] = None
    children: Optional[List["LayoutNode"]] = None
    condition: Optional[str] = None
    then_: Optional["LayoutNode"] = Field(None, alias="then")
    else_: Optional["LayoutNode"] = Field(None, alias="else")

    class Config:
        allow_population_by_field_name = True


LayoutNode.update_forward_refs()


class LayoutInterpretationResponse(BaseModel):
    structured: LayoutNode
    description: Optional[str] = None
    version: Optional[str] = None
    log: Optional[str] = None


class OpenAIKeyResponse(BaseModel):
    api_key: str


@app.post("/factory/interpret", response_model=LayoutInterpretationResponse)
async def interpret_layout(file: UploadFile = File(...)):
    data = await file.read()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai.api_key = api_key
        b64 = base64.b64encode(data).decode("utf-8")
        messages = [
            {
                "role": "system",
                "content": "You convert UI mocks into JSON layout trees for SwiftUI.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Return a JSON representation of the layout using the LayoutNode schema. JSON only.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{file.content_type};base64,{b64}"},
                    },
                ],
            },
        ]
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={"type": "json_object"},
        )
        log = response.model_dump_json()
        try:
            content = response.choices[0].message.content
            payload = json.loads(content)
            root_node = LayoutNode(**payload)
        except (json.JSONDecodeError, ValueError) as exc:
            raise HTTPException(
                status_code=500, detail="Invalid response from OpenAI"
            ) from exc
        return LayoutInterpretationResponse(
            structured=root_node, version="layout-v1", log=log
        )
    # Fallback placeholder when no API key is configured
    root_node = LayoutNode(
        type="VStack", children=[LayoutNode(type="Text", text="Hello")]
    )
    return LayoutInterpretationResponse(
        structured=root_node,
        description="Simple VStack with Hello text",
        version="layout-v1",
    )


class GenerateRequest(BaseModel):
    layout: LayoutNode
    name: Optional[str] = None
    style: Optional[Dict[str, Any]] = None
    backend_hooks: Optional[bool] = False


@app.post("/factory/generate")
async def generate_swiftui_view(data: GenerateRequest):
    name = data.name or "GeneratedView"
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai.api_key = api_key
        prompt = (
            "Generate a SwiftUI View struct named "
            f"{name} using the following JSON layout: {data.layout.json()}. "
            "Return only the Swift code."
        )
        messages = [
            {
                "role": "system",
                "content": "You generate SwiftUI code from layout descriptions.",
            },
            {"role": "user", "content": prompt},
        ]
        response = openai.chat.completions.create(model="gpt-4o", messages=messages)
        log = response.model_dump_json()
        swift = response.choices[0].message.content.strip()
        return {"swift": swift, "log": log}
    swift = f'struct {name}: View {{\n    var body: some View {{\n        Text("Hello")\n    }}\n}}'
    return {"swift": swift}


@app.get("/secret", response_model=OpenAIKeyResponse)
async def get_openai_key():
    api_key = os.getenv("OPENAI_API_KEY", "")
    return OpenAIKeyResponse(api_key=api_key)
