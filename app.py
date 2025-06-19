import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loader import load_document_from_url
from chunker import chunk_text
from embedder import embed_texts, embed_text
from vector_store import store_embeddings, query_top_k, clear_all_chunks
from llm_client import ask_llm

app = Flask(__name__)
CORS(app)

@app.route("/index", methods=["POST"])
def index_document():
    data = request.get_json()
    url = data.get("url")
    print(url)
    if not url:
        return jsonify({"error": "Missing 'url' in request"}), 400
    try:
        text = load_document_from_url(url)
        print(text)
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks)
        print(embeddings)
        store_embeddings(chunks, embeddings)
        return jsonify({"message": f"Indexed {len(chunks)} chunks."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400
    try:
        q_emb = embed_text(question)
        top_chunks = query_top_k(q_emb, k=3)
        if not top_chunks:
            return jsonify({"error": "No indexed data found. Please index a document first."}), 400
        context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, (chunk, _) in enumerate(top_chunks)])
        prompt = (
            f"Given the following document excerpts:\n\n{context}\n\n"
            f"Answer the following question as accurately as possible:\n{question}"
        )
        answer = ask_llm(prompt)
        return jsonify({"answer": answer, "chunks": [c[0] for c in top_chunks]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear_index():
    try:
        clear_all_chunks()
        return jsonify({"message": "All indexed chunks cleared from Redis."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
