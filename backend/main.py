import sys
import requests
import json
from pydantic import BaseModel

class Company(BaseModel):
    name: str
    funding: int
    industry: str
    founded: int


class WebsiteAnalysis(BaseModel):
    companies: list[Company]

def main():
    if len(sys.argv) < 2:
        print("Please provide a website URL as an argument")
        sys.exit(1)
    
    website = sys.argv[1]
    website = "https://r.jina.ai/" + website

    try:
        # Fetch website content
        response = requests.get(website)
        response.raise_for_status()  # Raise an exception for bad status codes
        content = response.text

        # Limit content length to first 2000 characters
        content = content[:2000]
        print("Website content (truncated):")
        print(content)
        print("\n" + "="*50 + "\n")

        # Prepare the request to Ollama API
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

        print("Sending request to Ollama API...")
        # Send request to Ollama API with timeout
        ollama_response = requests.post(
            "http://localhost:11434/api/chat",
            json=ollama_data,
            timeout=30  # 30 second timeout
        )
        ollama_response.raise_for_status()

        # Print raw response for debugging
        print("\nRaw Ollama API Response:")
        print(json.dumps(ollama_response.json(), indent=2))
        print("\n" + "="*50 + "\n")

        # Parse and validate the response
        result = ollama_response.json()
        analysis = WebsiteAnalysis.model_validate_json(result['message']['content'])
        
        print("\nExtracted Companies:")
        for company in analysis.companies:
            print(f"\nCompany: {company.name}")
            print(f"Industry: {company.industry}")
            print(f"Funding: ${company.funding:,}")
            print(f"Founded: {company.founded}")

    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

