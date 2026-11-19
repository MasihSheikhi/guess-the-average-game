import sqlite3
import io
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session

# Set matplotlib backend to Agg to prevent GUI errors in web servers
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Security configurations (use environment variables in production)
app.secret_key = os.environ.get('SECRET_KEY', 'your_development_secret_key')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'masih998')

# Database setup (relative path so it works anywhere)
DATABASE = os.path.join(os.path.dirname(__file__), 'guess_game.db')

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS guesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                guess INTEGER NOT NULL
            )
        ''')
        conn.commit()

def reset_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    init_db()

# Initialize the database when the app starts
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        count = conn.execute('SELECT COUNT(*) FROM guesses').fetchone()[0]
    return render_template('index.html', count=count)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    guess = request.form.get('guess')

    # Validate the guess
    try:
        guess = int(guess)
        if guess < 1 or guess > 100:
            return "Please enter a number between 1 and 100.", 400
    except ValueError:
        return "Please enter a valid number.", 400

    # Save the data to the database
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO guesses (name, guess) VALUES (?, ?)', (name, guess))
        conn.commit()
        count = conn.execute('SELECT COUNT(*) FROM guesses').fetchone()[0]

    return render_template('thank_you.html', count=count)

@app.route('/final_result', methods=['GET', 'POST'])
def final_result():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('show_results'))
        else:
            return "Only developers have access to this section. Incorrect password.", 403
    return render_template('final_result.html')

@app.route('/results')
def show_results():
    if not session.get('authenticated'):
        return "Only developers have access to this section.", 403

    with sqlite3.connect(DATABASE) as conn:
        guesses = [row[0] for row in conn.execute('SELECT guess FROM guesses').fetchall()]

    if not guesses:
        return "No guesses recorded yet."

    average = sum(guesses) / len(guesses)
    two_thirds_avg = (2 / 3) * average

    # Create the original distribution chart
    plt.figure(figsize=(12, 6))

    # Chart 1: Original histogram
    plt.subplot(1, 2, 1)
    plt.hist(guesses, bins=range(1, 101), edgecolor='black', color='skyblue')
    plt.title('Distribution of Guesses')
    plt.xlabel('Guess')
    plt.ylabel('Frequency')

    # Chart 2: Interval-based histogram
    plt.subplot(1, 2, 2)
    bins = range(1, 101, 10)  # Intervals: 1-10, 11-20, ..., 91-100
    plt.hist(guesses, bins=bins, edgecolor='black', color='lightgreen')
    plt.title('Guesses by Intervals')
    plt.xlabel('Guess Intervals')
    plt.ylabel('Frequency')
    plt.xticks(bins, [f'{i}-{i+9}' for i in bins], rotation=45)

    # Save the combined chart to a base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close() # Close the plot to free memory

    # Find the winner
    with sqlite3.connect(DATABASE) as conn:
        winner = conn.execute('''
            SELECT name, guess FROM guesses
            ORDER BY ABS(guess - ?) LIMIT 1
        ''', (two_thirds_avg,)).fetchone()

    # Reset the database for the next round
    reset_db()

    return render_template('results.html',
                          plot_url=plot_url,
                          average=average,
                          two_thirds_avg=two_thirds_avg,
                          winner=winner)

if __name__ == '__main__':
    app.run(debug=True)