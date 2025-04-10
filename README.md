# CountPesa Server - M-PESA Statement Parser & Feedback API

A very simple FastAPI service that provides two main functionalities:

1. **Statement Parsing**:
Parses M-PESA, and bank statements from PDF files and extracts transaction details. The application does not store the transaction data or the original statement PDFs.
This api is used by the [frontend application](https://app.countpesa.com) which visualizes the transaction data. This is the web version of the [CountPesa mobile app](https://play.google.com/store/apps/details?id=com.countpesa&utm_source=website&utm_medium=hero&utm_campaign=github_promo).

1. **Feedback Forwarding**: Forwards user feedback to a Google Sheets, facilitating easy aggregation and analysis of user responses and critical errors in the frontend application.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.8 or higher (for local development)
- Access to a Google Sheets API service account (optional if feedback needed)

### 1. Clone the Repository

```bash
git clone https://github.com/DMGithinji/countpesa-server.git
cd countpesa-server
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory based on the provided `.env.sample`. Only necessary if you want to link to Google Sheets for feedback forwarding.

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

### 4. Local Development Setup (Alternative)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- The API will be available at <http://localhost:8000>
- Access `/docs` for the interactive Swagger UI documentation

## Frontend Integration

You can test this server with the frontend application:

- Live web app: [app.countpesa.com](https://app.countpesa.com)
- Source code: [GitHub Repository](https://github.com/DMGithinji/countpesa-web-app)

## Contributing

Contributions to the project are welcome! Here are some ways you can contribute:

### Bank Statement Support

We're looking to expand the service to handle bank statements with the same transaction interface.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Other Improvement Ideas

- Enhanced transaction categorization
- Support for additional financial institutions
- Improved error handling
- Performance optimizations
- Test coverage
