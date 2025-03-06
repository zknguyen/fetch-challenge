# fetch-challenge

This project is a FastAPI application that processes receipts and calculates points based on various criteria. This is for Fetch Rewards receipt-processor-challenge (`https://github.com/fetch-rewards/receipt-processor-challenge`).

## Project Structure

```
fetch-challenge
├── src
│   ├── main.py          # FastAPI application with receipt processing logic
├── test
│   ├── test_main.py     # Contains unit tests for the endpoints
├── fetch-env            # Virtual environment to run the project
├── Dockerfile           # Instructions to build a Docker image for the application
├── requirements.txt     # Python dependencies required for the project
└── README.md            # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fetch-challenge
   ```

2. **Install dependencies:**
   You can install the required Python packages using pip. Make sure you have Python 3.7 or higher installed.
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   You can run the FastAPI application using the following command:
   ```
   uvicorn src.main:app --host 127.0.0.1 --port 8000
   ```

   The application will be accessible at `http://127.0.0.1:8000/docs`. This will take you to the SwaggerUI page.

## Docker Instructions

To build and run the application using Docker, follow these steps:

1. **Build the Docker image:**
   ```
   docker build -t fetch-challenge .
   ```

2. **Run the Docker container:**
   ```
   docker run -d -p 8000:8000 fetch-challenge
   ```

   The application will be accessible at `http://localhost:8000`.

## Usage

### Endpoints

- **POST /receipts/process**
  - Submit a receipt for processing.
  - Request body should include retailer, purchaseDate, purchaseTime, total, and items.

- **GET /receipts/{id}/points**
  - Retrieve the points associated with a specific receipt ID.