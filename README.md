# Rule-Based Email Spam Detection App

## 🎯 Objective
The objective of this project is to build a complete, locally runnable email spam detection application using a **purely rule-based approach**. This means no machine learning models or external APIs are used. Instead, the system relies on predefined logical heuristics and a scoring engine to classify emails as **Safe**, **Suspicious**, or **Spam**.

## 🧠 Approach Used
We implemented an evaluation engine (`spam_rules.py`) that checks the input email (sender, subject, and body) against a set of 10 practical rules. Each triggered rule adds to a total "spam score". 
If the total score crosses specific thresholds, the email is classified accordingly. The system provides transparency by listing the exact rules triggered and the reasons why.

## ✨ Features
- **Streamlit Web UI**: A clean, beginner-friendly interface to input emails and view results.
- **Rule-Based Engine**: Over 10 custom heuristic rules, covering:
  - Excessive links or use of URL shorteners.
  - Suspicious keywords (e.g., "winner", "urgent", "free").
  - Excessive uppercase letters or exclamation marks.
  - Suspicious sender domains (e.g., disposable emails, heavily numbered domains).
  - Short subjects masking promotional content.
  - Urgent/Manipulative subject lines.
  - Suspicious file attachment mentions.
- **Explainability**: Shows exactly which rules were matched and what score they added.
- **Sample Loader**: Allows users to quickly load test emails from a JSON file.

## 📂 Folder Structure
```text
spam-detection/
├── app.py                 # Streamlit application UI
├── spam_rules.py          # Core scoring engine and rule definitions
├── utils.py               # Helper text processing functions
├── sample_inputs.json     # Pre-made sample emails for easy testing
├── requirements.txt       # Project dependencies
├── .gitignore             # Standard Python ignore file
└── README.md              # Project documentation
```

## 🚀 Installation Steps

1. **Clone or Download the Repository**
2. **Ensure Python 3 is installed**
3. **Open a terminal in the project folder**
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 How to Run
Run the application locally using Streamlit:
```bash
streamlit run app.py
```
This will start a local web server and automatically open the app in your default web browser (typically at http://localhost:8501).

## 💡 Example Use Case
- **Input**: Sender is `winner@freeprize.xyz`, Subject is `URGENT: WINNER`, Body contains multiple links and words like `Click here`.
- **Process**: The system calculates points: Urgent subject (+3), Suspicious keywords (+2), Excessive exclamations (+2). Total score: 7.
- **Output**: The email is flagged as "Suspicious" (or "Spam" based on threshold) and clearly shows the breakdown of the score.

## ⚠️ Limitations
- **Brittle Rules**: Attackers can easily bypass these rules by slightly modifying their spelling or tactics.
- **False Positives/Negatives**: Manual rules lack the nuance of contextual understanding, potentially flagging legitimate marketing emails or missing sophisticated phishing attempts.
- **Hard to Maintain**: As spamming techniques evolve, adding new manual rules becomes difficult and complex.

## 🔮 Future Improvements
- **Integrate Machine Learning**: Use an NLP classification model (e.g., Naive Bayes or a Transformer model) alongside rules for better contextual understanding.
- **Reputation APIs**: Add checks against known global blocklists (DNSBL) or malicious link APIs (e.g., Google Safe Browsing).
- **Dynamic Thresholding**: Adjust scoring weights dynamically based on user feedback.
