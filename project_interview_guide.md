# 🎯 Complete Project Interview Guide
**Project Name:** Customer Complaint Analytics & UDAAP Risk Detection

This guide is designed to serve as a comprehensive breakdown of the entire project. It explains the core business problems, the data engineering pipeline, and deep-dives into every line of code so that you can confidently explain the project in an interview, even if you are just starting out.

---

## 📌 1. The Business Problem & Solution

**The Problem:** 
Financial institutions receive thousands of customer complaints. Regulatory bodies like the CFPB actively monitor these for **UDAAP** violations (Unfair, Deceptive, or Abusive Acts or Practices). Failing to identify these risks can lead to massive fines. Reading every single complaint manually is impossible.

**The Solution:**
We built an automated Data Engineering and NLP (Natural Language Processing) pipeline. It:
1. Ingests raw complaint data into a database.
2. Cleans the text.
3. Automatically scores the customer's sentiment (Positive/Negative/Neutral).
4. Scans the text for specific high-risk UDAAP keywords (e.g., "fraud", "hidden fee").
5. Visualizes the final insights in a web-based dashboard using Streamlit.

---

## 🏗️ 2. Architecture & Tech Stack

If asked about the architecture in an interview, you can describe it in these three layers:

- **Storage Layer (Database):** SQLite (`sqlite3`) handles our relational data.
- **Processing Layer (Pipeline):** Python (`pandas`) for data manipulation, `nltk` for text cleaning, and `textblob` for sentiment analysis.
- **Presentation Layer (UI):** `streamlit` combined with `plotly` to build interactive web dashboards and charts.

---

## 💻 3. Code Breakdown: Script by Script

The core logic lives inside the `src/` folder. Let's break down exactly what each script does.

### A. `initialize_db.py` (Data Ingestion)
**Goal:** Take the raw CSV file and dump it into an SQL Database so it can be queried later.

```python
def init_db():
    # 1. Load the raw data from our data/raw folder
    df = pd.read_csv(csv_path, low_memory=False)
    
    # 2. Standardize the Date Format
    # Dates are tricky in data science. We use pd.to_datetime to force the format.
    df['Date received'] = pd.to_datetime(df['Date received'], format='%d-%m-%Y', errors='coerce')
    
    # 3. Save it to a SQLite database file named 'complaints.db'
    with sqlite3.connect(db_path) as conn:
        df.to_sql("complaints", conn, if_exists="replace", index=False)
```
**Interview Talking Point:** *"I used Python to ingest the raw CSV and standardize the date schemas before loading it into an SQLite database for scalable querying."*

### B. `preprocessing.py` (Data Cleaning)
**Goal:** Raw text is messy. It has punctuation, uppercase/lowercase mismatches, and useless "stop words" (like "the", "and", "is").

```python
class ComplaintPreprocessor:
    def clean_text(self, text: str) -> str:
        # 1. Convert everything to lowercase
        text = str(text).lower()
        
        # 2. Use regular expressions (re) to replace punctuation with a space
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        
        # 3. Remove English Stop Words using the NLTK (Natural Language Toolkit) library
        words = text.split()
        cleaned_words = [w for w in words if w not in self.stop_words]
        
        return " ".join(cleaned_words)
```
**Interview Talking Point:** *"I built an NLP preprocessing class that normalizes strings. It lowercases everything, strips punctuation using regex, and leverages the NLTK corpus to remove English stop words to reduce noise in our dataset."*

### C. `sentiment.py` (Sentiment Analysis)
**Goal:** Determine if the customer is angry, happy, or neutral.

```python
def get_sentiment(text):
    # TextBlob reads the text and assigns a 'polarity' score from -1.0 (very negative) to 1.0 (very positive)
    polarity = TextBlob(str(text)).sentiment.polarity
    
    # We create business rules around the score:
    if polarity > 0.05:
        label = "Positive"
    elif polarity < -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return polarity, label
```
**Interview Talking Point:** *"For sentiment analysis, I implemented TextBlob to calculate a continuous polarity score, which I then mapped into discrete buckets (Positive, Negative, Neutral) to make it easier for business stakeholders to digest."*

### D. `risk_detection.py` (UDAAP Risk Engine)
**Goal:** Flag complaints that contain dangerous regulatory keywords.

```python
class UDAAPRiskDetector:
    def __init__(self):
        # A dictionary/list of dangerous phrases
        self.risk_keywords = ["hidden fee", "bait and switch", "scam", "fraud", "unauthorized charge"]
        
    def detect_risk(self, text: str) -> int:
        text_lower = str(text).lower()
        # Loop through the list. If a dangerous word is found in the text, return 1 (True)
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                return 1
        return 0 # Otherwise return 0 (False)
```
**Interview Talking Point:** *"I engineered a rule-based risk classification engine. It scans the normalized customer narratives against an exhaustive dictionary of known UDAAP violation keywords, flagging high-risk records automatically."*

### E. `dashboard_data.py` (The Orchestrator)
**Goal:** This script ties everything together into an automated pipeline.

```python
def run_pipeline():
    # Step 1: Preprocess the DB table
    preprocessor = ComplaintPreprocessor(db_path)
    df = preprocessor.process("complaints")
    
    # Step 2: Add Sentiment
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.process(df)
    
    # Step 3: Add Risk flags
    risk_detector = UDAAPRiskDetector()
    df = risk_detector.process(df)
    
    # Step 4: Save the final enriched CSV
    df.to_csv(output_path, index=False)
```
**Interview Talking Point:** *"I designed a modular pipeline architecture. The orchestrator script extracts the data, sequentially applies the preprocessing, sentiment, and risk classes, and loads the enriched dataset into a clean CSV for the dashboard."*

### F. `app.py` (The Interactive Streamlit Dashboard)
**Goal:** Provide a web UI for compliance officers to view the data.

- **`@st.cache_data`**: Used to cache the data loading. This means if you click between pages, it doesn't re-read the 4MB CSV file every time, keeping the dashboard lightning fast.
- **Pages**: Uses `st.sidebar.radio` to create a multi-page app (Executive Summary, Trends, NLP Insights, Risk Matrix).
- **Plotly Express (`px`)**: We use Plotly instead of Matplotlib because Plotly charts are interactive out-of-the-box (you can hover, zoom, and click them).
- **Risk Matrix**: In Page 4, we use a scatter plot (`px.scatter`) where the X-axis is Volume and the Y-axis is Risk, helping officers spot which products have the most critical compliance failures.

---

## 🙋‍♂️ 4. Common Interview Questions & How to Answer Them

> **Q: "Why did you use a rule-based engine for UDAAP risk instead of a Machine Learning model like BERT?"**
> **Answer:** "For regulatory compliance, explainability is crucial. If the compliance department asks why a complaint was flagged, a rule-based approach allows us to point to the exact keyword (e.g., 'hidden fee'). While a deep learning model might capture more nuance, a rule-based system guarantees deterministic, explainable results with zero false positives on specific terminology."

> **Q: "How did you handle missing data in the text column?"**
> **Answer:** "During the preprocessing stage, I used Pandas to explicitly drop rows where the 'Consumer Complaint Narrative' was null or entirely whitespace. NLP models fail if you feed them missing string types, so ensuring data quality upstream was critical."

> **Q: "How would you scale this if the data grew to 100 million records?"**
> **Answer:** "Currently, the pipeline uses Pandas, which processes data in-memory. If we scaled up, I would migrate the processing engine to Apache Spark (PySpark) or run the SQL transformations entirely inside a cloud data warehouse like BigQuery using dbt. I would also move the data storage from SQLite to a robust system like PostgreSQL."
