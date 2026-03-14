import re

def extract_domain(email: str) -> str:
    """Extracts the domain part from an email address."""
    if not email or '@' not in email:
        return ""
    return email.split('@')[-1].strip().lower()

def count_urls(text: str) -> int:
    """Counts the number of URLs present in the text using a simple regex."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|www\.[-\w.]+')
    return len(url_pattern.findall(text))

def has_url_shortener(text: str) -> bool:
    """Checks if the text contains common URL shorteners."""
    shortener_domains = [
        'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 
        'ow.ly', 'is.gd', 'buff.ly', 'adf.ly'
    ]
    text_lower = text.lower()
    for shortener in shortener_domains:
        if shortener in text_lower:
            return True
    return False

def calculate_uppercase_ratio(text: str) -> float:
    """Calculates the ratio of uppercase letters to total alphabet characters."""
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return 0.0
    uppercase_count = sum(1 for char in letters if char.isupper())
    return uppercase_count / len(letters)

def count_exclamation_marks(text: str) -> int:
    """Counts the number of exclamation marks in the text."""
    return text.count('!')

def count_suspicious_words(text: str, word_list: list) -> int:
    """Counts how many times suspicious words from a list appear in the text."""
    text_lower = text.lower()
    count = 0
    for word in word_list:
        # Use regex to find whole words where possible
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        count += len(re.findall(pattern, text_lower))
    return count
