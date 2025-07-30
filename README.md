# Alpaca Trader Bot

This project consists of a React frontend and a FastAPI backend for an algorithmic trading bot.

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

*   Node.js (LTS version recommended)
*   Python 3.13+

### Setup Instructions

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone https://github.com/ItsKillionaire/TradeUp.git # Replace with your repository URL if different
    cd TradeUp
    ```

2.  **Set up the Backend:**

    Navigate to the `backend` directory, create a virtual environment, install dependencies, and create a `.env` file.

    ```bash
    cd backend
    python3.13 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    
    # Create a .env file in the backend directory with your Alpaca API keys
    # Example .env content:
    # ALPACA_API_KEY="YOUR_ALPACA_API_KEY"
    # ALPACA_SECRET_KEY="YOUR_ALPACA_SECRET_KEY"
    # ALPACA_BASE_URL="https://paper-api.alpaca.markets" # Or live API URL
    # TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" # Optional
    # TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID" # Optional
    
    deactivate # Deactivate the virtual environment
    cd .. # Go back to the project root
    ```

3.  **Set up the Frontend:**

    Navigate to the `frontend` directory and install its dependencies.

    ```bash
    cd frontend
    npm install
    cd .. # Go back to the project root
    ```

### Running the Project

To start both the frontend and backend services simultaneously:

1.  **Navigate to the `frontend` directory:**

    ```bash
    cd frontend
    ```

2.  **Run the development command:**

    ```bash
    npm run start:dev
    ```

    This command will:
    *   Start the React development server for the frontend (usually on `http://localhost:3000`).
    *   Start the FastAPI backend server (usually on `http://localhost:8000`).

3.  **Access the Application:**

    Open your web browser and go to `http://localhost:3000`.

## Running Tests

To run the backend tests:

1.  **Ensure you are in the project root directory:**

    ```bash
    cd /path/to/your/alpaca_trader_bot # Replace with your actual project root path
    ```

2.  **Execute the pytest command:**

    ```bash
    PYTHONPATH=backend backend/.venv/bin/pytest backend/tests/
    ```

    This command sets the Python path to include the `backend` directory and then runs all tests located in the `backend/tests/` directory using `pytest`.