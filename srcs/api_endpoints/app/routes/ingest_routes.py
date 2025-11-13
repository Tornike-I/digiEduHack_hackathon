from flask import Blueprint, request, jsonify
from ..logic.ingest_logic import ingest_document
from ..db.vector_store import VectorStore

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.route("/ingest", methods=["POST"])
def ingest():
    """
    POST /api/ingest
    JSON body: {"text": "...", "metadata": {...}}
    """
    body = request.get_json(force=True)
    text = body.get("text")
    if not text:
        return jsonify({"error": "Missing 'text' in body"}), 400
    metadata = body.get("metadata")
    result = ingest_document(text, metadata=metadata)
    return jsonify({"status": "ok", **result}), 201

@ingest_bp.route("/ingest/clear", methods=["POST"])
def clear():
    # helper to clear DB during dev
    VectorStore().clear()
    return jsonify({"status": "cleared"})
