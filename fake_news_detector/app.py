import os
import zipfile
import gdown
import torch
from flask import Flask, render_template, request
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

MODEL_ZIP = "bert_model.zip"
MODEL_DIR = "bert_model/"
GOOGLE_ID = "1y4d8oeyIJV3NVGJJOlJF9RC_nai8xMNN"  # replace with your real ID

# ✅ Download model if not present
if not os.path.exists(MODEL_DIR):
    print("[INFO] Downloading fine-tuned model...")
    try:
        gdown.download(id=GOOGLE_ID, output=MODEL_ZIP, quiet=False)
    except Exception as e:
        print(f"[ERROR] Failed to download model: {e}")
        exit(1)

    print("[INFO] Extracting model...")
    with zipfile.ZipFile(MODEL_ZIP, 'r') as zip_ref:
        zip_ref.extractall()
    print("[SUCCESS] Model ready at", MODEL_DIR)

# ✅ Load model
print("[INFO] Loading BERT model and tokenizer...")
model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
tokenizer = BertTokenizer.from_pretrained(MODEL_DIR)

device = 0 if torch.cuda.is_available() else -1
print(f"[INFO] Using {'GPU' if device == 0 else 'CPU'}")

pipe = TextClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    return_all_scores=False,
    device=device
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['news']
    if not input_text.strip():
        return render_template("result.html", label="❌ Empty input", confidence="N/A")

    # Truncate to 512 tokens
    tokens = tokenizer.encode(input_text, truncation=True, max_length=512)
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

    try:
        output = pipe(truncated_text)
        if isinstance(output, list) and len(output) > 0:
            result = output[0]
            label = "Fake" if result['label'] == "LABEL_1" else "Real"
            confidence = f"{result['score'] * 100:.2f}%"
            return render_template("result.html", label=label, confidence=confidence)
        else:
            return render_template("result.html", label="❌ No prediction", confidence="N/A")
    except Exception as e:
        return f"❌ Prediction Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
