from flask import Flask, request, jsonify, redirect, render_template
from hashlib import md5
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Check if 'clicks' column exists, if not, add it
    cursor.execute('PRAGMA table_info(url_map);')
    columns = [column[1] for column in cursor.fetchall()]
    if 'clicks' not in columns:
        cursor.execute('ALTER TABLE url_map ADD COLUMN clicks INTEGER DEFAULT 0')

    conn.commit()
    conn.close()

# Helper function to generate a short URL
def generate_short_url(long_url):
    return md5(long_url.encode()).hexdigest()[:6]

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({'error': 'Missing long_url parameter'}), 400

    short_url = generate_short_url(long_url)

    # Save mapping in the database
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO url_map (short_url, long_url, clicks) VALUES (?, ?, ?)', 
                   (short_url, long_url, 0))  # Set initial click count to 0
    conn.commit()
    conn.close()

    return jsonify({'short_url': short_url})

# Route to redirect to original URL and track clicks
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url, clicks FROM url_map WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()

    if result:
        long_url, clicks = result
        # Increment the click count
        cursor.execute('UPDATE url_map SET clicks = ? WHERE short_url = ?', (clicks + 1, short_url))
        conn.commit()
        conn.close()
        return redirect(long_url)
    else:
        conn.close()
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    init_db()  # Call init_db function on app startup to set up the DB
    app.run(debug=True)
