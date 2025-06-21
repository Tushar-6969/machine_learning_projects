# 🖼️ Text Extracter - OCR Web App

This project is a full-stack web application for extracting text from images using OCR (Optical Character Recognition). It integrates a **Node.js + Express.js** backend with a **Python-based OCR model** (using EasyOCR or Tesseract) and serves dynamic pages using **EJS**.

---

## 🚀 How It Works

1. User uploads an image from the front-end (`views/index.ejs`).
2. The image is received and saved by `server.js` using **Multer** middleware.
3. `server.js` spawns a Python process and passes the image path to `model.py`.
4. `model.py` performs OCR using EasyOCR or Tesseract and returns the extracted text.
5. The output is captured and rendered in `templates/result.ejs`.

---

## 📁 Folder Structure

```
text extracter/
├── api/                  # (Optional) Future API routes or endpoints
├── public/               # Static assets (e.g., CSS, JS, etc.)
├── templates/            # EJS templates for output (e.g., result.ejs)
├── uploads/              # Uploaded images temporarily stored here
├── views/                # Frontend EJS (e.g., index.ejs for upload form)
├── model.py              # Python script for OCR
├── server.js             # Node.js + Express server
├── package.json          # Node dependencies
├── package-lock.json
└── image.png             # Sample test image
```

---

## 🧪 Tech Stack

* **Frontend:** EJS (views/templates), HTML
* **Backend:** Node.js, Express.js
* **File Upload:** Multer
* **OCR Model:** Python using:

  * [EasyOCR](https://github.com/JaidedAI/EasyOCR) (preferred)
  * Or [pytesseract](https://pypi.org/project/pytesseract/)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Tushar-6969/machine_learning_projects.git
cd machine_learning_projects/text\ extracter
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Install Python Requirements

Make sure Python 3 is installed. Then run:

```bash
pip install easyocr opencv-python numpy
```

If you're using `pytesseract`:

```bash
pip install pytesseract
```

Also install the **Tesseract-OCR binary**:

* Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
* Linux: `sudo apt install tesseract-ocr`

---

## ▶️ Run the App

```bash
node server.js
```

Now open your browser and go to:
🔗 [http://localhost:3000](http://localhost:3000)

---

## 📷 Usage Example

* Go to the homepage.
* Upload an image containing text.
* The server processes the image and renders the extracted text.

---

## 📌 Notes

* OCR is handled by a separate `model.py` script for modularity and flexibility.
* `server.js` uses `child_process.spawn()` to run Python code and capture the output.
* Images are saved in `/uploads` for temporary use and not persisted.
* You can switch between EasyOCR and Tesseract in `model.py` easily.

---

## 👨‍💼 Author

**Tushar Rathor**
BTech CSE (AIML)
GitHub: [@Tushar-6969](https://github.com/Tushar-6969)

---

## 💬 Feedback & Contributions

Pull requests, feature suggestions, and feedback are always welcome!
If you like this project, consider giving it a ⭐ on GitHub.
