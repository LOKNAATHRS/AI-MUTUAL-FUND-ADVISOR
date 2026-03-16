import requests
 
OLLAMA_API = "http://localhost:11434/api/generate"
 
def generate_answer(question, context, profile, funds):
 
    prompt = f"""
You are an AI financial advisor.
 
User Risk Profile: {profile}
 
Recommended Mutual Funds:
{funds}
 
Knowledge Context:
{context}
 
User Question:
{question}
 
Give a helpful explanation in simple language.
"""
 
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
 
    # Fix: catch all request errors so the endpoint returns a friendly message
    # instead of a 500 crash when Ollama is unavailable or times out
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=15)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return "LLM unavailable: Could not connect to Ollama. Please ensure it is running on http://localhost:11434."
    except requests.exceptions.Timeout:
        return "LLM unavailable: Request to Ollama timed out after 15 seconds."
    except requests.exceptions.RequestException as e:
        return f"LLM unavailable: {str(e)}"
 
    result = response.json()
 
    # Ollama typically returns a top-level "response" or a list of results
    if isinstance(result, dict) and "response" in result:
        return result["response"]
 
    # Fallback: try to extract from the first result entry
    if isinstance(result, dict) and "results" in result and isinstance(result["results"], list):
        first = result["results"][0]
        if isinstance(first, dict) and "response" in first:
            return first["response"]
        if isinstance(first, dict) and "content" in first and isinstance(first["content"], list):
            for chunk in first["content"]:
                if isinstance(chunk, dict) and chunk.get("type") == "output_text":
                    return chunk.get("text", "")
 
    # If we get here, return raw JSON as a fallback string
    return str(result)