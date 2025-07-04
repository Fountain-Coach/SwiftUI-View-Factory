#!/usr/bin/env python3
"""Process images in the image-upload directory and send them to the OpenAI API.

This handler collects all image files under ``image-upload/`` in chronological
order and submits them to the vision model. The final response from the model is
saved so other handlers can consume it as the last reply of the model.
"""
import os
import sys
import json
import base64
import yaml
import openai

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'image-upload')


def list_images(path: str) -> list[str]:
    """Return a sorted list of image paths by modification time."""
    supported = ('.png', '.jpg', '.jpeg')
    images = [os.path.join(path, f) for f in os.listdir(path)
              if f.lower().endswith(supported)]
    images.sort(key=lambda p: os.path.getmtime(p))
    return images


def encode_image(path: str) -> str:
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


if __name__ == '__main__':
    request_file = sys.argv[1]
    log_dir = sys.argv[2]

    with open(request_file) as f:
        data = yaml.safe_load(f)

    spec = data.get('spec', {})
    model = spec.get('gpt_model', 'gpt-4o')

    response_file = os.path.join(log_dir, 'processImageUploads_response.json')
    status_file = os.path.join(log_dir, 'status.yml')

    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        images = list_images(UPLOAD_DIR)
        if not images:
            raise FileNotFoundError('No images found in image-upload directory')

        contents = [
            {"type": "text", "text": "Interpret these mockups chronologically."}
        ]
        for path in images:
            contents.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{encode_image(path)}"}
            })

        messages = [
            {
                "role": "system",
                "content": (
                    "You are the SwiftUI View factory. Given a series of UI "
                    "mockups, return the best SwiftUI view code as JSON with "
                    "keys 'swift' and 'description'."
                ),
            },
            {"role": "user", "content": contents},
        ]

        resp = openai.ChatCompletion.create(model=model, messages=messages)
        result = {
            "reply": resp.choices[0].message.content.strip(),
            "log": json.dumps(resp, default=str),
        }
        with open(response_file, 'w') as f:
            json.dump(result, f, indent=2)
        status = 'success'
    except Exception as e:
        with open(os.path.join(log_dir, 'error.log'), 'w') as f:
            f.write(str(e))
        status = 'error'

    with open(status_file, 'w') as f:
        f.write(f'status: {status}\n')
