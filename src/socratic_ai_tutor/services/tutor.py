import base64
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.deepseek.com")

def solve(image_bytes: bytes):
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "以初中数学老师的身份向用户讲解这道题目，使用初中方法，返回格式为标准的Markdown，通过与用户不断的对话和提问，苏格拉底式的引导用户解题，每次引导一步"},
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            },
        ],
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )
    
    return response.choices[0].message.content