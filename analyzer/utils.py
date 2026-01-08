import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pandas as pd
from collections import Counter


def analyze_text_complexity(text):
    """
    Analyzes text and returns stats and a base64 encoded plot.
    """
    if not text:
        return 0, 0, None

    # Basic cleaning and tokenization
    words = text.split()
    word_count = len(words)
    sentence_count = text.count(".") + text.count("!") + text.count("?")
    if sentence_count == 0:
        sentence_count = 1

    # Analysis with Pandas
    df = pd.DataFrame({"word": words})
    df["length"] = df["word"].str.len()

    # Generate Plot: Word Length Distribution
    plt.figure(figsize=(6, 4))
    df["length"].plot(
        kind="hist",
        bins=10,
        title="Word Length Distribution",
        color="skyblue",
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

    return word_count, sentence_count, graphic
