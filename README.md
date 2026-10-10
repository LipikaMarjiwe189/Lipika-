# 🎓 SmartStudy AI

> An AI-powered study assistant that helps students understand programming
> concepts faster — built with Python, Streamlit, and Google Gemini.

---

## ✨ Features

| Feature | What it does |
|---|---|
| 💡 **Explain a Topic** | Get beginner-friendly explanations with real-world analogies |
| 📄 **Summarize Notes** | Paste raw notes → get a concise summary + key bullet points |
| 🐍 **Code Explainer** | Paste Python code → get a line-by-line English explanation |
| 📝 **Practice Quiz** | Generate multiple-choice quizzes on any topic |

---

## 📁 Project Structure

```
smartstudy_ai/
├── app.py              ← Streamlit UI + feature pages
├── ai_helper.py        ← All Gemini AI API calls
├── utils.py            ← Small shared helper functions
├── .env.example        ← Template for your API key
├── .env                ← YOUR real key (never share this file!)
├── requirements.txt    ← Python dependencies
└── README.md           ← This guide
```

---

## 🚀 Setup Instructions (VS Code)

### Step 1 — Prerequisites

Make sure you have the following installed:
- **Python 3.9 or newer** → https://www.python.org/downloads/
- **VS Code** → https://code.visualstudio.com/

Verify Python is installed by opening a terminal and running:
```
python --version
```

---

### Step 2 — Open the project in VS Code

1. Open VS Code.
2. Go to **File → Open Folder** and select the `smartstudy_ai` folder.
3. Open the integrated terminal: **Terminal → New Terminal** (or press `` Ctrl+` ``).

---

### Step 3 — Create a virtual environment (recommended)

A virtual environment keeps project packages separate from your system Python.

```bash
# Create the virtual environment
python -m venv venv

# Activate it  (Windows)
venv\Scripts\activate

# Activate it  (macOS / Linux)
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **streamlit** — builds the web UI
- **google-generativeai** — talks to the Gemini AI API
- **python-dotenv** — loads your secret API key from the `.env` file

---

### Step 5 — Get a free Gemini API key 🔑

> ⚠️  **The AI features will NOT work until you complete this step.**

1. Visit **https://aistudio.google.com/app/apikey** (free, no credit card needed).
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy the key that appears.

---

### Step 6 — Configure the API key securely

1. In the `smartstudy_ai/` folder, create a new file called **`.env`**.
2. Open it and add exactly this line (replace the placeholder with your real key):

```
GEMINI_API_KEY=AIzaSy_paste_your_real_key_here
```

3. Save the file.

> 🔒 **Security note:** The `.env` file is listed in `.gitignore` and will
> never be committed to GitHub. Your key stays on your machine only.

---

### Step 7 — Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`).
Open that URL in your browser — the app will load automatically.

---

## 🧠 How the code works (plain English)

| File | What it does in simple words |
|---|---|
| `app.py` | The "front door" of the app. Streamlit reads this file and draws the web page. The sidebar navigation decides which section to show. |
| `ai_helper.py` | The "brain". Each function builds a text prompt, sends it to Gemini, and returns the answer. |
| `utils.py` | Small tools used everywhere — checking if the key exists, counting words, cleaning up text. |
| `.env` | A tiny text file that holds your secret API key. Never shown in the UI or pushed to GitHub. |
| `requirements.txt` | A shopping list of Python packages. `pip` reads it and installs everything at once. |

---

## ❓ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` again |
| `❌ API Key missing` shown in sidebar | Check your `.env` file exists and the key is correct |
| `400 API_KEY_INVALID` error | Your key was copied incorrectly — regenerate it at aistudio.google.com |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |

---

## 📜 License

Free to use for learning and personal projects.
