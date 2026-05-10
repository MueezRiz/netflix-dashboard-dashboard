import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page config
st.set_page_config(page_title="Netflix Show Insights", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS for aesthetics
st.markdown("""
<style>
    /* Styling headers */
    h1, h2, h3, h4 {
        color: #E50914 !important;
        font-family: 'Arial', sans-serif;
    }
    /* Styling the metrics boxes */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: white;
    }
    [data-testid="stMetric"] {
        background-color: #1c1c1c;
        padding: 15px;
        border-left: 5px solid #E50914;
        border-radius: 5px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.4);
    }
    /* Horizontal lines styling */
    hr {
        border: 1px solid #E50914;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    df['date_added'] = pd.to_datetime(df['date_added'])
    return df

st.title("🎬 Comprehensive Netflix Content Dashboard")
st.markdown("Dive deep into Netflix's massive catalog! Explore trends, search by genres, and track your favorite actors and directors over the years.")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'netflix_cleaned.csv' not found. Please ensure it's in the same directory.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.header("🔍 Filter Options")
types = st.sidebar.multiselect("Content Type", options=df['type'].unique(), default=df['type'].unique())

min_yr = int(df['release_year'].min())
max_yr = int(df['release_year'].max())
year_range = st.sidebar.slider("Release Year", min_yr, max_yr, (2000, max_yr))

all_ratings = [r for r in df['rating'].dropna().unique() if r != 'Unknown']
selected_ratings = st.sidebar.multiselect("Maturity Rating", options=all_ratings, default=all_ratings)

# Apply filters
p_df = df[(df['type'].isin(types)) & 
          (df['release_year'].between(year_range[0], year_range[1])) &
          (df['rating'].isin(selected_ratings))]

# --- Metrics Banner ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("📌 Total Titles", f"{len(p_df):,}")
col2.metric("🎥 Total Movies", f"{len(p_df[p_df['type'] == 'Movie']):,}")
col3.metric("📺 Total TV Shows", f"{len(p_df[p_df['type'] == 'TV Show']):,}")
movies_dur = p_df[p_df['type'] == 'Movie']['duration_num'].mean()
col4.metric("⏱ Avg Movie Duration", f"{movies_dur:.0f} min" if pd.notnull(movies_dur) else "N/A")

st.markdown("---")

# --- Interactive Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Overview & Trends", "🎬 Cast & Directors", "⭐ Deep Dive & Ratings"])

with tab1:
    st.header("Overview & Global Trends")
    st.markdown("See what types of content dominate the collection and how production changed over time.")
    r1c1, r1c2 = st.columns(2)
    
    with r1c1:
        yearly_added = p_df.groupby('year_added').size().reset_index(name='count')
        fig1 = px.line(yearly_added, x='year_added', y='count', markers=True, title="Trend of Content Added per Year", color_discrete_sequence=["#E50914"])
        fig1.update_layout(xaxis_title="Year Added", yaxis_title="Number of Titles", template="plotly_dark", hovermode="x unified")
        st.plotly_chart(fig1, width="stretch")

    with r1c2:
        type_counts = p_df['type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig2 = px.pie(type_counts, names='Type', values='Count', title="Distribution by Content Type", hole=0.5, color_discrete_sequence=["#E50914", "#B00710"])
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, width="stretch")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        countries = p_df['country'].dropna().str.split(', ').explode()
        countries = countries[countries != 'Unknown']
        top_countries = countries.value_counts().head(10).reset_index()
        top_countries.columns = ['Country', 'Count']
        fig3 = px.bar(top_countries, x='Count', y='Country', orientation='h', title="Top 10 Producing Countries", color_discrete_sequence=["#E50914"])
        fig3.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
        st.plotly_chart(fig3, width="stretch")

    with r2c2:
        genres = p_df['listed_in'].dropna().str.split(', ').explode()
        top_genres = genres.value_counts().head(10).reset_index()
        top_genres.columns = ['Genre', 'Count']
        fig4 = px.bar(top_genres, x='Count', y='Genre', orientation='h', title="Top 10 Most Common Genres", color_discrete_sequence=["#B00710"])
        fig4.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
        st.plotly_chart(fig4, width="stretch")

with tab2:
    st.header("Behind the Scenes (Cast & Creators)")
    st.markdown("Find out who brings the Netflix library to life—from directors calling the shots to the most prominent cast members.")
    c1, c2 = st.columns(2)
    
    with c1:
        directors = p_df['director'].dropna().str.split(', ').explode()
        directors = directors[directors != 'Unknown']
        top_dirs = directors.value_counts().head(10).reset_index()
        top_dirs.columns = ['Director', 'Titles']
        fig_dir = px.bar(top_dirs, x='Titles', y='Director', orientation='h', title="Top 10 Most Featured Directors", color_discrete_sequence=["#E50914"])
        fig_dir.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
        st.plotly_chart(fig_dir, width="stretch")

    with c2:
        cast = p_df['cast'].dropna().str.split(', ').explode()
        cast = cast[cast != 'Unknown']
        top_cast = cast.value_counts().head(10).reset_index()
        top_cast.columns = ['Actor', 'Appearances']
        fig_cast = px.bar(top_cast, x='Appearances', y='Actor', orientation='h', title="Top 10 Most Featured Cast Members", color_discrete_sequence=["#B00710"])
        fig_cast.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
        st.plotly_chart(fig_cast, width="stretch")

with tab3:
    st.header("Ratings & Deep Dive")
    st.markdown("Take a closer look at the age demographics (Maturity Ratings) and browse the catalog individually.")
    
    # Rating Distribution
    rating_counts = p_df['rating'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']
    # Filter out unknown just to clean visualization
    rating_counts = rating_counts[rating_counts['Rating'] != 'Unknown']
    
    fig_rat = px.bar(rating_counts, x='Rating', y='Count', title="Content Volumes by Maturity Rating", text='Count', color_discrete_sequence=["#E50914"])
    fig_rat.update_layout(xaxis={'categoryorder':'total descending'}, template="plotly_dark")
    st.plotly_chart(fig_rat, width="stretch")
    
    st.markdown("### 🎬 Browse Specific Titles")
    st.markdown("Use this interactive table to explore individual movies and TV shows matching your filters.")
    display_df = p_df[['title', 'type', 'director', 'cast', 'rating', 'release_year', 'duration', 'listed_in']].copy()
    display_df = display_df.rename(columns={
        "title": "Title", "type": "Type", "director": "Director", "cast": "Cast", "rating": "Rating",
        "release_year": "Release Year", "duration": "Duration", "listed_in": "Genres"
    })
    # Remove index from dataframe visualization for a cleaner look
    st.dataframe(display_df.set_index("Title"), height=400)
