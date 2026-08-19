import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Let's test the key on disier
api_key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

url = "https://llm.disier.net/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Qwen/Qwen3.8-27B",
    "messages": [
        {"role": "user", "content": "Hola Qwen, confirma si estás activo."}
    ],
    "temperature": 0.3
}

print("Probando conexión con Disier LLM (Qwen/Qwen3.8-27B)...")
try:
    res = requests.post(url, headers=headers, json=payload, timeout=20)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print("¡CONEXIÓN EXITOSA!")
        print(res.json()["choices"][0]["message"]["content"])
    else:
        print("Respuesta de error:", res.text)
except Exception as e:
    print(f"Error: {e}")
