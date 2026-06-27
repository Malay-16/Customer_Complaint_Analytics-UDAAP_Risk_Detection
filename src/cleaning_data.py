from IPython import core
import os
import pandas as pd
from preprocessing import ComplaintPreprocessor
from sentiment import SentimentAnalyzer
from risk_detection import UDAAPRiskDetector

def run_pipeline():
    # Define absolute paths based on this script's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "sql", "complaints.db")
    output_path = os.path.join(base_dir, "data", "cleaned", "cleaned_complaints.csv")
    
    print("--- Starting End-to-End Extraction Pipeline ---")
    
    # 1. Preprocessing
    print("\nStep 1: Preprocessing data...")
    preprocessor = ComplaintPreprocessor(db_path=db_path)
    df = preprocessor.process(table_name="complaints")
    
    # 2. Sentiment Analysis
    print("\nStep 2: Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.process(df, text_column="clean_narrative")
    
    # 3. UDAAP Risk Detection
    print("\nStep 3: Detecting UDAAP risks...")
    risk_detector = UDAAPRiskDetector()
    df = risk_detector.process(df, text_column="clean_narrative")
    
    # 4. Save Final Dataset
    print(f"\nStep 4: Saving final enriched dataset to:\n  {output_path}")
    df.to_csv(output_path, index=False)
    
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()
