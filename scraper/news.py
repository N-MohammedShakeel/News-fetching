import feedparser
import json
from datetime import datetime, timedelta
import re

# Define the RSS feed URLs
feeds = {
    'Inc42': 'https://inc42.com/feed',
    'Entrackr': 'https://entrackr.com/rss'
}

# Set target date to yesterday
target_date = (datetime.now() - timedelta(days=1)).date()  # Only yesterday's news

# Function to extract image URL from an entry
def extract_image(entry):
    if 'media_content' in entry and entry.media_content:
        return entry.media_content[0]['url']
    elif 'media_thumbnail' in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0]['url']
    elif 'summary' in entry and 'img' in entry.summary:
        match = re.search(r'<img.*?src="(.*?)"', entry.summary)
        if match:
            return match.group(1)
    return None  # Return None if no image found

# Function to fetch and filter articles
def fetch_articles(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            published_date = datetime(*entry.published_parsed[:6]).date()
            if published_date == target_date:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'image_url': extract_image(entry)
                })
    
    return articles

# Collect articles from all feeds
all_articles = {source: fetch_articles(url) for source, url in feeds.items()}

# Remove empty sources
all_articles = {source: articles for source, articles in all_articles.items() if articles}

# Define the output JSON file path
output_file = 'news.json'

# Write the filtered articles to a JSON file
if all_articles:
    with open(output_file, 'w') as json_file:
        json.dump(all_articles, json_file, indent=4)
    print(f"Articles from {target_date} (Yesterday) have been written to {output_file}")
else:
    print(f"No articles found for {target_date}. JSON file not created.")
