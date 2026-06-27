# Customer Complaint Analytics & UDAAP Risk Detection

## 📌 Executive Summary
This project is an end-to-end data engineering and analytics pipeline designed to monitor consumer financial complaints and automatically identify Unfair, Deceptive, or Abusive Acts or Practices (UDAAP). By combining Natural Language Processing (NLP) techniques with rule-based classification and SQL analytics, this pipeline extracts actionable insights from raw consumer complaint narratives. 

## 🚀 Steps Performed
1. **Infrastructure Initialization**: Structured the workspace into designated folders (`data/raw/`, `sql/`, `src/`, etc.) and loaded `complaints.csv` (9,477 records).
2. **Database Ingestion**: Processed raw CSV data, standardized datetime formats, and ingested it into a localized SQLite Database (`sql/complaints.db`).
3. **Data Preprocessing Pipeline**: Built a Python NLP pipeline to strip punctuation, remove generic stop words, and lowercase all consumer narratives for robust analysis.
4. **Sentiment Analysis**: Computed a polarity score for every narrative using TextBlob, categorizing complaints into Positive, Neutral, or Negative.
5. **UDAAP Risk Detection**: Engineered a rule-based classifier that scans normalized text for high-risk regulatory keywords (e.g., "hidden fee", "unauthorized charge", "misled", "scam") and flags compliance violations.
6. **Dashboard Extraction**: Ran the master extraction pipeline to build a fully enriched `cleaned_complaints.csv` dataset.
7. **Interactive Dashboard**: Deployed a dynamic 4-page Streamlit web dashboard to visually report on trends, risks, and sentiment.

## 📈 Business Insights & Key Findings

Based on the processed dataset of 9,477 consumer complaints, our analytics engine uncovered the following answers to our core business questions:

- **Which products generate the highest complaints?**
  1. Credit card (3,560 complaints)
  2. Checking or savings account (2,558 complaints)
  3. Mortgage (1,768 complaints)

- **Which complaint categories are increasing?**
  *Credit Cards* and *Checking/Savings accounts* make up the vast majority of all recent incoming complaint volumes, dwarfing all other financial products in the recent timeframe.

- **Which issues may indicate UDAAP risk?**
  The top issues that frequently contain UDAAP-flagged language (such as "bait and switch" or "unauthorized charge") are:
  1. Billing disputes
  2. Struggling to pay mortgage
  3. Managing an account

- **What is customer sentiment?**
  As expected with complaint data, sentiment is overwhelmingly negative, but the exact breakdown is:
  - **Negative:** 97.58%
  - **Positive:** 2.30%
  - **Neutral:** 0.12%

- **Which complaints require immediate escalation?**
  There are exactly **622 complaints** that require immediate compliance review. These are high-priority tickets where the consumer's text flagged positive for UDAAP risk *and* carried a heavily negative sentiment.

- **Which regions have the highest complaint volume?**
  1. California (1,087 complaints)
  2. Texas (898 complaints)
  3. New York (784 complaints)

## 💡 Strategic Recommendations & Operational Improvements
1. **Overhaul Billing Dispute Workflows:** Because "Billing disputes" are the #1 trigger for UDAAP risk flags (often mentioning "unauthorized charges" or "hidden fees"), the organization should immediately audit its fee disclosure practices for Credit Cards.
2. **Proactive Mortgage Hardship Outreach:** "Struggling to pay mortgage" is a massive driver of compliance risk. Deploying proactive communication regarding forbearance or payment plans before consumers reach the complaint stage can heavily mitigate regulatory exposure.
3. **Targeted State Interventions:** Allocate additional customer service routing priority and compliance auditing to California, Texas, and New York, as they represent the highest density of dissatisfied customers.
4. **Automated Escalation:** Integrate the NLP pipeline directly into the live ticketing system to automatically flag and route those 622 severe UDAAP-risk complaints directly to the Legal/Compliance department to avoid CFPB fines.

---

## 📂 Directory Structure
```text
├── data/
│   ├── raw/                 # Raw input datasets
│   └── cleaned/             # Enriched output datasets (cleaned_complaints.csv)
├── sql/                     # SQLite database and optimized SQL analytics queries
├── src/                     # Core pipeline Python scripts
│   ├── initialize_db.py     # Ingests raw CSV and initializes the SQLite DB
│   ├── preprocessing.py     # Text normalization
│   ├── sentiment.py         # Sentiment analysis using TextBlob
│   ├── risk_detection.py    # Rule-based UDAAP risk classification
│   ├── cleaning_data.py     # Master script to run the extraction pipeline
│   └── app.py               # Streamlit Interactive Dashboard
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## ⚙️ Configuration & Reproduction Steps
To run this pipeline locally from scratch:

1. **Clone & Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```
2. **Initialize Database**
   ```bash
   python src/initialize_db.py
   ```
3. **Run Extraction Pipeline**
   ```bash
   python src/cleaning_data.py
   ```
4. **Launch Dashboard**
   ```bash
   streamlit run src/app.py
   ```

## 📊 Dashboard Layout Guide (Power BI / Streamlit)
- **Page 1: Executive Summary** - KPI Cards and Sentiment Donut Charts.
- **Page 2: Complaint Trends** - Time-series volume and State-level Choropleth maps.
- **Page 3: NLP Insights** - Word clouds and 100% Stacked Bar Charts for product sentiment.
- **Page 4: Risk Dashboard** - High-density Risk Matrix highlighting intersections of volume and compliance violations.
