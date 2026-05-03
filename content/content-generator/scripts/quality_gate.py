"""
Quality Gate — Preview image before spending on I2V
Shows generated image to user → confirm/regenerate/cancel
Saves ~50% cost by catching bad images early.
"""
import os, json, time

GATE_FILE = "/home/openclaw/.openclaw/workspace/output/quality_gates.json"
os.makedirs(os.path.dirname(GATE_FILE), exist_ok=True)


def save_gate(chat_id: str, image_path: str, context: dict):
    """Save pending quality gate — waiting for user approval"""
    gates = _load_all()
    gates[str(chat_id)] = {
        "image_path": image_path,
        "context": context,
        "status": "pending",
        "created_at": time.time()
    }
    _save_all(gates)


def get_gate(chat_id: str) -> dict:
    return _load_all().get(str(chat_id), {})


def approve_gate(chat_id: str):
    gates = _load_all()
    if str(chat_id) in gates:
        gates[str(chat_id)]["status"] = "approved"
        _save_all(gates)


def reject_gate(chat_id: str):
    gates = _load_all()
    gates.pop(str(chat_id), None)
    _save_all(gates)


def is_pending(chat_id: str) -> bool:
    gate = get_gate(chat_id)
    return gate.get("status") == "pending"


def _load_all():
    if os.path.exists(GATE_FILE):
        with open(GATE_FILE) as f:
            return json.load(f)
    return {}


def _save_all(data):
    with open(GATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def build_preview_message(image_path: str) -> tuple[str, list]:
    """Build message + buttons for quality gate"""
    text = (
        "Ini hasil image-nya dulu! 👆\n\n"
        "Suka? Lanjut ke video, atau mau generate ulang?"
    )
    buttons = [
        [
            {"text": "🚀 Lanjut ke Video!", "callback_data": "gate:approve"},
            {"text": "🔄 Generate Ulang", "callback_data": "gate:retry"},
        ],
        [
            {"text": "❌ Batal", "callback_data": "gate:cancel"}
        ]
    ]
    return text, buttons
