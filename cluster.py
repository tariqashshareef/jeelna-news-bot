"""Groups articles into themes by meaning."""

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster(articles, threshold=0.5):
    """
    Groups articles by theme using embeddings of title and description.

    Args:
        articles: A list of article dicts.
        threshold: Cosine distance below which groups merge. Lower means more, smaller groups.

    Returns:
        A list of groups, where each group is a list of article dicts.
    """

    texts = []
    for article in articles:
        texts.append(article["title"] + ". " + article["description"])

    vectors = model.encode(texts)

    clusterer = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        metric="cosine",
        linkage="average",
    )

    labels = clusterer.fit_predict(vectors)

    groups = {}

    for label, article in zip(labels, articles):
        if label not in groups:
            groups[label] = []
        groups[label].append(article)

    return list(groups.values())