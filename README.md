# 🧠 Smart Resume Screener  
### _AI-Powered JD–Resume Analyzer using Google Gemini_

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Flask-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Frontend-TailwindCSS-38b2ac?style=flat-square">
  <img src="https://img.shields.io/badge/AI-Google%20Gemini-orange?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square">
</p>

> 🚀 A lightweight AI-based web application that analyzes resumes against job descriptions using **Google Gemini Pro Vision API**, delivering an instant **match score**, **key strengths**, and **identified gaps** to assist in data-driven hiring.

---



## 🧩 Features

✅ **AI-Driven Resume Analysis** — Scores resumes against JDs using Google Gemini.  
✅ **Instant Insights** — Shows top strengths and critical gaps for each candidate.  
✅ **Modern UI** — Built with Tailwind CSS for a clean, responsive layout.  
✅ **Structured Output** — Enforces a strict JSON schema for consistency.  
✅ **Easy Integration** — Simple REST API ready for production or extension.  

---

## 🏗️ Project Structure

```
Smart-Resume-Screener/
├── resume_screener_backend.py     # Flask backend: handles AI logic & API requests
├── resume_screener_frontend.html  # Frontend: Tailwind + Vanilla JS
└── README.md                      # Project documentation (this file)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML5, Tailwind CSS, JavaScript (Fetch API) |
| **Backend** | Python 3.x, Flask, Flask-CORS |
| **AI Engine** | Google Gemini (`google-genai` SDK) |
| **Output Schema** | JSON (strict schema validation) |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/smart-resume-screener.git
cd smart-resume-screener
```

### 2️⃣ Install Backend Dependencies
Make sure Python 3.8+ is installed.

```bash
pip install flask flask-cors google-genai
```

### 3️⃣ Set Up Environment Variables

You need a valid Gemini API key.  
Get yours from [Google AI Studio Console](https://aistudio.google.com/).

```bash
# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows CMD
set GEMINI_API_KEY="your_api_key_here"
```

---

## 🧠 Running the Application

### 🖥️ Step 1: Start the Flask Backend
```bash
python resume_screener_backend.py
```
It will start a local server at:
```
http://127.0.0.1:8080
```

### 🌐 Step 2: Open the Frontend
Open `resume_screener_frontend.html` directly in your browser.

> 💡 You can edit the backend URL in the HTML file (`API_URL`) if running on a remote server.

---

## 📡 API Documentation

### Endpoint: `/analyze`
**Method:** `POST`  
**Content-Type:** `application/json`

#### 🔹 Request Body
```json
{
  "job_description": "Looking for a Python developer with React experience...",
  "candidates": [
    {
      "id": "Candidate 1",
      "resume_text": "5 years of experience in Python, Flask, React..."
    }
  ]
}
```

#### 🔹 Response
```json
{
  "status": "success",
  "results": [
    {
      "candidate_id": "Candidate 1",
      "analysis": {
        "match_score": 9,
        "candidate_name": "John Doe",
        "key_strengths": "Strong in React, Flask, and REST APIs.",
        "identified_gaps": "Limited exposure to AWS deployment."
      }
    }
  ]
}
```

---

## 🎨 UI Highlights

- Dark mode, responsive layout  
- Tailwind CSS-based design  
- Dynamic color-coded scoring:
  - 🟢 **Shortlisted** (Score ≥ 8)
  - 🟡 **Review** (Score 3–7)
  - 🔴 **Low Match** (Score < 3)

---

## 🧩 Backend Highlights

- Robust Flask server with:
  - ✅ CORS enabled  
  - ✅ Schema validation  
  - ✅ Error handling (API, JSONDecode, Internal errors)
  - ✅ Gemini AI integration with retry handling  
- Outputs clean, structured JSON responses.

---

## 🧾 Environment Variables

| Variable | Description |
|-----------|--------------|
| `GEMINI_API_KEY` | Google Gemini API key (required) |
| `PORT` | Default: `8080` |

---

## 🌍 Deployment Guide

- **Local:** Open `resume_screener_frontend.html` in your browser and run Flask locally.
- **Remote:**  
  - Host backend on Render / Google Cloud Run / AWS Lambda.  
  - Host frontend on Netlify / GitHub Pages.  
  - Update:
    ```js
    const API_URL = 'https://your-deployed-backend.com/analyze';
    ```

---

## 🧪 Future Enhancements

- [ ] Multi-candidate batch screening  
- [ ] Resume file upload (PDF/DOCX parsing)  
- [ ] Cloud deployment template (Docker + Render)  
- [ ] Analytics dashboard (match trends)  

---

## 🤝 Contributing

Contributions are welcome! 🎉  
Follow these steps:

```bash
git checkout -b feature/new-feature
git commit -m "Add new feature"
git push origin feature/new-feature
```

Then open a Pull Request 🚀

---

## 📜 License

This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ using Flask, Tailwind, and Google Gemini</sub>
</p>
