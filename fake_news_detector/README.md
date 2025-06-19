
# 📰 Fake News Detector using BERT

This project is a fine-tuned BERT model that classifies news articles as **Fake** or **Real**.  
It includes a complete training pipeline, a Flask web app for live predictions, and Google Drive integration for model loading.

---

## 🚀 Features

- ✅ Fine-tuned BERT (`bert-base-uncased`)
- ✅ High Accuracy (~99%)
- ✅ Flask web app with live input
- ✅ Handles large models via Google Drive download
- ✅ Clean modular code (training, prediction, frontend)

---

## 🏗️ Folder Structure

```
fake_news_detector/
├── app.py               # Flask web app
├── train.py             # Model training script
├── predict.py           # Manual prediction script
├── model_download.py    # Downloads model from Google Drive if missing
├── bert_model/          # Saved fine-tuned model (not on GitHub)
├── templates/           # HTML pages
├── static/              # CSS / JS (optional)
├── requirements.txt     # Python dependencies
├── .gitignore           # Files to exclude from Git
└── README.md            # This file
```

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Tushar-6969.git
cd "ML Projects/fake_news_detector"
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Get the Fine-tuned Model

#### Option A: Auto-download from Google Drive
```bash
python app.py
```

#### Option B: Manually download and unzip
Download `bert_model.zip` from [Google Drive](https://drive.google.com/file/d/1y4d8oeyIJV3NVGJJOlJF9RC_nai8xMNN/view?usp=sharing)  
Extract it inside `fake_news_detector/` so you have:

```
fake_news_detector/bert_model/
```

---

## ▶️ Run the Web App

```bash
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧠 Model Details

- Base Model: `bert-base-uncased`
- Dataset: [Fake and Real News Dataset (Kaggle)](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
- Binary classification: `LABEL_1` = Fake, `LABEL_0` = Real
- Accuracy: ~99% on balanced test data

---

## 📊 Sample Prediction

```text
📰 Input:
  The World Health Organization has declared the end of the COVID-19 emergency.

📢 Prediction: Real News  
📊 Confidence: 98.6%
```

---

## 📁 Dataset Usage

This project uses two CSVs:
- `Fake.csv`
- `True.csv`

You can:
- Download them from Kaggle
- Or use the script to load them from Drive
- Or upload sample CSVs in `sample_data/`

---

## ⚠️ Notes

- `bert_model/` is ignored via `.gitignore` to keep repo small.
- Use the Google Drive download script or zip manually.

---

## 👨‍💻 Author

Made with ❤️ by **Tushar Rathor**

[GitHub](https://github.com/Tushar-6969) • [LinkedIn](www.linkedin.com/in/tushar-rathor-277427259)

---
