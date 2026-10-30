""" Generates a summarized report of news articles on Sudan in the past week."""

import os
from datetime import date, timedelta

from clean import clean
from cluster import cluster
from dedup import dedup
from ingest import fetch, save_raw
from report import make_report
from store import upload
from summarize import summarize

def main():
    """
    Runs the full news pipeline, storing files locally and to an S3 bucket.

    Fetches articles, cleans, dedupes, clusters, and summarizes them,
    then stores the raw articles and the markdown report.
    """

    today = date.today()
    to_date = today - timedelta(days=1)
    from_date = to_date - timedelta(days=6)
        
    articles = fetch(from_date, to_date)

    raw_file = f"raw_articles/{to_date}.json"
    report_file = f"reports/{to_date}.md"

    os.makedirs("raw_articles", exist_ok=True)
    save_raw(articles, raw_file)

    articles = clean(articles)

    articles = dedup(articles)

    groups = cluster(articles)

    sections = []
    
    for group in groups:
        if len(group) < 2:
            continue
        try:
            section = summarize(group)
        except Exception as e:
            print(f"skipped a group of {len(group)}: {e}")
            continue
        if section["about_sudan"]:
            sections.append(section)

    if not sections:
        raise RuntimeError("no sections generated, not uploading an empty report")

    text = make_report(sections)

    os.makedirs("reports", exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(text)

    upload(raw_file, raw_file)
    upload(report_file, report_file)

if __name__ == "__main__":
    main()