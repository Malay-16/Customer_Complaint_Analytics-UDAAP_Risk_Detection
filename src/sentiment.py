import pandas as pd
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        """Initializes the SentimentAnalyzer."""
        pass
        
    def process(self, df: pd.DataFrame, text_column: str = "clean_narrative") -> pd.DataFrame:
        """
        Computes sentiment polarity using TextBlob.
        Maps continuous score into 'Positive', 'Neutral', or 'Negative' 
        and stores it in 'sentiment_label'.
        """
        print(f"Applying sentiment analysis on {len(df)} records...")
        
        def get_sentiment(text):
            if pd.isna(text) or str(text).strip() == "":
                return 0.0, "Neutral"
            polarity = TextBlob(str(text)).sentiment.polarity
            
            # Categorize based on polarity thresholds
            if polarity > 0.05:
                label = "Positive"
            elif polarity < -0.05:
                label = "Negative"
            else:
                label = "Neutral"
                
            return polarity, label

        # Apply to column
        results = df[text_column].apply(get_sentiment)
        
        # Unpack the tuple of (score, label) into columns
        df['sentiment_score'] = results.apply(lambda x: x[0])
        df['sentiment_label'] = results.apply(lambda x: x[1])
        
        return df
