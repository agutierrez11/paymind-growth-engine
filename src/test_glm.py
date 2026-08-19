import os
import requests
import json

api_key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

# Test endpoints
endpoints = [
    ("https://zenmux.ai/api/v1/chat/completions", "z-ai/glm-5.3-free"),
    ("https://zenmux.ai/v1/chat/completions", "z-ai/glm-5.3-free"),
    ("https://api.zenmux.ai/v1/chat/completions", "z-ai/glm-5.3-free"),
    ("https://open.bigmodel.cn/api/paas/v4/chat/completions", "glm-4-flash")
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "z-ai/glm-5.3-free",
    "messages": [
        {"role": "user", "content": "Hola, confirma si estás activo y cuál es tu nombre de modelo."}
    ],
    "temperature": 0.3
}

for url, model in endpoints:
    payload["model"] = model
    print(f"Probando endpoint: {url} con modelo {model}...")
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print("RESPUESTA EXITOSA:")
            print(res.json()["choices"][0]["message"]["content"])
            break
        else:
            print(f"Error: {res.text[:200]}")
    except Exception as e:
        print(f"Excepción: {e}")
