# Company Extractor

A Chrome extension and FastAPI backend that extracts company information from websites using AI.

## Project Structure

```
company-extractor/
├── backend/              # FastAPI backend
│   └── main.py           # API server code
├── frontend/             # Chrome extension frontend
│   └── src/
│       └── entrypoints/
│           └── popup/
│               └── App.svelte  # Extension popup UI
└── requirements.txt      # Python dependencies
```

## Features

- Chrome extension that captures the current webpage URL
- FastAPI backend that processes website content
- AI-powered extraction of company information using Ollama
- Structured output of company details (name, funding, industry, founded year)

## Prerequisites

- Python 3.8+
- Node.js and npm
- Ollama running locally with the llama3.2 model
- Chrome browser

## Setup

### Backend Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```bash
   python backend/main.py
   ```
   The server will run on http://localhost:8000

### Chrome Extension Setup

1. Build the extension:
   ```bash
   cd frontend
   npm init
   npm i -D wxt
   npm run build
   ```

2. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `frontend/dist` directory

## Usage

1. Make sure the FastAPI backend is running
2. Navigate to a webpage you want to analyze
3. Click the extension icon in your Chrome toolbar
4. Click the "Extract Company Info" button
5. The extension will send the current URL to the API
6. Company information will be displayed in the popup

## API Endpoints

### POST /analyze

Analyzes a website and extracts company information.

**Request:**
```json
{
  "url": "example.com"
}
```

**Response:**
```json
{
  "companies": [
    {
      "name": "Example Corp",
      "funding": 1000000,
      "industry": "Technology",
      "founded": 2020
    }
  ]
}
```

## Development

### Backend Development

The backend uses FastAPI and communicates with Ollama to extract company information. Debug information is printed to the console to help troubleshoot issues.

### Frontend Development

The frontend is built with Svelte and uses the Chrome Extension API to interact with the current tab.

## Troubleshooting

- If the API doesn't respond, make sure the FastAPI server is running
- If Ollama doesn't respond, ensure it's running with the llama3.2 model
- Check the console logs in both the backend and Chrome DevTools for errors

## License

MIT
