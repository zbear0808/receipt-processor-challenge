# Testing the Receipt Processor Service

This document outlines how to set up and test the Receipt Processor microservice.

## Docker instructions

run these in the project directory

```bash
docker build -t testing
```

```bash
docker run -p 8080:80 testing
```

this will start the service and map the container's port 80 to the localhost port 8080


## Local Setup (alternative option)

### Prerequisites

- Python 3.7+ installed
- `pip` (Python package installer)


  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Service

1.  **Start the FastAPI server using Uvicorn (from within the `receipt-processor` directory):**
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    *   `app.main:app`: Tells Uvicorn where to find the FastAPI application instance (`app` object inside `app/main.py`).
    *   `--reload`: Enables auto-reloading when code changes are detected (useful for development).
    *   `--port 8000`: Specifies the port to run the server on.

    The server should now be running at `http://127.0.0.1:8000`. You can also access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

# Testing the Endpoints

Use tools like `curl` or Postman

## 1. Submit a Receipt (`POST /receipts/process`)

*   **URL:** `http://127.0.0.1:8000/receipts/process` or `http://localhost:8080/receipts/process`
*   **Method:** `POST`
*   **Headers:** `Content-Type: application/json`
*   **Body:** A JSON object representing the receipt. You can use the examples provided in the `examples/` directory of the main project (e.g., `../examples/simple-receipt.json`).

**Example using `curl` (run from the `receipt-processor` directory):**

```bash
curl -X POST http://127.0.0.1:8000/receipts/process \
-H "Content-Type: application/json" \
-d @../examples/simple-receipt.json

```


Expected Response:

A JSON object containing the generated ID for the receipt.

```json
{
  "id": "some-unique-identifier"
}
(The actual ID will be a UUID)
```

### 2. Get Points for a Receipt (GET /receipts/{id}/points)

URL: http://127.0.0.1:8000/receipts/{id}/points (Replace {id} with the ID received from the previous step)
Method: GET
Example using curl (replace some-unique-identifier with the actual ID):

curl http://127.0.0.1:8000/receipts/some-unique-identifier/points
Expected Response shape:

A JSON object containing the points awarded 

```json
{
  "points": 0
}
```

If the ID is not found:

Status Code: 404 Not Found
Response Body:

```json
{
  "detail": "No receipt found for that ID."
}
```

Stopping the Service
Press Ctrl+C in the terminal where Uvicorn is running. If you used a virtual environment, you can deactivate it with the command deactivate.


