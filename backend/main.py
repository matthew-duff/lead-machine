import sys
import requests
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

class Company(BaseModel):
    name: str
    funding: int
    industry: str
    founded: int

class WebsiteAnalysis(BaseModel):
    companies: List[Company]

class WebsiteRequest(BaseModel):
    url: str

app = FastAPI(
    title="Company Extractor API",
    description="API to extract company information from websites",
    version="1.0.0"
)

@app.post("/analyze", response_model=WebsiteAnalysis)
async def analyze_website(request: WebsiteRequest):
    print(f"Received request to analyze website: {request.url}")
    try:
        website = "https://r.jina.ai/" + request.url
        print(f"Full website URL: {website}")

        # Fetch website content
        print("Fetching website content...")
        response = requests.get(website)
        response.raise_for_status()
        content = response.text
        print(f"Website content fetched successfully. Content length: {len(content)} characters")
        
        # Print the actual content
        print("\n" + "="*50)
        print("WEBSITE CONTENT:")
        print("="*50)
        print(content)
        print("="*50 + "\n")

        # Limit content length to first 2000 characters
        content = content[:2000]
        print(f"Content truncated to {len(content)} characters")
        print("\n" + "="*50)
        print("TRUNCATED CONTENT:")
        print("="*50)
        print(content)
        print("="*50 + "\n")

        # Prepare the request to Ollama API
        print("Preparing request to Ollama API...")
        ollama_data = {
            "model": "llama3.2",
            "messages": [{
                "role": "user",
                "content": "Extract company information from this text. Return a JSON with a list of companies. Each company should have: name (string), funding (integer), industry (string), founded (integer)."
            },
            {
                "role": "user",
                "content": content
            }],
            "stream": False,
            "format": WebsiteAnalysis.model_json_schema(),
            "options": {"num_ctx": 4096}
        }
        print(f"Ollama request data prepared with format: {json.dumps(WebsiteAnalysis.model_json_schema(), indent=2)}")

        # Send request to Ollama API with timeout
        print("Sending request to Ollama API...")
        ollama_response = requests.post(
            "http://localhost:11434/api/chat",
            json=ollama_data,
            timeout=30
        )
        ollama_response.raise_for_status()
        print("Received response from Ollama API")

        # Print raw response for debugging
        result = ollama_response.json()
        print(f"Raw Ollama response: {json.dumps(result, indent=2)}")

        # Parse and validate the response
        print("Parsing and validating response...")
        analysis = WebsiteAnalysis.model_validate_json(result['message']['content'])
        print(f"Successfully extracted {len(analysis.companies)} companies")
        
        return analysis

    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching website: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Company Extractor API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

