# Alpaca Trader Bot

This project consists of a React frontend and a FastAPI backend for an algorithmic trading bot.

## Getting Started

This project has been streamlined to ensure a simple and reliable setup and execution process.

### Prerequisites

*   Node.js (LTS version recommended)
*   Python 3.13+

### 1. Setup

First, you need to create a `.env` file in the `backend` directory with your Alpaca API keys.

**Example `backend/.env`:**
```
ALPACA_API_KEY="YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY="YOUR_ALPACA_SECRET_KEY"
ALPACA_BASE_URL="https://paper-api.alpaca.markets" # Or live API URL
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" # Optional
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID" # Optional
```

### 2. Running the Application

To start both the frontend and backend services, simply run the development script from the project root:

```bash
./run_dev.sh
```

This single command will start:
*   The FastAPI backend server on `http://localhost:8000`.
*   The React development server on `http://localhost:3000`.

You can access the application in your web browser at `http://localhost:3000`.

## Running Tests

To run the backend tests, execute the following command from the project root:

```bash
PYTHONPATH=backend backend/.venv/bin/pytest backend/tests/
```
