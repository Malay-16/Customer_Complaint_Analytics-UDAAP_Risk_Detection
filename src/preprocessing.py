import sqlite3
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import string

class ComplaintPreprocessor:
    def __init__(self, db_path: str):
        """
        Initializes the ComplaintPreprocessor.
        Ensures that NLTK stopwords are available.
        """
        self.db_path = db_path
        
        # Ensure stopwords are downloaded
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
            
        self.stop_words = set(stopwords.words('english'))
        
    def load_data(self, query: str = "SELECT * FROM complaints") -> pd.DataFrame:
        """Loads data from the SQLite database using the provided query."""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
        
    def clean_text(self, text: str) -> str:
        """
        Applies standard text normalization:
        - Forces lowercasing
        - Strips punctuation and special characters
        - Removes generic english stopwords
        """
        if pd.isna(text) or str(text).strip() == '':
            return ""
            
        # Lowercase
        text = str(text).lower()
        
        # Replace punctuation/special characters with a space
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        
        # Strip extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove stopwords
        words = text.split()
        cleaned_words = [w for w in words if w not in self.stop_words]
        
        return " ".join(cleaned_words)
        
    def process(self, table_name: str = "complaints") -> pd.DataFrame:
        """
        Executes the full pipeline sequentially:
        1. Loads data.
        2. Filters out null or blank Consumer Complaint Narratives.
        3. Cleans the text and outputs a 'clean_narrative' column.
        """
        # 1. Load the data
        query = f"SELECT * FROM {table_name}"
        df = self.load_data(query)
        
        # Define the column name
        col_name = 'Consumer Complaint Narrative'
        
        if col_name not in df.columns:
            raise ValueError(f"Column '{col_name}' not found in the loaded data.")
            
        # 2. Filter out rows where the narrative is null or completely blank
        df = df.dropna(subset=[col_name])
        # Make sure values are strings and strip to check for blanks
        df = df[df[col_name].astype(str).str.strip() != '']
        
        # 3. Apply standard text normalization
        df['clean_narrative'] = df[col_name].apply(self.clean_text)
        
        return df

if __name__ == "__main__":
    # Example usage (will not run fully unless complaints.db exists):
    # preprocessor = ComplaintPreprocessor(db_path="../sql/complaints.db")
    # clean_df = preprocessor.process()
    # print(clean_df.head())
    pass
