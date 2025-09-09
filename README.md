GameAnalytics-Unlocking-Tennis-data-with-Sportsradar-API

An interactive **Tennis Analytics Dashboard** built with **Streamlit** and **PostgreSQL**, designed to provide insights into player performance, rankings, and match statistics.

## 🚀 Features

* 📊 **Interactive Visualizations**: Explore player rankings, movements, and performance trends.
* 🎨 **Creative UI**: Engaging sidebar, homepage, and time-based greetings.
* 🗄️ **Database Integration**: Powered by PostgreSQL for efficient data storage and querying.
* 🔍 **Search & Filter**: Easily find player stats based on country, ranking, or points.
* 📈 **Dynamic Analytics**: Track top movers, rank changes, and country-wise performance.

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend**: Python
* **Database**: PostgreSQL
* **Visualization**: Plotly, Matplotlib

## 📂 Project Structure

```
tennis-analytics/
│── app.py                # Main entry point for the Streamlit app
│── db.py                 # Database connection & query execution
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
│── app_pages/            # Different pages of the dashboard
│   │── homepage.py
│   │── player_stats.py
│   │── rankings.py
│   │── country_analysis.py
│── data/                 # (Optional) CSV files or seed data
```

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/tennis-analytics.git
   cd tennis-analytics
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**

   * Create a database in PostgreSQL:

     ```sql
     CREATE DATABASE tennisdb;
     ```

   * Import tables and seed data (competitors, rankings, matches, etc.).

   * Update your **db.py** file with credentials:

     ```python
     conn = psycopg2.connect(
         host="localhost",
         database="tennisdb",
         user="your_username",
         password="your_password"
     )
     ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```
   Check out my project at: 
https://www.loom.com/share/a5a6c20a2f8840a39af09c89c8a0c940?sid=0cd7b58e-779b-4f28-a1f4-db1317ae927b
## 📸 Screenshots

*(Add some screenshots of your dashboard here for better presentation)*

## 📈 Future Enhancements

* AI-powered match outcome predictions.
* Integration with live sports APIs (e.g., Sportradar).
* Advanced filters and personalized dashboards.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

## 📜 License

This project is licensed under the MIT License.


