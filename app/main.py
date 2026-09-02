from flask import Flask, request, jsonify
from app.claude import get_response

app = Flask(__name__)

# Historial de conversaciones por número de teléfono (en memoria)
conversations: dict[str, list] = {}


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/chat")
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Campo 'message' requerido"}), 400
    messages = [{"role": "user", "content": data["message"]}]
    response = get_response(messages)
    return jsonify({"response": response})


@app.post("/whatsapp")
def whatsapp():
    incoming = request.form.get("Body", "").strip()
    from_number = request.form.get("From", "unknown")

    if not incoming:
        return _twiml("")

    if from_number not in conversations:
        conversations[from_number] = []

    conversations[from_number].append({"role": "user", "content": incoming})

    response = get_response(conversations[from_number])

    conversations[from_number].append({"role": "assistant", "content": response})

    return _twiml(response)


def _twiml(message: str):
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""
    return app.response_class(xml, mimetype="text/xml")
