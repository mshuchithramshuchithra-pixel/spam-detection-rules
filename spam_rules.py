from utils import (
    extract_domain, 
    count_urls, 
    has_url_shortener, 
    calculate_uppercase_ratio, 
    count_exclamation_marks, 
    count_suspicious_words
)

# Configuration for scoring and thresholds
SPAM_THRESHOLD = 5
SUSPICIOUS_THRESHOLD = 4

# Predefined lists of suspicious elements
SUSPICIOUS_KEYWORDS = [
    "free", "winner", "urgent", "claim now", "act now", "cash prize", 
    "lottery", "guaranteed", "100%", "click here", "no cost",
    "credit card", "investment", "viagra", "cheap", "discount", "make money"
]

SUSPICIOUS_ATTACHMENTS = [".exe", ".scr", ".zip", ".rar", ".js", ".vbs", ".bat"]

DISPOSABLE_DOMAINS = ["mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com"]


def evaluate_email(sender: str, subject: str, body: str):
    """
    Evaluates an email based on predefined manual rules.
    Returns structurally formatted results containing the score, label, and triggered rules.
    """
    total_score = [0]
    triggered_rules = []

    def trigger(rule_name, score, reason):
        total_score[0] += score
        triggered_rules.append({
            "rule": rule_name,
            "score": score,
            "reason": reason
        })

    # Rule 1: Too many links
    url_count = count_urls(body)
    if url_count > 2:
        score_added = (url_count - 2) * 2  # +2 for every link above 2 (max up to some point, but we keep it simple)
        trigger("Too Many Links", min(score_added, 6), f"Found {url_count} links in the body. Excessive links are suspicious.")

    # Rule 2: Suspicious keywords
    keyword_count = count_suspicious_words(subject + " " + body, SUSPICIOUS_KEYWORDS)
    if keyword_count > 0:
        score_added = min(keyword_count * 2, 6) # Cap the penalty at 6
        trigger("Suspicious Keywords", score_added, f"Found {keyword_count} instances of spammy keywords like 'free', 'urgent', 'winner'.")

    # Rule 3: Excessive uppercase
    upper_ratio = calculate_uppercase_ratio(body)
    if upper_ratio > 0.6 and len([c for c in body if c.isalpha()]) > 10:
        trigger("Excessive Uppercase", 3, f"{int(upper_ratio*100)}% of the letters in the body are uppercase.")

    # Rule 4: Too many exclamation marks
    exclamation_count = count_exclamation_marks(subject + body)
    if exclamation_count > 3:
        trigger("Excessive Exclamations", 2, f"Found {exclamation_count} exclamation marks. Overuse of punctuation is common in spam.")

    # Rule 5: Suspicious sender domain
    domain = extract_domain(sender)
    if domain in DISPOSABLE_DOMAINS:
        trigger("Suspicious Sender Domain", 4, f"Sender domain '{domain}' is a known disposable/temporary email provider.")
    elif domain and sum(1 for c in domain.split('.')[0] if c.isdigit()) > 4:
        trigger("Suspicious Sender Domain", 3, f"Sender domain '{domain}' contains too many numbers, which looks auto-generated.")

    # Rule 6: Very short subject with promotional body
    words_in_subject = subject.split()
    if 0 < len(words_in_subject) <= 2 and keyword_count > 0:
        trigger("Short Subject + Promo Body", 2, "Subject is very short and body contains promotional/suspicious keywords.")

    # Rule 7: Missing subject
    if not subject.strip():
        trigger("Missing Subject", 2, "The email has no subject line.")

    # Rule 8: Urgent subject
    urgent_words = ["urgent", "action required", "immediately", "important update"]
    if count_suspicious_words(subject, urgent_words) > 0:
        trigger("Urgent Subject", 3, "Subject attempts to create a false sense of urgency.")

    # Rule 9: Suspicious attachment mentions
    body_lower = body.lower()
    found_suspicious_ext = False
    for ext in SUSPICIOUS_ATTACHMENTS:
        if ext in body_lower and ("attached" in body_lower or "attachment" in body_lower or "invoice" in body_lower or "document" in body_lower):
            found_suspicious_ext = True
            break
    if found_suspicious_ext:
        trigger("Suspicious Attachment Pattern", 4, "Email mentions attachments and contains dangerous file extensions (.exe, .zip, etc.).")

    # Rule 10: URL Shorteners
    if has_url_shortener(body):
        trigger("URL Shortener", 3, "Email body contains a URL shortener (e.g., bit.ly, tinyurl), often used to hide malicious links.")

    # Determine Label
    if total_score[0] >= SPAM_THRESHOLD:
        label = "Spam"
    elif total_score[0] >= SUSPICIOUS_THRESHOLD:
        label = "Suspicious"
    else:
        label = "Safe"

    return {
        "score": total_score[0],
        "label": label,
        "triggered_rules": triggered_rules,
        "thresholds": {
            "spam": SPAM_THRESHOLD,
            "suspicious": SUSPICIOUS_THRESHOLD
        }
    }
