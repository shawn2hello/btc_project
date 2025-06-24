import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

os.makedirs("data", exist_ok=True)

df = pd.read_csv('data/btc_tweet_sample.csv')

# drop rows with missing text
df['tweet.text'] = df['tweet.text'].astype(str).dropna()

analyzer = SentimentIntensityAnalyzer()

sentiment_scores = df['tweet.text'].apply(analyzer.polarity_scores)

# Convert sentiment dicts to DataFrame
sentiment_df = pd.DataFrame(sentiment_scores.tolist())

# Merge with original dataframe
df = pd.concat([df.reset_index(drop=True), sentiment_df], axis=1)

def label_sentiment(compound):
    if compound >= 0.7:
        return 'greatly positive'
    elif compound >= 0.3:
        return 'positive'
    elif compound <= -0.7:
        return 'greatly negative'
    elif compound <= -0.3:
        return 'negative'
    else:
        return 'neutral'
    
df['sentiment'] = df['compound'].apply(label_sentiment)

# 🔍 Add context keyword matching
keywords = [
    'crash', 'dump', 'sell-off', 'plunge', 'bearish',
    'moon', 'pump', 'bullish', 'breakout', 'rally',
    'ETF', 'regulation', 'ban', 'approval', 'hack', 'whale'
]
keyword_pattern = '|'.join(keywords)
df['context_match'] = df['tweet.text'].str.contains(keyword_pattern, case=False, na=False)

# Save the result to a new CSV file
df.to_csv("data/tweet_results.csv", index=False)

