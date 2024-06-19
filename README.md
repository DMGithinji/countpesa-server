# CountPesa Server

This is a simple Django application that is designed to perform two primary functions:

**1. Statement Parsing**: It takes M-Pesa statements as input along with the statement password and extracts transaction details, returning the transactions to the client. The application does not store the transaction data or the original statement PDFs.

**2. Feedback Forwarding**: Functionality to forward user feedback to Google Sheets, facilitating easy aggregation and analysis of user responses.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose (optional)
- Python 3.8 or higher
- Access to a Google Sheets API service account (for feedback forwarding)

## Setup
### 1. Clone the Repository

Start by cloning this repository to your local machine:

```
git clone https://github.com/DMGithinji/countpesa-server.git
cd countpesa-server
```

### 2. Environment Variables
Create a `.env` file in the project root directory and populate it with the necessary environment variables.

A sample env file is provided under `.env.sample`:


### 3. Build and Run with Docker


To build and run the application using Docker:

```
docker build -t app .
docker run -p 8000:8000 --env-file .env app
```

Alternatively, if you are using Docker Compose:

```
docker-compose up --build
```

## Usage
### Parsing M-Pesa Statements
To parse an M-Pesa statement:

- Access the endpoint: `http://localhost:8000/process_pdf/`
- Upload your M-Pesa statement PDF and password.
- The service will return the parsed transaction details.
- For the `http://localhost:8000/v2/process_pdf/` endpoint, data is encrypted in transit.

## Contributing
Contributions to the project are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request. You can also open an issue to discuss any changes or improvements.
