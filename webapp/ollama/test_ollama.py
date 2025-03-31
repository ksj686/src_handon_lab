import requests
import json
url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": "대한민국의 역대 왕조를 소개해줄래?"
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print('Success')
    # 개별 JSON 객체로 분할
    json_objects = response.content.decode().strip().split("\n")

    # 각 JSON 객체를 Python 사전으로 변환
    data = [json.loads(obj) for obj in json_objects]
    res_text = ''
    # 변환된 데이터 출력
    for item in data:
        print(item)
        res_text += item['response']
        
    print(res_text)
else:
    print("Error:", response.status_code, response.text)

'''
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ollama API 설정 (URL과 API 키)
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_API_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMCj5CxNHVHcrOu8hd9olDptPb3Ze9d8+08/m0vHpDmV"

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    headers = {
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"}), 500

    summary = response.json().get('summary')
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)

'''