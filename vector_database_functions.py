from dotenv import load_dotenv

genai.configure(api_key= os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def embed_text(text, single=False):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs)
    embeddings = embeddings.last_hidden_state.mean(dim=1).numpy()
    if single:
        return embeddings[0]
    return embeddings

def store_embeddings(filename, embeddings):
    for i, embedding in enumerate(embeddings):
        doc_ref = db.collection('pdf_embeddings').document(f"{filename}_{i}")
        doc_ref.set({'embedding': embedding.tolist(), 'filename': filename})

from scipy.spatial.distance import cosine

def query_embeddings(query_embedding):
    docs = db.collection('pdf_embeddings').stream()
    similarities = []
    for doc in docs:
        data = doc.to_dict()
        embedding = np.array(data['embedding'])
        similarity = 1 - cosine(query_embedding, embedding)
        similarities.append((similarity, data['filename']))
    similarities.sort(key=lambda x: x[0], reverse=True)
    return [filename for _, filename in similarities[:5]]

def generate_response(results, query):
    relevant_texts = "\n".join(results)
    prompt = f"This is the use case of user ['{query}'] and these are service titles available ['{relevant_texts}'] show output of the names of services suitable."
    response = model.generate_content(prompt)
    if response.status_code == 200:
        return response.json()["output"]
    else:
        raise Exception("Error in fetching response from Gemini API")
