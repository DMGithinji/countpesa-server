# Feedback Forwarder API

A simple FastAPI server that forwards feedback data to a specified Google Sheet. This project is designed to be reusable across multiple projects, each with its own feedback Google Sheet.

## Features

- Accepts feedback via a POST request to `/feedback/` with a JSON payload
- Forwards feedback data (type, message, email, and timestamp) to a Google Sheet specified in the request
- Includes a health check endpoint at `/health`

## Project Structure

```
feedback-forwarder/
├── .env                # Environment variables for Google Sheets credentials
├── .gitignore          # Git ignore file
├── main.py             # FastAPI application
├── g_sheet.py          # Google Sheets integration logic
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies
```

## Prerequisites

- Python 3.8+
- A Google Cloud project with the Google Sheets API enabled
- A Google Service Account with credentials
- Google Sheets created for feedback storage

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd feedback-forwarder
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Google Service Account credentials:

```
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account-email
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email
UNIVERSE_DOMAIN=googleapis.com
```

* Replace the placeholders with values from your Google Service Account key file (JSON format).

### 5. Set Up Google Sheets

* Create a Google Sheet named `justTLDR_Feedback` (or any name, but it must match the workSheetType mapping in g_sheet.py).
* Share the sheet with your service account email (e.g., your-service-account-email@your-project-id.iam.gserviceaccount.com) with **Editor** permissions.
* See the "Google Sheets Setup Process" section below for detailed steps.

### 6. Run the Server

```bash
uvicorn main:app --reload
```

* The API will be available at http://127.0.0.1:8000
* Use `/docs` for the interactive Swagger UI

## API Endpoints

### POST `/feedback/`

Submit feedback to a specified Google Sheet.

* **Request Body**:
  ```json
  {
    "google_sheet": "justTLDR_Feedback",
    "message": "Great app!",
    "type": "normal",
    "email": "user@example.com"
  }
  ```
  * `google_sheet`: Required. The name of the Google Sheet (must match a key in g_sheet.py).
  * `message`: Required. The feedback message.
  * `type`: Optional. The type of feedback (e.g., positive, negative).
  * `email`: Optional. The user's email.

* **Response**:
  ```json
  {
    "status": "success",
    "message": "Feedback submitted successfully"
  }
  ```

### GET `/health`

Check if the server is running.

* **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

## Google Sheets Setup Process

### 1. Create the Google Sheet

* Go to Google Sheets.
* Create a new spreadsheet.
* Name it eg `justTLDR_Feedback` (Take note of that name, it'll be used in your requests).

### 2. Enable Google Sheets API

* Go to the Google Cloud Console.
* Create a new project (or select an existing one).
* Navigate to **"APIs & Services" > "Library"**.
* Search for "Google Sheets API" and click "Enable".

### 3. Create a Service Account

* In the Google Cloud Console, go to **"IAM & Admin" > "Service Accounts"**.
* Click **"Create Service Account"**.
   * Enter a name (e.g., feedback-forwarder).
   * Skip the "Grant this service account access" step (not needed for Sheets).
   * Skip the "Grant users access" step.
* After creation, click on the service account, go to the **"Keys"** tab, and click **"Add Key" > "Create new key"**.
   * Select **JSON** and download the key file.
* Open the JSON file and copy the values into your .env file.

### 4. Share the Google Sheet with the Service Account

* Open your Google Sheet.
* Click the **"Share"** button in the top-right corner.
* In the "Share with people and groups" field, paste the client_email from your .env file (e.g., your-service-account-email@your-project-id.iam.gserviceaccount.com).
* Set the permission to **"Editor"** (this allows the service account to append rows).
* Click **"Send"** or **"Done"**.

### 5. Verify the Setup

* Run the server and send a test request:
  ```bash
  curl -X POST "http://127.0.0.1:8000/feedback/" \
  -H "Content-Type: application/json" \
  -d '{"google_sheet": "justtldr_feedback", "message": "Test feedback"}'
  ```
* Check your Google Sheet for a new row with the feedback data.

## Notes

* The Google Sheet must exist and be shared with the service account before the API can write to it.
* The sheet's first tab (sheet1) is used by default. If you need to use a different tab, modify the get_worksheet function in g_sheet.py to select the desired tab (e.g., spreadsheet.worksheet("Sheet2")).