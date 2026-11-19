# Guess 2/3 of the Average Game

A web-based implementation of the famous game theory experiment, "Guess 2/3 of the Average" (also known as the Keynesian Beauty Contest), built with Python (Flask) and SQLite.

## About the Game
In this game, participants are asked to pick a number between 1 and 100. The winner is the person whose number is closest to **two-thirds of the average** of all the numbers submitted.

## Features
- **User Interface:** Clean and responsive UI built with Bootstrap 5.
- **Data Visualization:** Admin dashboard uses Matplotlib to generate real-time histograms and interval charts of the guesses.
- **Database:** Lightweight SQLite database to store participants and their guesses.
- **Admin Panel:** Password-protected page to view analytics and declare the winner.

## Getting Started

### Prerequisites
- Python 3.8 or higher.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/guess-the-average.git
   cd guess-the-average
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

## Admin Access
To view the final results and charts, navigate to `/final_result`. The default admin password is `masih998` (you can change this by setting an environment variable `ADMIN_PASSWORD`).

## How it works
Once the admin logs in, the app calculates the average, the two-thirds average, plots the distribution of guesses, identifies the winner, and then automatically clears the database for the next round.

## License
This project is licensed under the MIT License.