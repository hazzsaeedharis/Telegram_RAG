# TelegramRAG: AI-Powered Document Analysis with Web and Telegram Interfaces

**TelegramRAG is a Retrieval-Augmented Generation (RAG) application with a React frontend and a TON-gated Telegram bot, powered by LangChain, OpenAI, and Redis.**


## About The Project

TelegraRAG is a powerful tool for analyzing documents using artificial intelligence. It offers two convenient interfaces: a user-friendly web application and a Telegram bot for on-the-go analysis.

The core of the project is a RAG pipeline that can process Google Docs and PDF files, extract their content, and answer questions based on the information within them. This is made possible by leveraging the power of LangChain for orchestration, OpenAI for language understanding, and Redis for efficient vector storage and retrieval.

A unique feature of this project is the Telegram bot's integration with the TON (The Open Network) blockchain. To access the bot's full capabilities, users are required to make a payment in TON, demonstrating a practical application of cryptocurrency in a real-world application. This not only showcases technical skill in Web3 but also highlights a focus on privacy and decentralized systems.

### Key Features:

*   **Dual Interface:** Access the service through a modern React-based web app or a convenient Telegram bot.
*   **RAG Pipeline:** Efficiently processes and analyzes documents to provide accurate answers to user queries.
*   **TON Payment Integration:** A unique, privacy-focused payment system for the Telegram bot.
*   **Modular Architecture:** A clean and maintainable codebase with a clear separation of concerns between the frontend, backend, and bot.

---

## Built With

*   **Backend:** Python, Flask, LangChain, OpenAI, Redis
*   **Frontend:** React, TypeScript, Styled-Components
*   **Bot:** python-telegram-bot
*   **Database:** Redis (for vector storage)
*   **Deployment:** (Add your deployment platforms, e.g., Vercel, Heroku)

---

## Architecture

The application is composed of three main components:

1.  **Backend (Flask):** A Python-based server that exposes a REST API for indexing documents, asking questions, and managing the vector store.
2.  **Frontend (React):** A single-page application that provides a web interface for interacting with the backend API.
3.  **Telegram Bot:** A Python script that connects to the Telegram API, handles user commands, and communicates with the backend API.


## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8+
*   Node.js v14+
*   Redis

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/hazzsaeedharis/Telegram_RAG.git
    cd Telegram_RAG
    ```
2.  **Backend Setup**
    ```sh
    # Install Python dependencies
    pip install -r requirements.txt

    # Create a .env file in the root directory and add your API keys
    cp .env.example .env
    ```
    Your `.env` file should look like this:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
    TON_WALLET_ADDRESS="your_ton_wallet_address"
    BACKEND_URL="http://localhost:5001"
    ```
3.  **Frontend Setup**
    ```sh
    # Navigate to the frontend directory
    cd frontend

    # Install NPM packages
    npm install
    ```

### Running the Application

1.  **Start Redis**
2.  **Start the Backend Server**
    ```sh
    python app.py
    ```
3.  **Start the Frontend Development Server**
    ```sh
    cd frontend
    npm start
    ```
4.  **Start the Telegram Bot**
    ```sh
    python telegram_bot.py
    ```

---

## Usage

### Web App

1.  Open your browser and navigate to `http://localhost:3000`.
2.  Paste the URL of a Google Doc or PDF into the input field and click "Index Document".
3.  Once the document is indexed, you can ask questions about it in the second input field.

### Telegram Bot

1.  Start a conversation with your bot on Telegram.
2.  Use the `/start` and `/help` commands to get information about the bot.
3.  To unlock the bot's features, send a TON payment to the specified wallet address.
4.  Use the `/pay <transaction_hash>` command to verify your payment.
5.  Once verified, you can send a Google Docs link or upload a file to be indexed.
6.  Ask questions about the indexed document.

---

## Future Improvements

*   Implement a more robust payment verification system for the TON payments.
*   Add support for more document types (e.g., .docx, .txt).
*   Develop a user authentication system for the web app.
*   Improve the conversational abilities of the Telegram bot.
*   Deploy the application to a cloud platform for public access.
