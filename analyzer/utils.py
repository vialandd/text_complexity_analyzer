"""
Utility functions for text complexity analysis using Pandas and Matplotlib.
"""
import base64
from io import BytesIO
from collections import Counter
import matplotlib
matplotlib.use('Agg') # Set backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from nltk.sentiment import SentimentIntensityAnalyzer

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
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')
try:
    nltk.data.find('chunkers/maxent_ne_chunker_tab')
except LookupError:
    nltk.download('maxent_ne_chunker_tab')
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')
try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')

# --- Global Frequency Data (Lazy Loading Pattern) ---
from nltk.corpus import brown
_WORD_RANKINGS = None

def get_word_rankings():
    """
    Returns a dictionary mapping words to their frequency rank based on the Brown corpus.
    Low rank = Frequent (e.g., 'the' is 1).
    """
    global _WORD_RANKINGS
    if _WORD_RANKINGS is None:
        # Build frequency distribution from Brown corpus
        # Case insensitive to capture general usage
        print("Building frequency distribution from Brown corpus...")
        freq_dist = nltk.FreqDist(w.lower() for w in brown.words() if w.isalpha())
        # Create rank map: {word: rank}
        # most_common returns [(word, count), ...]
        common_words = [w for w, c in freq_dist.most_common()]
        _WORD_RANKINGS = {word: rank for rank, word in enumerate(common_words, 1)}
    return _WORD_RANKINGS

def get_word_rarity_label(rank):
    if rank <= 1000:
        return "Common"
    elif rank <= 5000:
        return "Intermediate"
    else:
        return "Advanced/Rare"

def calculate_jaccard(sent1, sent2):
    """Calculates Jaccard similarity between two sentences."""
    words1 = set(word_tokenize(sent1.lower()))
    words2 = set(word_tokenize(sent2.lower()))
    if not words1 or not words2:
        return 0.0
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)

def analyze_text_complexity(text):
    """
    Analyzes text and returns stats structured by category.

    Args:
        text (str): The text content to analyze.

    Returns:
        dict: A dictionary containing categorized metrics.
    """
    if not text:
        return {}

    # --- Preprocessing ---
    try:
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
    except LookupError:
        words = text.split()
        sentences = text.split('.')

    vowels = set("aeiouAEIOU")
    alpha_words = [w.lower() for w in words if w.isalpha()]
    stop_words = set(stopwords.words('english'))

    # --- 1. General Stats ---
    word_count = len(words)
    sentence_count = len(sentences)
    
    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    
    # Consonants
    if alpha_words:
        total_consonants = sum(1 for char in text if char.isalpha() and char not in vowels)
        avg_consonants = round(total_consonants / len(alpha_words), 2)
    else:
        avg_consonants = 0.0

    # --- 2. Reading & Complexity ---
    flesch_score = textstat.flesch_reading_ease(text)
    # Round for display
    flesch_score = round(flesch_score, 1)
    # Clamp for progress bar (0 to 100)
    flesch_progress = max(0, min(100, flesch_score))
    
    # Jaccard Index (Cohesion)
    total_jaccard = 0.0
    if len(sentences) > 1:
        for i in range(len(sentences) - 1):
            total_jaccard += calculate_jaccard(sentences[i], sentences[i+1])
        avg_jaccard = round(total_jaccard / (len(sentences) - 1), 3)
    else:
        avg_jaccard = 1.0

    # Sentence Highlighting & Complexity Scope
    highlighted_sentences = []
    
    # Identify frequent words for highlighting (Top 5 non-stopwords, count > 1)
    if alpha_words:
        word_counts = Counter(w for w in alpha_words if w not in stop_words)
        # set of top words for O(1) lookup
        top_words_set = {word for word, count in word_counts.most_common(5) if count > 1}
    else:
        top_words_set = set()

    max_sent_len = max(len(word_tokenize(s)) for s in sentences) if sentences else 1

    for sent in sentences:
        sent_tokens = word_tokenize(sent)
        sent_words_alpha = [w.lower() for w in sent_tokens if w.isalpha()]
        sent_len = len(sent_words_alpha)
        
        # Calculate Complexity Score (0.0 to 1.0)
        # Factors: Length (>20 is hard), Complex words (>6 chars)
        complex_count = sum(1 for w in sent_words_alpha if len(w) > 6)
        
        # Heuristic: 
        # Length score: 20 words = 0.5
        # Compexity score: 4 complex words = 0.5
        len_score = min(sent_len / 30, 0.6)
        comp_score = min(complex_count / 8, 0.4)
        
        total_score = len_score + comp_score
        # Cap opacity at 0.6 to keep text readable
        opacity = min(total_score, 0.6) 
        # Normalize to 0 if very simple
        if sent_len < 8 and complex_count < 2:
            opacity = 0

        # Highlight frequent words within the sentence string
        # We assume standard spacing for simplicity in reconstruction or just replace tokens
        # A safer way to preserve punctuation is iterating tokens
        formatted_sent = []
        for token in sent_tokens:
            if token.lower() in top_words_set:
                formatted_sent.append(f"<strong class='text-primary' title='Frequent word'>{token}</strong>")
            else:
                formatted_sent.append(token)
        
        # Reconstruct roughly (NLTK doesn't perfectly reconstruct, but this is a visualization tool)
        # Using a simple join is often 'good enough' for analysis view, 
        # or we could use the original text slicing if we had offsets.
        # For simplicity/robustness here, we'll join with spaces and fix puntuation manually if needed,
        # or simplified: just trust space joining for the 'visual' representation.
        # NLTK's TreebankWordDetokenizer is better if available (downloaded?). 
        # Let's try simple join but handles punctuation naively.
        
        # Better approach: string replace on the original sentence segment? 
        # Risk of matching substrings.
        # Let's stick to token join for the visual highlighting, even if perfect spacing is lost.
        from nltk.tokenize.treebank import TreebankWordDetokenizer
        try:
            display_text = TreebankWordDetokenizer().detokenize(formatted_sent)
        except:
            display_text = " ".join(formatted_sent)

        highlighted_sentences.append({
            'text': display_text,
            'complexity_score': round(total_score * 10, 1), # 0-10 scale for tooltip
            'opacity': round(opacity, 2)
        })

    # --- 3. Lexical Structure ---
    # Diversity & Rare Words
    if alpha_words:
        unique_words = len(set(alpha_words))
        lexical_diversity = round(unique_words / len(alpha_words), 2)
        complex_words_count = sum(1 for w in alpha_words if w not in stop_words)
        rare_word_ratio = round(complex_words_count / len(alpha_words), 2)
    else:
        lexical_diversity = 0.0
        rare_word_ratio = 0.0

    # POS Tagging & Graph
    content_ratio = 0.0
    pos_graph = None
    if alpha_words:
        pos_tags = nltk.pos_tag(alpha_words, tagset='universal')
        pos_counts = pd.Series([tag for word, tag in pos_tags]).value_counts()
        
        content_tags = {"NOUN", "VERB", "ADJ", "ADV"}
        content_count = sum(1 for tag in pos_tags if tag[1] in content_tags)
        content_ratio = round(content_count / len(alpha_words), 2)
        
        plt.figure(figsize=(8, 6)) # Increased size
        pos_counts.head(5).plot(kind="pie", autopct='%1.1f%%', title="Top 5 Reading Roles")
        plt.ylabel("")
        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches='tight')
        buffer.seek(0)
        pos_graph = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        plt.close()

    # Word Length Graph
    len_graph = None
    df = pd.DataFrame({"word": alpha_words})
    if not df.empty:
        df["length"] = df["word"].str.len()
        plt.figure(figsize=(10, 6)) # Increased size
        df["length"].plot(kind="hist", bins=15, title="Word Length Distribution", color="#198754", edgecolor="black")
        plt.xlabel("Length of Word")
        plt.ylabel("Frequency")
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        len_graph = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        plt.close()

    # --- 4. Advanced (N-grams & Entities) ---
    # N-grams > 1 occurrence
    repeating_bigrams = []
    repeating_trigrams = []
    if len(alpha_words) > 2:
        bigram_counts = Counter(ngrams(alpha_words, 2))
        trigram_counts = Counter(ngrams(alpha_words, 3))
        
        repeating_bigrams = [
            f"{bg[0]} {bg[1]} ({count})" 
            for bg, count in bigram_counts.most_common(5) if count > 1
        ]
        repeating_trigrams = [
            f"{tg[0]} {tg[1]} {tg[2]} ({count})" 
            for tg, count in trigram_counts.most_common(5) if count > 1
        ]

    # Named Entities
    entities = []
    if alpha_words:
        # We need case-sensitive tagging for NER, so use original words but stripped of punctuation
        orig_words = [w for w in words if w.isalpha()]
        try:
            tagged = nltk.pos_tag(orig_words)
            chunked = nltk.ne_chunk(tagged)
            for chunk in chunked:
                if hasattr(chunk, 'label'):
                    entities.append(f"{' '.join(c[0] for c in chunk)} ({chunk.label()})")
        except Exception:
            pass # NER can be fragile

    # --- 5. Global Corpus Comparison (Frequency Analysis) ---
    word_rarity_dist = {"Common": 0, "Intermediate": 0, "Advanced/Rare": 0}
    
    # Load rankings (cached)
    rankings = get_word_rankings()
    
    for word in alpha_words:
        # Check rank vs Brown corpus
        rank = rankings.get(word, 999999) # Default to very rare if not in corpus
        label = get_word_rarity_label(rank)
        word_rarity_dist[label] += 1
    
    # Normalize to percentages
    total_alpha = len(alpha_words) if alpha_words else 1
    rarity_stats = {
        k: round((v / total_alpha) * 100, 1) for k, v in word_rarity_dist.items()
    }
    
    # Generate Rarity Bar Chart
    freq_graph = None
    if alpha_words:
        plt.figure(figsize=(8, 4))
        plt.bar(rarity_stats.keys(), rarity_stats.values(), color=['#198754', '#ffc107', '#dc3545'])
        plt.title("Vocabulary Complexity vs. Standard English")
        plt.ylabel("Percentage (%)")
        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches='tight')
        buffer.seek(0)
        freq_graph = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        plt.close()

    return {
        'general': {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_consonants': avg_consonants,
            'sentiment': sentiment, # dict: neg, neu, pos, compound
        },
        'reading': {
            'flesch_score': flesch_score,
            'flesch_progress': flesch_progress,
            'avg_jaccard': avg_jaccard,
            'highlighted_sentences': highlighted_sentences,
        },
        'lexical': {
            'diversity': lexical_diversity,
            'rare_ratio': rare_word_ratio,
            'content_ratio': content_ratio,
            'pos_graph': pos_graph,
            'len_graph': len_graph,
        },
        'advanced': {
            'bigrams': repeating_bigrams,
            'trigrams': repeating_trigrams,
            'entities': sorted(list(set(entities))), # Deduplicate
            'rarity_stats': rarity_stats,
            'freq_graph': freq_graph,
        }
    }


