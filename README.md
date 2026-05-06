# 🛡️ SpamGuard AI

**SpamGuard AI** is a lightweight, intelligent message classification service built with Flask. It provides a robust RESTful API and a premium web interface to detect spam messages based on heuristic rules, keywords, and text patterns.

---

## ✨ Features

- **🚀 Dual Interface**: Use the service via a sleek, modern Web UI or a standard REST API.
- **🔍 Intelligent Scoring**: Analyzes messages based on:
  - **Spam Keywords**: Detection of common phishing and marketing trigger words.
  - **Text Heuristics**: Monitors excessive exclamation marks and uppercase ratios.
  - **Link Analysis**: Identifies suspicious URLs and HTTP patterns.
  - **Contextual Flags**: Recognizes suspicious prefixes like `RE:` or `FWD:` used in phishing.
- **📊 Detailed Feedback**: Returns not just a classification, but a confidence score and a list of specific reasons for the classification.
- **🎨 Premium UI**: A responsive, dark-mode dashboard with smooth animations and real-time feedback.

---

## 🛠️ Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the dependencies:
```bash
# Clone the repository (if applicable)
# git clone <repository-url>
# cd "Spam Detection Service"

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Service
Start the Flask server:
```bash
python spam_detector.py
```
The service will be available at:
- **Web UI**: [http://localhost:7003](http://localhost:7003)
- **API Endpoint**: `http://localhost:7003/detect-spam`

---

## 🔌 API Documentation

### Detect Spam
**Endpoint:** `POST /detect-spam`

**Request Body:**
```json
{
  "message": "Congratulations! You've won a free prize. Click here now!"
}
```

**Response Body:**
```json
{
  "classification": "SPAM",
  "is_spam": true,
  "message": "Congratulations! You've won a free prize. Click here now!",
  "reasons": [
    "Spam keywords found: free, won, prize, click here, congratulations",
    "Excessive exclamation marks: 2",
    "Contains 0 link(s)"
  ],
  "spam_score": 75
}
```

---

## 🧪 Testing

You can run the included test script to verify the API functionality:
```bash
python test_api.py
```

---

## 💻 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, Vanilla CSS (Premium Dark Theme), JavaScript (Fetch API)
- **Middleware**: Flask-CORS for cross-origin support

---

## 📝 License
This project is open-source and available under the MIT License.
