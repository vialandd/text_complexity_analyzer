"""
Utility functions for text complexity analysis using Pandas and Matplotlib.
"""
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sentinel_tokenize

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def analyze_text_complexity(text):
    """
    Analyzes text and returns stats and a base64 encoded plot.

    Args:
        text (str): The text content to analyze.

    Returns:
        dict: A dictionary containing various metrics and the graph.
    """
    if not text:
        return {}

    # Tokenization
    try:
        words = word_tokenize(text)
        sentences = sentinel_tokenize(text)
    except LookupError:
        # Fallback if NLTK fails for some reason
        words = text.split()
        sentences = text.split('.')

    word_count = len(words)
    sentence_count = len(sentences)

    # 1. Consonant Analysis
    vowels = set("aeiouAEIOU")
    consonant_count = sum(1 for char in text if char.isalpha() and char not in vowels)
    
    # 2. Lexical Diversity (Type-Token Ratio)
    # Filter out non-alphabetic tokens for fairer comparison
    alpha_words = [w.lower() for w in words if w.isalpha()]
    if alpha_words:
        unique_words = len(set(alpha_words))
        lexical_diversity = round(unique_words / len(alpha_words), 2)
    else:
        lexical_diversity = 0.0

    # 3. Rare Word Density (using NLTK stopwords as "common")
    stop_words = set(stopwords.words('english'))
    # "Complex" words are those NOT in stopwords (simplified definition)
    complex_words_count = sum(1 for w in alpha_words if w not in stop_words)
    rare_word_ratio = round(complex_words_count / len(alpha_words), 2) if alpha_words else 0.0

    # 4. Flesch Reading Ease
    flesch_score = textstat.flesch_reading_ease(text)

    # Analysis with Pandas for Graph
    df = pd.DataFrame({"word": alpha_words})
    if not df.empty:
        df["length"] = df["word"].str.len()
        
        # Generate Plot: Word Length Distribution
        plt.figure(figsize=(6, 4))
        df["length"].plot(
            kind="hist",
            bins=10,
            title="Word Length Distribution",
            color="#198754", # Success green
            edgecolor="black",
        )
        plt.xlabel("Length of Word")
        plt.ylabel("Frequency")
        plt.tight_layout()

        # Save to base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        graphic = base64.b64encode(image_png).decode("utf-8")
    else:
        graphic = None

    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'consonant_count': consonant_count,
        'lexical_diversity': lexical_diversity,
        'rare_word_ratio': rare_word_ratio,
        'flesch_score': flesch_score,
        'graph': graphic
    }


