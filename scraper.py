"""Scrape top headlines from Hacker News and save them to CSV.

Check a site's robots.txt and terms before scraping, and keep requests light.
"""
import csv
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com/"


def scrape():
    resp = requests.get(URL, headers={"User-Agent": "learning-scraper/1.0"}, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    for span in soup.select("span.titleline"):
        link = span.find("a")
        if link:
            rows.append({"title": link.get_text(strip=True), "url": link.get("href")})
    return rows


def save(rows, path="headlines.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    try:
        headlines = scrape()
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")
    save(headlines)
    print(f"Saved {len(headlines)} headlines at {datetime.now():%Y-%m-%d %H:%M}")
    for h in headlines[:5]:
        print("-", h["title"])
