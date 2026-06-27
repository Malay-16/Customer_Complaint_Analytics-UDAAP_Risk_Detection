import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="UDAAP Risk Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "cleaned", "cleaned_complaints.csv")
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path, low_memory=False)
    
    date_col = 'Date received' if 'Date received' in df.columns else 'Date Received'
    if date_col in df.columns:
        df['Date'] = pd.to_datetime(df[date_col], errors='coerce')
    else:
        df['Date'] = pd.to_datetime("today")
    return df

df = load_data()

if df.empty:
    st.error("Dataset not found. Please run the extraction pipeline first.")
    st.stop()

# Fallbacks in case columns are missing
if 'is_udaap_risk' not in df.columns: df['is_udaap_risk'] = 0
if 'sentiment_label' not in df.columns: df['sentiment_label'] = 'Neutral'
if 'State' not in df.columns: df['State'] = 'Unknown'
if 'Product' not in df.columns: df['Product'] = 'Unknown'
if 'Company' not in df.columns: df['Company'] = 'Unknown'

# --- Sidebar Navigation ---
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to:", [
    "1. Executive Summary", 
    "2. Complaint Trends", 
    "3. NLP Insights", 
    "4. Risk Dashboard"
])

st.title(page[3:]) # Set title dynamically based on the page selected (removing the number)


# PAGE 1: EXECUTIVE SUMMARY

if page == "1. Executive Summary":
    st.markdown("### High-level snapshot of project health and overall metrics")
    
    total_complaints = len(df)
    risk_flags = df['is_udaap_risk'].sum()
    risk_pct = (risk_flags / total_complaints) * 100 if total_complaints > 0 else 0
    negative_sentiment = len(df[df['sentiment_label'] == 'Negative'])
    
    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints", f"{total_complaints:,}")
    col2.metric("UDAAP Risk (%)", f"{risk_pct:.1f}%")
    col3.metric("Negative Sentiment Vol", f"{negative_sentiment:,}")
    
    st.markdown("---")
    
    # Overall Sentiment Donut Chart
    st.subheader("Overall Sentiment Distribution")
    sent_counts = df['sentiment_label'].value_counts().reset_index()
    sent_counts.columns = ['Sentiment', 'Count']
    fig_donut = px.pie(
        sent_counts, values='Count', names='Sentiment', hole=0.4,
        color='Sentiment',
        color_discrete_map={"Positive": "#00CC96", "Neutral": "#636EFA", "Negative": "#EF553B"}
    )
    st.plotly_chart(fig_donut, use_container_width=True)


# PAGE 2: COMPLAINT TRENDS

elif page == "2. Complaint Trends":
    st.markdown("### Temporal and geographical analysis of complaint volumes")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Complaint Volume Over Time")
        time_df = df.copy()
        time_df['MonthYear'] = time_df['Date'].dt.to_period("M")
        trend = time_df.groupby('MonthYear').size().reset_index(name='Complaints')
        trend['MonthYear'] = trend['MonthYear'].dt.to_timestamp()
        
        fig_time = px.line(trend, x='MonthYear', y='Complaints', markers=True)
        fig_time.update_layout(xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(fig_time, use_container_width=True)
        
    with col_right:
        st.subheader("Complaint Density by State")
        # Filter out unknown states and count
        state_df = df[df['State'] != 'Unknown'].groupby('State').size().reset_index(name='Complaints')
        fig_map = px.choropleth(
            state_df, locations='State', locationmode="USA-states", 
            color='Complaints', scope="usa",
            color_continuous_scale="Blues",
            title="Geographical Distribution"
        )
        st.plotly_chart(fig_map, use_container_width=True)


# PAGE 3: NLP INSIGHTS

elif page == "3. NLP Insights":
    st.markdown("### Deep dive into textual data and customer sentiment")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Narrative Word Cloud")
        if 'clean_narrative' in df.columns:
            # Sample 2000 records to keep it fast
            text_data = " ".join(df['clean_narrative'].dropna().sample(min(2000, len(df))).astype(str).tolist())
            if text_data.strip():
                wordcloud = WordCloud(width=800, height=500, background_color='white', max_words=150).generate(text_data)
                fig_wc, ax = plt.subplots(figsize=(8,5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig_wc)
            else:
                st.info("No text data available for word cloud.")
        else:
            st.info("clean_narrative column not found.")
            
    with col_right:
        st.subheader("Sentiment Breakdown by Product (100% Stacked)")
        sent_df = df.groupby(['Product', 'sentiment_label']).size().reset_index(name='Count')
        fig_sent = px.bar(
            sent_df, x='Product', y='Count', color='sentiment_label', 
            barmode='stack',
            color_discrete_map={"Positive": "#00CC96", "Neutral": "#636EFA", "Negative": "#EF553B"}
        )
        # Using barnorm='percent' to make it a 100% stacked chart
        fig_sent.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_tickangle=-45, barnorm='percent')
        fig_sent.update_yaxes(title_text='Percentage (%)')
        st.plotly_chart(fig_sent, use_container_width=True)


# PAGE 4: RISK DASHBOARD

elif page == "4. Risk Dashboard":
    st.markdown("### Focused compliance monitoring for UDAAP violations")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Product Risk Matrix")
        # Pre-calculate data for matrix
        risk_stats = df.groupby('Product').agg(
            Total_Complaints=('is_udaap_risk', 'size'),
            UDAAP_Risks=('is_udaap_risk', 'sum')
        ).reset_index()
        
        # Scatter plot highlighting high volume and high risk instances
        fig_matrix = px.scatter(
            risk_stats, x='Total_Complaints', y='UDAAP_Risks', 
            size='Total_Complaints', color='UDAAP_Risks', hover_name='Product',
            color_continuous_scale="Reds", size_max=40
        )
        fig_matrix.update_layout(xaxis_title="Total Complaints", yaxis_title="Flagged UDAAP Risks")
        st.plotly_chart(fig_matrix, use_container_width=True)
        
    with col_right:
        st.subheader("Highest Risk Density (Company / Product)")
        # Calculate risk density
        company_risk = df.groupby(['Company', 'Product']).agg(
            Total_Complaints=('is_udaap_risk', 'size'),
            UDAAP_Risks=('is_udaap_risk', 'sum')
        ).reset_index()
        company_risk['Risk_Density_%'] = (company_risk['UDAAP_Risks'] / company_risk['Total_Complaints'] * 100).round(1)
        
        # Filter for companies with a meaningful baseline of complaints
        company_risk = company_risk[company_risk['Total_Complaints'] >= 5]
        top_risks = company_risk.sort_values(by=['Risk_Density_%', 'UDAAP_Risks'], ascending=[False, False]).head(15)
        
        st.dataframe(
            top_risks.style.background_gradient(subset=['Risk_Density_%'], cmap='Reds'),
            use_container_width=True,
            height=400
        )
