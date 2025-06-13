Project Code Filename:Police_ledger_projectCode.py
# Police_Ledger_logs-Project
Project Title:
SecureCheck Dashboard: A Digital Ledger for Police Post Logs

Project Overview

This project aims to build a comprehensive digital dashboard for analyzing and predicting outcomes of police traffic stops. By leveraging data science techniques, SQL databases, and interactive dashboards, the project provides actionable insights for law enforcement agencies and policymakers to improve road safety, transparency, and operational efficiency.

🚓 SecureCheck Dashboard: Police Post Digital Ledger

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

A modern, interactive dashboard for analyzing and predicting police traffic stop outcomes using Python, SQL, and Streamlit.

📂 Project Structure

🚀 Quick Start

1. Clone the repository:
    ```bash
    git clone https://[github.com/yourusername/yourrepo.git](https://github.com/Vaishnaviwork/Police_Ledger_logs-Project)
    cd yourrepo
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your database:
    - Use [PostgreSQL](https://www.postgresql.org/) and create a table as described in the code.
    - Update the `db_url` in `Police_ledger_projectCode.py` with your credentials.

4. Run the dashboard:
    ```bash
    streamlit run Police_ledger_projectCode.py
    ```

📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Sample Police Stop Data (Stanford Open Policing Project)](https://openpolicing.stanford.edu/data/)


Key Components

1. Data Collection & Storage
Data Source: Police traffic stop records, including details like stop date/time, location, driver demographics, vehicle information, violations, searches, and outcomes.
Database: Data is stored in a relational database (PostgreSQL) using a well-defined schema to ensure data integrity and efficient querying.

2.Data Processing & Cleaning
Python & Pandas: Used to clean and preprocess the data. This includes removing columns with only missing values, filling or dropping NaNs, and standardizing formats.
SQLAlchemy: Facilitates seamless interaction between Python and the SQL database for both data insertion and querying.

3. Database Design
Schema: The database schema is designed to capture all relevant aspects of a traffic stop, such as driver details, stop circumstances, and outcomes.
Normalization: Ensures data is organized efficiently, reducing redundancy and improving query performance.
We used render cloud platform to connect the DB.

5. Interactive Dashboard (Streamlit)
Visualization: The dashboard displays raw data, summary statistics, and advanced analytics using tables and interactive charts (via Plotly).
Filters: Users can filter data by country, time, and other attributes for targeted analysis.
Advanced Insights: Predefined SQL queries provide insights such as:
Most common violations and vehicles
Arrest/search rates by time, country, or demographic
Trends by year, month, and hour
Demographic breakdowns and violation patterns
Prediction: Users can input new stop details to predict likely outcomes and violations using rule-based logic derived from historical data.

8. Analytics & Insights
SQL Queries: Advanced queries (including window functions and subqueries) are used to extract trends, compare day/night arrest rates, analyze violation patterns, and more.
Visualization: Results are visualized as tables, pie charts, and line charts for easy interpretation.

Project Goals & Benefits
Transparency: Provides a clear, data-driven view of police stop activity.
Efficiency: Enables quick lookups and analytics for operational decision-making.
Predictive Power: Assists officers in anticipating likely outcomes based on historical patterns.
Policy Support: Informs policymakers about trends and potential areas for intervention (e.g., high-risk times, demographic disparities).
User-Friendly: The Streamlit dashboard makes complex analytics accessible to non-technical users.

Conclusion
This project demonstrates how modern data science tools can transform raw police log data into actionable intelligence. By integrating Python, postgreSQL, render and Streamlit, it delivers a robust, interactive platform for monitoring, analyzing, and improving police traffic stop operations.

⭐️ Show your support

If you like this project, please ⭐️ the repo and share it!
 

