import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Background and styling
st.markdown(
    """
    <style>
    .stApp {
        background: 
            repeating-linear-gradient(135deg, rgba(255,255,255,0.07) 0px, rgba(255,255,255,0.07) 2px, transparent 2px, transparent 40px),
            linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
        background-attachment: fixed;
    }
    .metric-label {
        color: #a259c6; /* Lilac accent */
        font-weight: bold;
        text-shadow: 1px 1px 2px #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        margin-bottom: 1rem;
    ">
      <span style="
        display: inline-block;
        padding-left: 100%;
        animation: marquee 12s linear infinite;
        font-size: 1.3em;
        font-weight: 600;
        color: #a259c6;
      ">
        📊 Explore Traffic Stop Data and Predict Outcomes
      </span>
    </div>
    <style>
    @keyframes marquee {
      0%   { transform: translate(0, 0); }
      100% { transform: translate(-100%, 0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)
# DB connection
db_url = "postgresql://vaish28:vG4D2gnkah4BsXvYAxYiws0ji7MayOsF@dpg-d0ka3b3e5dus73bju3sg-a.singapore-postgres.render.com/Traffic"
engine = create_engine(db_url)

def run_sql(query):
    return pd.read_sql(query, engine)

st.markdown(
    "<h1 style='color:#1e3c72;'>🚓🚨 SecureCheck Dashboard: A Digital Ledger for Police Post Logs</h1>",
    unsafe_allow_html=True
)

# Load and clean database
base_df = pd.read_sql("SELECT * FROM traffic_stops", engine)
base_df.dropna(axis=1, how='all', inplace=True)

if 'driver_age' in base_df.columns:
    base_df['driver_age'] = base_df['driver_age'].fillna(base_df['driver_age'].median())
if 'driver_gender' in base_df.columns:
    base_df['driver_gender'] = base_df['driver_gender'].fillna('Unknown')
base_df.dropna(subset=['stop_date', 'stop_time'], inplace=True)
object_cols = base_df.select_dtypes(include='object').columns
base_df[object_cols] = base_df[object_cols].fillna('Unknown')
bool_cols = base_df.select_dtypes(include='bool').columns
base_df[bool_cols] = base_df[bool_cols].fillna(False)

# Country filter
st.sidebar.header("🔍 Country Filter")
country = st.sidebar.selectbox("Select Country", base_df['country_name'].unique())
st.markdown(
    f"<h3 style='color:#3A6073;'>📋 Police Ledger data for {country}</h3>",
    unsafe_allow_html=True
)
st.dataframe(base_df[base_df['country_name'] == country])

# Query options from project
query_options = {
   
    "🚗 Top 10 vehicle numbers in drug-related stops": """
        SELECT vehicle_number, COUNT(*) AS drug_stop_count
        FROM traffic_stops
        WHERE drugs_related_stop = TRUE
        GROUP BY vehicle_number
        ORDER BY drug_stop_count DESC
        LIMIT 10;
    """,
    "🚗 Most frequently searched vehicles": """
        SELECT violation_raw AS vehicle_number, COUNT(*) AS search_count
        FROM traffic_stops
        WHERE search_conducted = TRUE
        GROUP BY violation_raw
        ORDER BY search_count DESC
        LIMIT 10;
    """,
    "🧍 Age group with highest arrest rate": """
        SELECT driver_age, COUNT(*) AS arrest_count
        FROM traffic_stops
        WHERE is_arrested = TRUE
        GROUP BY driver_age
        ORDER BY arrest_count DESC
        LIMIT 5;
    """,
    "🧍 Gender distribution per country": """
        SELECT country_name, driver_gender, COUNT(*) AS stop_count
        FROM traffic_stops
        GROUP BY country_name, driver_gender
        ORDER BY country_name;
    """,
    "🧍 Race and gender combo with highest search rate": """
        SELECT driver_race, driver_gender, COUNT(*) AS searches
        FROM traffic_stops
        WHERE search_conducted = TRUE
        GROUP BY driver_race, driver_gender
        ORDER BY searches DESC
        LIMIT 5;
    """,
    "🕒 Time of day with most stops": """
        SELECT LEFT(stop_time, 2) AS hour, COUNT(*) AS total_stops
        FROM traffic_stops
        GROUP BY hour
        ORDER BY total_stops DESC;
    """,
    "🕒 Average stop duration per violation": """
        SELECT violation, AVG(
            CASE stop_duration 
                WHEN '<5 Min' THEN 3
                WHEN '6-15 Min' THEN 10
                WHEN '16-30 Min' THEN 23
                WHEN '30+ Min' THEN 35
                ELSE 10
            END
        ) AS avg_duration_minutes
        FROM traffic_stops
        GROUP BY violation;
    """,
    "⚖️ Violations tied to searches/arrests": """
        SELECT violation, COUNT(*) AS total,
        COUNT(*) FILTER (WHERE search_conducted = TRUE OR is_arrested = TRUE) AS flagged
        FROM traffic_stops
        GROUP BY violation
        ORDER BY flagged DESC
        LIMIT 5;
    """,
    "⚖️ Most common violations under 25": """
        SELECT violation, COUNT(*) AS count
        FROM traffic_stops
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY count DESC
        LIMIT 5;
    """,
    "⚖️ Violations rarely leading to search/arrest": """
        SELECT violation,
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE search_conducted = TRUE OR is_arrested = TRUE) AS flagged
        FROM traffic_stops
        GROUP BY violation
        HAVING COUNT(*) FILTER (WHERE search_conducted = TRUE OR is_arrested = TRUE) = 0
        LIMIT 5;
    """,
    "🌍 Countries with highest drug-related stop rate": """
        SELECT country_name, COUNT(*) AS drug_stops
        FROM traffic_stops
        WHERE drugs_related_stop = TRUE
        GROUP BY country_name
        ORDER BY drug_stops DESC
        LIMIT 5;
    """,
    "🌙Are stops during the night more likely to lead to arrests": """
        SELECT
    CASE
        WHEN CAST(SUBSTRING(stop_time FROM '^[0-9]{1,2}') AS INTEGER) BETWEEN 20 AND 23
          OR CAST(SUBSTRING(stop_time FROM '^[0-9]{1,2}') AS INTEGER) BETWEEN 0 AND 5
            THEN 'Night'
        ELSE 'Day'
    END AS period,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
    ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
    FROM traffic_stops
    WHERE stop_time ~ '^[0-9]{1,2}:'  -- Only rows where stop_time starts with 1 or 2 digits and a colon
    GROUP BY period
    ORDER BY period;
    """,

    "🌍 Arrest rate by country and violation": """
        SELECT country_name, violation,
        COUNT(*) FILTER (WHERE is_arrested = TRUE) * 100.0 / COUNT(*) AS arrest_rate
        FROM traffic_stops
        GROUP BY country_name, violation
        ORDER BY arrest_rate DESC
        LIMIT 10;
    """,
    
    "🌍 Country with most stops having search conducted": """
        SELECT country_name, COUNT(*) AS search_count
        FROM traffic_stops
        WHERE search_conducted = TRUE
        GROUP BY country_name
        ORDER BY search_count DESC
        LIMIT 5;
    """,
    "📅 Yearly Stops & Arrests by Country": """
	SELECT
    country_name,
    EXTRACT(YEAR FROM stop_date::date) AS year,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent,
    SUM(COUNT(*)) OVER (PARTITION BY country_name ORDER BY EXTRACT(YEAR FROM stop_date::date)) AS running_total_stops
	FROM traffic_stops
	GROUP BY country_name, year
	ORDER BY country_name, year;
    """,
     "📈 Violation Trends by Age & Race": """
       	SELECT
            t.driver_age,
            t.driver_race,
            v.violation,
            COUNT(*) AS violation_count
        FROM traffic_stops t
        JOIN (
            SELECT DISTINCT violation FROM traffic_stops
        ) v ON t.violation = v.violation
        GROUP BY t.driver_age, t.driver_race, v.violation
        ORDER BY violation_count DESC
        LIMIT 10;
    """,
    "⏰ Stops by Year, Month, Hour": """
       SELECT
    EXTRACT(YEAR FROM stop_date::date) AS year,
    EXTRACT(MONTH FROM stop_date::date) AS month,
    LEFT(stop_time, 2) AS hour,
    COUNT(*) AS total_stops
	FROM traffic_stops
	GROUP BY year, month, hour
	ORDER BY year, month, hour;
    """,
     "🚨 Violations with High Search & Arrest Rates": """
        SELECT
            violation,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS searches,
            SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
            ROUND(100.0 * SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent,
            ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent,
            RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) DESC) AS search_rank,
            RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) DESC) AS arrest_rank
        FROM traffic_stops
        GROUP BY violation
        ORDER BY search_rate_percent DESC, arrest_rate_percent DESC
        LIMIT 10;
    """,
     "🌍 Driver Demographics by Country": """
        SELECT
            country_name,
            AVG(driver_age) AS avg_age,
            MODE() WITHIN GROUP (ORDER BY driver_gender) AS most_common_gender,
            MODE() WITHIN GROUP (ORDER BY driver_race) AS most_common_race,
            COUNT(*) AS total_stops
        FROM traffic_stops
        GROUP BY country_name
        ORDER BY total_stops DESC;
    """,
     "🏆 Top 5 Violations by Arrest Rate": """
        SELECT
            violation,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
            ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percent
        FROM traffic_stops
        GROUP BY violation
        HAVING COUNT(*) > 10
        ORDER BY arrest_rate_percent DESC
        LIMIT 5;
    
    """
}

st.markdown(
    "<h3 style='color:#a259c6; font-size:2.2em; font-weight:700; margin-bottom:0.2em;'>📌Advanced Insights</h3>",
    unsafe_allow_html=True
)
selected_query = st.selectbox("", list(query_options.keys()))

if selected_query:
    st.subheader(f"🔎 Result: {selected_query}")
    result_df = run_sql(query_options[selected_query])
    st.dataframe(result_df)

    # Show metrics for top row if possible
    if not result_df.empty:
        cols = result_df.columns
        st.markdown(f"<span class='metric-label'>Rows:</span> <b>{len(result_df)}</b>", unsafe_allow_html=True)
        if len(cols) >= 2:
            st.metric(label=f"Top {cols[0]}", value=str(result_df.iloc[0, 0]))
            st.metric(label=f"Top {cols[1]}", value=str(result_df.iloc[0, 1]))

    # Pie chart results
    if not result_df.empty and result_df.shape[1] >= 2:
        col1, col2 = result_df.columns[:2]
        if result_df[col1].nunique() <= 10 and pd.api.types.is_numeric_dtype(result_df[col2]):
            fig = px.pie(result_df, names=col1, values=col2, title=f"{col2} distribution by {col1}")
            st.plotly_chart(fig, use_container_width=True)

    # Line chart for time-based or numeric x/y
    if not result_df.empty and "hour" in result_df.columns and result_df.shape[1] >= 2:
        st.line_chart(result_df.set_index("hour")[result_df.columns[1]])
    elif not result_df.empty and result_df.shape[1] >= 2 and pd.api.types.is_numeric_dtype(result_df[result_df.columns[0]]):
        st.line_chart(result_df.set_index(result_df.columns[0])[result_df.columns[1]])

    # Download button for results
    if not result_df.empty:
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name='query_results.csv',
            mime='text/csv',
        )

    # Summary statistics
    if not result_df.empty:
        with st.expander("Show summary statistics"):
            st.write(result_df.describe(include='all'))

# ------------------------
# Form Input for New Prediction (Rule-Based)
# ------------------------
st.header("📝 Add New Police Log & Predict Outcome and Violation")

with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    county_name = st.text_input("County Name")
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])
    search_type = st.text_input("Search Type")
    drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
    stop_duration = st.selectbox("Stop Duration", base_df['stop_duration'].dropna().unique())
    vehicle_number = st.text_input("Vehicle Number")
    timestamp = pd.Timestamp.now()

    submitted = st.form_submit_button("Predict Stop Outcome & Violation")

    if submitted:
        filtered_data = base_df[
            (base_df['driver_gender'] == driver_gender) &
            (base_df['driver_age'] == driver_age) &
            (base_df['search_conducted'] == int(search_conducted)) &
            (base_df['stop_duration'] == stop_duration) &
            (base_df['drugs_related_stop'] == int(drugs_related_stop))
        ]

        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"

        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

        st.markdown(f"""
        **Prediction Summary**

        - **Predicted Violation:** {predicted_violation}
        - **Predicted Stop Outcome:** {predicted_outcome}

        A {driver_age}-year-old {driver_gender} driver in {county_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date} ({search_text}), and the stop {drug_text}.
        - Stop duration: **{stop_duration}**
        - Vehicle Number: **{vehicle_number}**
        """)
