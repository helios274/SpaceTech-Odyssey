import re
import uuid
from django.utils.text import slugify


def capitalize_words(text):
    def capitalize_word(match):
        word = match.group(0)
        # Check if the word is not fully uppercase
        if not word.isupper():
            return word.capitalize()
        return word

    # Use regex to match words
    return re.sub(r'\b\w+\b', capitalize_word, text)


def generate_slug(title):
    words = title.split()[:8]
    slug = slugify(' '.join(words))
    short_uuid = uuid.uuid4().hex[:8]
    return f"{slug}-{short_uuid}"
