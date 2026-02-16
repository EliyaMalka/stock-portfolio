import requests

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# === Configuration ===
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"
COLLECTION_NAME = "stock_qa_collection"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
TOP_K = 3

# === Setup ===
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


# === 1. Rephrase the user's question ===
def rephrase_question(question):
    system_prompt = (
        "Please rewrite the following question to be clearer "
        "and fix any spelling or grammar mistakes. Respond only with the fixed question."
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    try:
        data = response.json()
        return data['message']['content'].strip()
    except KeyError:
        print("\n[Error] Unexpected response from Ollama.")
        print(data)
        return "Failed to rephrase question."


# === 2. Search Qdrant for relevant context ===
def search_qdrant(query, top_k=TOP_K):
    vector = embedder.encode(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector.tolist(),
        limit=top_k
    )
    contexts = []
    for result in results:
        payload = result.payload
        if "question" in payload and "answer" in payload:
            contexts.append(f"Q: {payload['question']}\nA: {payload['answer']}")
        elif "text" in payload:
            contexts.append(payload['text'])
    return "\n\n".join(contexts)


# === 3. Generate final answer with Ollama ===
def generate_answer(context, question):
    prompt = f"""Answer the following question based on the context below. 
If the answer is not found, say "I don't know."

Context:
{context}

Question:
{question}
"""
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    })
    return response.json()['message']['content'].strip()


# === 4. Main chat loop ===
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter a question (or type 'exit' to quit): ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Exiting.")
            break

        print("\n[Step 1] Rephrasing the question...")
        rephrased = rephrase_question(user_input)
        print(f"Rephrased question: {rephrased}")

        print("\n[Step 2] Searching for relevant context in Qdrant...")
        context = search_qdrant(rephrased)

        print("\n[Step 3] Generating answer using Ollama...")
        answer = generate_answer(context, rephrased)

        print("\n[Result] Answer:")
        print(answer)
