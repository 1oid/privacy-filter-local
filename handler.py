from flask import Flask, request, jsonify
import json
import os
from opf._api import OPF

import runpod
import json
import requests
import os
import re
from typing import Optional
from google import genai
from google.genai import types


class GeminiAnswer:

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Please set GEMINI_API_KEY environment variable or provide API key")

        os.environ['GEMINI_API_KEY'] = self.api_key

        self.client = genai.Client()
        self.model_name = model_name

    def process(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        content = self.clear_content(prompt)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=content,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.6,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                thinking_config=types.ThinkingConfig(thinking_budget=-1)  # 开启动态思考
            )
        )
        return self._clean_yaml_content(response.text)

    def clear_content(self, content: str) -> str:
        # delete begin with # digest:
        content = re.sub(r'# digest:.*?(?:\r\n|\r|\n|$)', '', content)
        return content.strip()

    def _clean_yaml_content(self, content: str) -> str:
        """
        clean YAML content, remove markdown format

        Args:
            content: original content

        Returns:
            str: cleaned content
        """
        # remove ```yaml and ``` mark
        content = re.sub(r'^```yaml\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)

        # remove <output> tag
        content = re.sub(r'<output>\s*', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s*</output>', '', content, flags=re.IGNORECASE)

        # remove extra empty lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        return content.strip()


def handler(event):
    """
    This is the handler function that will be called by RunPod serverless.
    """

    job_input = event.get('input', None)

    if job_input is None:
        return {
            "status": 500,
            "message": "input is null"
        }

    text = job_input.get('text', None)
    redc = OPF(
        device='mps',
        decode_mode='viterbi',
        output_mode='typed',
        discard_overlapping_predicted_spans=False,
    )
    result = redc.redact(text)

    return {
        "resp": result,
        "status": 200,
        "message": "success"
    }