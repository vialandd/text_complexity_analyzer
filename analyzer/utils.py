"""
Utility functions for text complexity analysis using Pandas and Matplotlib.
"""
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg') # Set backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng')
try:
    nltk.data.find('taggers/universal_tagset')
except LookupError:
    nltk.download('universal_tagset')

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
        sentences = sent_tokenize(text)
    except LookupError:
        # Fallback if NLTK fails for some reason
        words = text.split()
        sentences = text.split('.')

    word_count = len(words)
    sentence_count = len(sentences)

    # 1. Consonant Analysis (Average per word)
    vowels = set("aeiouAEIOU")
    alpha_words = [w.lower() for w in words if w.isalpha()]
    
    if alpha_words:
        total_consonants = sum(1 for char in text if char.isalpha() and char not in vowels)
        avg_consonants = round(total_consonants / len(alpha_words), 2)
    else:
        avg_consonants = 0.0
    
    # 2. Part of Speech Tagging
    if alpha_words:
        pos_tags = nltk.pos_tag(alpha_words, tagset='universal')
        pos_counts = pd.Series([tag for word, tag in pos_tags]).value_counts()
        
        # Calculate ratios
        content_tags = {"NOUN", "VERB", "ADJ", "ADV"}
        content_count = sum(1 for tag in pos_tags if tag[1] in content_tags)
        content_ratio = round(content_count / len(alpha_words), 2)
        
        # Generate Pie Chart for POS
        plt.figure(figsize=(6, 4))
        pos_counts.head(5).plot(
            kind="pie", 
            autopct='%1.1f%%', 
            title="Top 5 Reading Roles"
        )
        plt.ylabel("")
        
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        pos_graph = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        plt.close()
    else:
        content_ratio = 0.0
        pos_graph = None

    # 3. Sentence Difficulty Highlighting
    # A sentence is "hard" if it has > 20 words or > 3 complex words (length > 6)
    highlighted_sentences = []
    for sent in sentences:
        sent_words = [w for w in word_tokenize(sent) if w.isalpha()]
        is_hard = False
        if len(sent_words) > 20:
            is_hard = True
        else:
            complex_in_sent = sum(1 for w in sent_words if len(w) > 6)
            if complex_in_sent > 3:
                is_hard = True
        
        highlighted_sentences.append({
            'text': sent,
            'is_hard': is_hard
        })

    # 4. Lexical Diversity (Type-Token Ratio)
    # Filter out non-alphabetic tokens for fairer comparison
    if alpha_words:
        unique_words = len(set(alpha_words))
        lexical_diversity = round(unique_words / len(alpha_words), 2)
    else:
        lexical_diversity = 0.0

    # 5. Rare Word Density (using NLTK stopwords as "common")
    stop_words = set(stopwords.words('english'))
    # "Complex" words are those NOT in stopwords (simplified definition)
    complex_words_count = sum(1 for w in alpha_words if w not in stop_words)
    rare_word_ratio = round(complex_words_count / len(alpha_words), 2) if alpha_words else 0.0

    # 6. Flesch Reading Ease
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
        'avg_consonants': avg_consonants,
        'lexical_diversity': lexical_diversity,
        'rare_word_ratio': rare_word_ratio,
        'flesch_score': flesch_score,
        'graph': graphic,
        'highlighted_sentences': highlighted_sentences,
        'content_ratio': content_ratio,
        'pos_graph': pos_graph,
    }


