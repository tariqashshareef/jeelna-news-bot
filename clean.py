"""Cleans articles with faulty or missing data."""

def clean(articles):
    """
    Removes articles with nulls, repeated urls, and consent pages.

    Args:
        articles: A list of article dicts.

    Returns:
        A new cleaned list of article dicts.
    """

    kept = []
    seen = []

    for article in articles:

        if article["url"] in seen:
            continue

        if not article["title"] or not article["url"]:
            continue
        
        if not article["description"]:
            continue

        if "consent." in article["url"]:
            continue

        seen.append(article["url"])
        kept.append(article)

    return kept