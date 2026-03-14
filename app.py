import streamlit as st
import json
import os
from spam_rules import evaluate_email

# Set page configuration
st.set_page_config(page_title="Rule-Based Spam Detector", page_icon="🛡️", layout="centered")

def load_sample_inputs():
    """Loads sample emails from the JSON file."""
    file_path = "sample_inputs.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# Application Header
st.title("🛡️ Email Spam Detection App")
st.markdown("""
Welcome to the rule-based Email Spam Detection system.
This project analyzes the sender, subject, and body of an email to determine if it is **Safe**, **Suspicious**, or **Spam** based on heuristic rules.
No machine learning is used—only pure logic and scoring!
""")

st.divider()

# Load samples
samples = load_sample_inputs()
sample_options = ["None (Manual Entry)"] + [sample["name"] for sample in samples]

st.sidebar.header("📁 Load Sample Emails")
st.sidebar.markdown("Use this to quickly test different cases without typing.")
selected_sample_name = st.sidebar.selectbox("Choose a sample:", sample_options)

# Pre-fill data if a sample is selected
default_sender = ""
default_subject = ""
default_body = ""

if selected_sample_name != "None (Manual Entry)":
    # Find the corresponding sample
    for sample in samples:
        if sample["name"] == selected_sample_name:
            default_sender = sample["sender"]
            default_subject = sample["subject"]
            default_body = sample["body"]
            break

# Input Form
st.header("📝 Email Details")

sender_input = st.text_input("Sender Email Address", value=default_sender, placeholder="e.g., mail@example.com")
subject_input = st.text_input("Email Subject", value=default_subject, placeholder="e.g., Important update about your account")
body_input = st.text_area("Email Body", value=default_body, height=200, placeholder="Paste the email content here...")

# Analysis Section
if st.button("🔍 Analyze Email", type="primary"):
    if not sender_input and not subject_input and not body_input:
        st.warning("Please enter at least some email content to analyze.")
    else:
        with st.spinner("Analyzing email..."):
            # Run the engine
            result = evaluate_email(sender_input, subject_input, body_input)

            st.divider()
            
            # Display Results Container
            st.header("📊 Analysis Result")
            
            # Label visualization
            label = result["label"]
            score = result["score"]
            
            if label == "Spam":
                st.error(f"**Classification: {label}**")
            elif label == "Suspicious":
                st.warning(f"**Classification: {label}**")
            else:
                st.success(f"**Classification: {label}**")
            
            # Score visualization
            st.metric(label="Total Spam Score", value=score)
            
            # Explanation of rules triggered
            st.subheader("🚨 Triggered Rules (" + str(len(result["triggered_rules"])) + ")")
            
            if len(result["triggered_rules"]) == 0:
                st.info("No suspicious patterns were detected in this email.")
            else:
                for rule in result["triggered_rules"]:
                    with st.expander(f"{rule['rule']} (+{rule['score']} pts)", expanded=True):
                        st.write(rule["reason"])
            
            # Threshold information
            st.caption(f"Score > {result['thresholds']['suspicious']} = Suspicious | Score > {result['thresholds']['spam']} = Spam")

st.sidebar.divider()
st.sidebar.info("Built for demonstration purposes. This uses a purely rule-based approach.")
