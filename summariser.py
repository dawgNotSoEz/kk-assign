import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from config import api_key

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def summarize_text(text, length="3 lines", language="English"):
    # Determine the number of lines based on length setting
    if length == "3 lines":
        line_count = 3
    elif length == "5 lines":
        line_count = 5
    elif length == "1 paragraph":
        line_count = "a single comprehensive paragraph"
    else:
        line_count = 3
    
    # Build the prompt with language support
    if language == "English":
        prompt = f"Summarize the following text in exactly {line_count} concise lines:\n\n{text}"
    else:
        prompt = f"Summarize the following text in exactly {line_count} concise lines. Provide the summary in {language} language:\n\n{text}"
    
    response = model.generate_content(prompt)
    return response.text

def summarize_url(url, length="3 lines", language="English"):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract main article content (remove scripts, styles, ads)
    for script in soup(["script", "style", "nav", "footer", "aside"]):
        script.decompose()
    
    # Get article text
    article = soup.find('article') or soup.find('main') or soup
    text = article.get_text(separator=' ', strip=True)
    
    # Limit to first 5000 chars to avoid token limits
    text = text[:5000]
    
    return summarize_text(text, length, language)
