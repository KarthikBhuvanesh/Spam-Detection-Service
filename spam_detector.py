from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# Expanded Spam keywords
SPAM_KEYWORDS = [
    'free', 'winner', 'won', 'prize', 'click here', 'urgent',
    'limited offer', 'earn money', 'cash prize', 'congratulations',
    'buy now', 'exclusive deal', 'no risk', 'guaranteed',
    '100% free', 'act now', 'apply now', 'claim your', 'bitcoin',
    'crypto', 'investment', 'double your', 'unlimited', 'expire',
    'instant', 'bonus', 'rewards', 'inheritance', 'lottery'
]

def detect_spam(message):
    if not message:
        return False, 0, ["Empty message"]
        
    text_lower = message.lower()
    score = 0
    reasons = []

    # 1. Check spam keywords
    matched = [kw for kw in SPAM_KEYWORDS if kw in text_lower]
    if matched:
        # Give more weight to unique matches
        score += len(set(matched)) * 15
        reasons.append(f"Spam keywords found: {', '.join(list(set(matched))[:5])}")

    # 2. Excessive exclamation marks
    excl = message.count('!')
    if excl > 2:
        score += min(excl * 5, 25)
        reasons.append(f"Excessive exclamation marks: {excl}")

    # 3. Excessive uppercase (more than 30% of letters)
    letters = [c for c in message if c.isalpha()]
    if letters:
        upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        if upper_ratio > 0.3 and len(message) > 10:
            score += 30
            reasons.append(f"High uppercase ratio: {upper_ratio:.0%}")

    # 4. URLs / suspicious links
    urls = re.findall(r'http[s]?://|www\.', text_lower)
    if urls:
        score += len(urls) * 20
        reasons.append(f"Contains {len(urls)} link(s)")

    # 5. Check for "re: " or "fwd: " in subject-like lines (often used in phishing)
    if text_lower.startswith(('re:', 'fwd:')):
        score += 10
        reasons.append("Suspicious prefix (RE/FWD)")

    is_spam = score >= 40
    # Cap score at 100
    final_score = min(score, 100)
    
    return is_spam, final_score, reasons

# Premium UI for the Service
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpamGuard AI | Detection Service</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-dim: #94a3b8;
            --success: #22c55e;
            --danger: #ef4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow: hidden;
        }

        /* Animated Background Gradients */
        .bg-glow {
            position: fixed;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(15, 23, 42, 0) 70%);
            border-radius: 50%;
            z-index: -1;
            filter: blur(80px);
            animation: move 20s infinite alternate;
        }

        @keyframes move {
            from { transform: translate(-30%, -30%); }
            to { transform: translate(30%, 30%); }
        }

        .container {
            width: 100%;
            max-width: 600px;
            background: var(--card-bg);
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transform: translateY(0);
            transition: transform 0.3s ease;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 8px;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        p.subtitle {
            color: var(--text-dim);
            margin-bottom: 32px;
            font-size: 1.1rem;
        }

        .input-group {
            margin-bottom: 24px;
        }

        textarea {
            width: 100%;
            height: 150px;
            background: rgba(15, 23, 42, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 16px;
            color: white;
            font-size: 1rem;
            resize: none;
            transition: all 0.3s ease;
            outline: none;
        }

        textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
        }

        button {
            width: 100%;
            background: var(--primary);
            color: white;
            border: none;
            padding: 16px;
            border-radius: 16px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }

        button:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        #result {
            margin-top: 32px;
            display: none;
            padding: 24px;
            border-radius: 16px;
            animation: slideUp 0.4s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .badge {
            padding: 6px 16px;
            border-radius: 100px;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-spam { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid var(--danger); }
        .badge-ham { background: rgba(34, 197, 94, 0.2); color: var(--success); border: 1px solid var(--success); }

        .score-bar-container {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin-bottom: 16px;
            overflow: hidden;
        }

        .score-bar {
            height: 100%;
            width: 0%;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .reasons-list {
            list-style: none;
            color: var(--text-dim);
            font-size: 0.9rem;
        }

        .reasons-list li {
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .reasons-list li::before {
            content: "•";
            color: var(--primary);
        }

        .loading {
            opacity: 0.7;
            pointer-events: none;
        }

        .loader {
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="container">
        <h1>SpamGuard AI</h1>
        <p class="subtitle">Intelligent message classification service</p>
        
        <div class="input-group">
            <textarea id="messageInput" placeholder="Paste your suspicious message here..."></textarea>
        </div>
        
        <button onclick="detectSpam()" id="submitBtn">
            <span id="btnText">Analyze Message</span>
            <div class="loader" id="loader"></div>
        </button>

        <div id="result">
            <div class="result-header">
                <span id="classificationText" style="font-size: 1.25rem; font-weight: 600;"></span>
                <span id="badge" class="badge"></span>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 0.9rem; color: var(--text-dim);">Spam Probability</span>
                <span id="scoreText" style="font-weight: 600;"></span>
            </div>
            <div class="score-bar-container">
                <div id="scoreBar" class="score-bar"></div>
            </div>

            <div id="reasonsContainer">
                <p style="font-size: 0.9rem; margin-bottom: 8px; font-weight: 600;">Detection Flags:</p>
                <ul id="reasonsList" class="reasons-list"></ul>
            </div>
        </div>
    </div>

    <script>
        async function detectSpam() {
            const message = document.getElementById('messageInput').value;
            if (!message.trim()) return;

            const btn = document.getElementById('submitBtn');
            const loader = document.getElementById('loader');
            const btnText = document.getElementById('btnText');
            const resultDiv = document.getElementById('result');

            // UI Loading State
            btn.classList.add('loading');
            loader.style.display = 'block';
            btnText.style.display = 'none';

            try {
                const response = await fetch('/detect-spam', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                
                // Update UI with results
                resultDiv.style.display = 'block';
                const classification = document.getElementById('classificationText');
                const badge = document.getElementById('badge');
                const scoreBar = document.getElementById('scoreBar');
                const scoreText = document.getElementById('scoreText');
                const reasonsList = document.getElementById('reasonsList');

                classification.textContent = data.is_spam ? 'Potential Spam Detected' : 'Message Appears Safe';
                badge.textContent = data.classification;
                badge.className = 'badge ' + (data.is_spam ? 'badge-spam' : 'badge-ham');
                
                scoreText.textContent = data.spam_score + '%';
                scoreBar.style.width = data.spam_score + '%';
                scoreBar.style.backgroundColor = data.is_spam ? 'var(--danger)' : 'var(--success)';

                reasonsList.innerHTML = '';
                if (data.reasons.length > 0) {
                    data.reasons.forEach(reason => {
                        const li = document.createElement('li');
                        li.textContent = reason;
                        reasonsList.appendChild(li);
                    });
                } else {
                    const li = document.createElement('li');
                    li.textContent = 'No obvious spam indicators found.';
                    reasonsList.appendChild(li);
                }

            } catch (error) {
                alert('Error connecting to the service');
            } finally {
                btn.classList.remove('loading');
                loader.style.display = 'none';
                btnText.style.display = 'block';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/detect-spam', methods=['POST'])
def detect():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message field'}), 400

    message = data['message']
    is_spam, score, reasons = detect_spam(message)

    return jsonify({
        'message': message,
        'is_spam': is_spam,
        'spam_score': score,
        'classification': 'SPAM' if is_spam else 'NOT SPAM',
        'reasons': reasons
    })

if __name__ == '__main__':
    print("Spam Detection Service is running at http://localhost:7003")
    app.run(port=7003, debug=True)
