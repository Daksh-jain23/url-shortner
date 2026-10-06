# URL Shortener

A lightweight, fast, and simple URL Shortener application built with **FastAPI**, **SQLite**, and **Redis** caching, featuring a clean HTML/JS frontend.

---

## Features

- **Fast URL Shortening**: Encodes auto-incrementing database IDs into compact Base62 strings (`a-z`, `A-Z`, `0-9`).
- **Redis Caching**: Caches shortened-to-original URL mappings for ultra-fast redirection and reduced database load (with a 60-second TTL).
- **Persistent Storage**: Uses SQLite to reliably store URL mappings.
- **Deduplication**: Reuses existing short codes if an identical original URL has already been shortened.
- **Interactive UI**: Minimalist web interface to input URLs and immediately receive clickable shortened links.
- **FastAPI Interactive Docs**: Built-in Swagger API documentation via `/docs`.

---

## Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: SQLite3
- **Cache**: Redis
- **Frontend**: HTML5, Vanilla JavaScript
- **Server**: Uvicorn

---

## Project Structure

```text
URL-Shortner/
├── Backend/
│   ├── main.py                 # FastAPI application and route endpoints
│   ├── database.py             # SQLite database connection and schema initialization
│   ├── services/
│   │   └── shorten_logic.py    # URL shortening and resolution logic with Redis caching
│   ├── utils/
│   │   └── base62.py           # Base62 encoding and decoding utilities
│   ├── test_services.py        # Helper script to inspect stored URLs
│   └── urls.db                 # SQLite database file
├── Frontend/
│   └── index.html              # Frontend user interface
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Redis Server** running locally on default port `6379`
  - Linux/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install redis-server
    sudo systemctl start redis-server
    ```
  - macOS (Homebrew):
    ```bash
    brew install redis
    brew services start redis
    ```
  - Docker:
    ```bash
    docker run -d --name redis -p 6379:6379 redis:alpine
    ```

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd URL-Shortner
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. Ensure your Redis server is running:
   ```bash
   redis-cli ping
   # Expected output: PONG
   ```

2. Start the FastAPI development server from the `Backend` directory:
   ```bash
   cd Backend
   fastapi dev main.py
   ```
   *Alternatively, run with uvicorn directly:*
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. Open your browser and navigate to:
   - **Frontend UI**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

| Method | Endpoint | Description | Request / Params | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Serves the web frontend interface | None | HTML file |
| `POST` | `/shorten` | Creates or retrieves a shortened URL | Form data: `url` (str) | `{"short_url": "http://127.0.0.1:8000/<short_code>"}` |
| `GET` | `/{short_code}` | Redirects (302) to original URL | Path parameter: `short_code` | 302 Redirect or error JSON |

---

## How It Works

1. **Generating a Short URL**:
   - The user inputs a URL.
   - The backend checks if the URL already exists in SQLite. If not, it inserts a new record and gets the unique `id`.
   - The `id` is converted to a compact string via Base62 encoding (`encode_base62`).
   - The key `url:<code}>` is cached in Redis with an expiration of 60 seconds.
   - The shortened URL link is returned to the client.

2. **Resolving a Short URL**:
   - When a user accesses `http://127.0.0.1:8000/{short_code}`, Redis is checked first.
   - **Cache Hit**: Instantly redirects to the target URL.
   - **Cache Miss**: Decodes the Base62 string back to the numeric ID (`decode_base62`), queries SQLite for the original URL, populates Redis cache, and redirects (HTTP 302).
