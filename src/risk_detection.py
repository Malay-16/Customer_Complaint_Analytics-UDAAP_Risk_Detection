import pandas as pd

class UDAAPRiskDetector:
    def __init__(self):
        """
        Initializes the risk detector with an exhaustive dictionary of target 
        risk substrings associated with UDAAP violations.
        """
        self.risk_keywords = [
            "hidden fee",
            "hidden charges",
            "bait and switch",
            "misled",
            "misleading",
            "lied",
            "deceptive",
            "unauthorized charge",
            "unauthorized transaction",
            "refused to release",
            "forced",
            "coerced",
            "scam",
            "fraud",
            "stolen",
            "without consent",
            "never agreed"
        ]
        
    def detect_risk(self, text: str) -> int:
        """Returns 1 if any risk keyword is found in the text, else 0."""
        if pd.isna(text):
            return 0
        text_lower = str(text).lower()
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                return 1
        return 0
        
    def process(self, df: pd.DataFrame, text_column: str = "clean_narrative") -> pd.DataFrame:
        """
        Applies rule-based risk classification on the given column.
        Sets binary column 'is_udaap_risk'.
        """
        print(f"Applying UDAAP risk detection on {len(df)} records...")
        df['is_udaap_risk'] = df[text_column].apply(self.detect_risk)
        return df
