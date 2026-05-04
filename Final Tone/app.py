from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

genai.configure(api_key="paste your gemini api key")

MODELS = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

def get_model():
    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model
        except:
            continue
    raise Exception("All models exhausted.")

model = get_model()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.json
    text = data.get("text", "")
    tone = data.get("tone", "friendly")
    prompt = f"Rewrite this sentence in a {tone} tone:\n{text}"
    response = model.generate_content(prompt)
    return jsonify({"result": response.text})

if __name__ == "__main__":
    app.run(debug=True)
