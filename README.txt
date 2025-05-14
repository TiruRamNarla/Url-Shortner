

# **TIRU RAM NARLA URL Shortener**

A lightweight URL shortening service built using **Flask** and **SQLite**, designed to generate compact links and track how many times they are accessed.

---

## 📌 Features

* 🔗 Convert long URLs into short, 6-character links
* 🧠 Uses MD5 hashing for deterministic short URLs
* 🗃️ Stores mappings in a local SQLite database
* 📊 Tracks how many times each short URL is visited
* 🌐 Web interface for URL input
* 📡 JSON API for programmatic access

---

## 🏗️ How It Works

1. The app hashes the original URL using MD5.
2. The first 6 characters of the hash are used as the short URL.
3. The mapping is stored in a SQLite database (`urls.db`) along with a click counter.
4. When a user accesses a short URL, they are redirected to the original link and the click count is updated.

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── urls.db                # SQLite database (auto-created)
└── templates/
    └── index.html         # HTML front-end for URL input
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/tiru-url-shortener.git
   cd tiru-url-shortener
   ```

2. **Install dependencies**

   ```bash
   pip install flask
   ```

3. **Create the `index.html` file in the `templates/` folder**

   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>URL Shortener</title>
   </head>
   <body>
       <h1>TIRU RAM NARLA URL Shortener</h1>
       <form id="shorten-form">
           <input type="text" id="long_url" placeholder="Enter your long URL" required>
           <button type="submit">Shorten</button>
       </form>
       <div id="result"></div>
       <script>
           document.getElementById('shorten-form').onsubmit = async function(e) {
               e.preventDefault();
               const response = await fetch('/shorten', {
                   method: 'POST',
                   headers: { 'Content-Type': 'application/json' },
                   body: JSON.stringify({ long_url: document.getElementById('long_url').value })
               });
               const data = await response.json();
               if (data.short_url) {
                   document.getElementById('result').innerText = 'Short URL: ' + window.location.href + data.short_url;
               } else {
                   document.getElementById('result').innerText = 'Error: ' + data.error;
               }
           }
       </script>
   </body>
   </html>
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

   The server starts at `http://127.0.0.1:5000/`

---

## 🧪 API Endpoints

### `POST /shorten`

Shortens a long URL.

**Request Body (JSON):**

```json
{
  "long_url": "https://example.com"
}
```

**Response:**

```json
{
  "short_url": "abc123"
}
```

---

### `GET /<short_url>`

Redirects to the original long URL and increments the visit count.

---

## 🗄️ Database Details

* **Database:** `urls.db`
* **Table:** `url_map`
* **Columns:**

  * `short_url` – 6-character hashed ID
  * `long_url` – Original URL
  * `clicks` – Number of times the short URL has been visited

The `clicks` column is automatically created if missing.

---

## 📌 Notes

* The same long URL will always generate the same short URL (deterministic hashing).
* If a short URL already exists in the database, it's reused.
* Ideal for internal tools or as a learning project for Flask and databases.

---

## 🙋 Author

**TIRU RAM NARLA**

---


