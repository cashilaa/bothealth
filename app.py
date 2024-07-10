import os
import time
import random
from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_community.llms import Replicate
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()

# Initialize embeddings
try:
    embeddings = download_hugging_face_embeddings()
    if embeddings is None:
        raise ValueError("The embeddings is None. Please check the download_hugging_face_embeddings function.")
    print(f"Embeddings: {embeddings}")
except Exception as e:
    print(f"Error initializing embeddings: {e}")
    embeddings = None

<<<<<<< HEAD
# def text_split(text):
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     document = Document(page_content=text)
#     return text_splitter.split_documents([document])

# Load and process data
# pdf_file_path = "data/Gale Encyclopedia of Medicine Vol. 1 (A-B).pdf"
# extracted_data = load_pdf(pdf_file_path)
# if extracted_data is None:
#     raise ValueError("The extracted data is None. Please check the load_pdf function.")
# print(f"Extracted Data: {extracted_data}")

# Split the extracted text into chunks
# text_chunks = text_split(extracted_data)
# if not text_chunks:
#     raise ValueError("The text_chunks is None or empty. Please check the text_split function.")
# print(f"Text Chunks: {text_chunks}")

embeddings = download_hugging_face_embeddings()
if embeddings is None:
    raise ValueError("The embeddings is None. Please check the download_hugging_face_embeddings function.")
print(f"Embeddings: {embeddings}")

os.environ["REPLICATE_API_TOKEN"] = ["REPLICATE_API_TOKEN"]
=======
# Set Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_eKkENc6fSN6Jn2sYOgnosHLoD0Kb4rv4GjgUB"
>>>>>>> 3b33fe27defdcd99d45403ee1c19faf153b57a5b

# Initialize the Replicate model
llm = Replicate(
    model="a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea",
    config={
        'max_new_tokens': 100,
        'temperature': 0.7,
        'top_k': 50
    }
)

# Function to generate question suggestions
def generate_question_suggestion():
    suggestions = [
        "What are some simple exercises I can do at home?",
        "How can I improve my sleep quality?",
        "What are the signs of dehydration I should watch out for?",
        "Can you explain the importance of regular health check-ups?",
        "What are some heart-healthy foods I should include in my diet?",
        "How can I manage stress effectively?",
        "What are the common side effects of my medications?",
        "How can I maintain good hygiene to prevent infections?",
        "What are some memory exercises I can practice daily?",
        "How can I make my home safer to prevent falls?",
        "What should I include in a balanced meal for my age?",
        "How often should I have my vision and hearing checked?",
        "What are some social activities suitable for seniors in my area?",
        "How can I keep my brain active and healthy?",
        "What are the benefits of staying socially active in old age?"
    ]
    return random.choice(suggestions)

# Flask routes
@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form["msg"]
        input_text = msg
        print(f"Received message: {input_text}")

        # Simulate processing delay
        time.sleep(1)

        # Retrieve response from the model
        result = llm.generate([input_text])
        print(f"LLMResult: {result}")

        # Access the generated text from the result object
        if result.generations and result.generations[0]:
            generated_text = result.generations[0][0].text
        else:
            generated_text = "I'm sorry, I couldn't generate a response. Could you please rephrase your question?"

        print(f"Response: {generated_text}")

        return jsonify({"response": generated_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route("/get_suggestion", methods=["GET"])
def get_suggestion():
    try:
        suggestion = generate_question_suggestion()
        return jsonify({"suggestion": suggestion})
    except Exception as e:
        print(f"Error generating suggestion: {e}")
        return jsonify({"error": "Unable to generate a suggestion at this time."}), 500

# Route to handle voice input
@app.route("/voice_input", methods=["POST"])
def voice_input():
    try:
        data = request.json
        voice_input_text = data["voice_input"]
        print(f"Voice input received: {voice_input_text}")

        # Simulate processing delay
        time.sleep(1)

        # Retrieve response from the model (similar to the /get route)
        result = llm.generate([voice_input_text])
        print(f"LLMResult: {result}")

        # Access the generated text from the result object
        if result.generations and result.generations[0]:
            generated_text = result.generations[0][0].text
        else:
            generated_text = "I'm sorry, I couldn't generate a response. Could you please rephrase your question?"

        print(f"Response: {generated_text}")

        return jsonify({"response": generated_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing your voice input. Please try again."}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
