import feedparser
import json
from datetime import datetime, timedelta

# Define the RSS feed URLs
feeds = {
    'Inc42': 'https://inc42.com/feed',
    'Entrackr': 'https://entrackr.com/feed'
}

# Automatically set target date to yesterday
target_date = (datetime.now() - timedelta(days=1)).date()

# Function to fetch and filter articles
def fetch_articles(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        # Ensure 'published_parsed' exists
        if hasattr(entry, 'published_parsed'):
            published_date = datetime(*entry.published_parsed[:6]).date()
            if published_date == target_date:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published
                })
    
    return articles

# Collect articles from all feeds
all_articles = {source: fetch_articles(url) for source, url in feeds.items()}

# Remove empty sources
all_articles = {source: articles for source, articles in all_articles.items() if articles}

# Define the output JSON file path
output_file = 'news.json'

# Write the filtered articles to a JSON file
with open(output_file, 'w') as json_file:
    json.dump(all_articles, json_file, indent=4)

if all_articles:
    print(f"Articles from {target_date} have been written to {output_file}")
else:
    print(f"No articles found for {target_date}. JSON file not created.")
