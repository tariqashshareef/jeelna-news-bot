"""De-duplicates articles, keeping the first of each instance."""

def dedup(articles):
    """
    Removes exact and near-duplicate articles via a cutoff in title overlap.

    Args:
        articles: A list of article dicts.

    Returns:
        A new de-duplicated list of article dicts.
    """
    
    cutoff = 0.2
    kept = []
    kept_words = []

    for article in articles:
        words = set(article["title"].lower().split())
        is_dup = False

        for other in kept_words:
            if len(words & other) / len(words | other) >= cutoff:
                is_dup = True
                break

        if not is_dup:
            kept.append(article)
            kept_words.append(words)

    return kept