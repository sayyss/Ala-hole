from flask import Flask, render_template, request, jsonify
import openai
import requests
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
EXA_API_KEY = os.getenv('EXA_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_essay():
    try:
        essay = request.json.get('essay', '')
        
        if not essay:
            return jsonify({'error': 'No essay provided'}), 400
        
        # Step 1: Extract claims from essay using LLM
        claims = extract_claims_from_essay(essay)
        
        # Step 2: Find supporting articles for each claim
        results = []
        for claim in claims:
            supporting_articles = find_supporting_articles(claim)
            results.append({
                'claim': claim,
                'articles': supporting_articles
            })
        
        return jsonify({
            'claims': claims,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_claims_from_essay(essay: str) -> List[str]:
    """Extract factual claims from the essay using OpenAI."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Extract the key factual claims and arguments from the given essay. Return them as a numbered list of bullet points. Focus on claims that can be verified with research or citations."
                },
                {
                    "role": "user",
                    "content": f"Extract the key factual claims from this essay:\n\n{essay}"
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        claims_text = response.choices[0].message.content
        
        # Parse the numbered list into individual claims
        claims = []
        for line in claims_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-')):
                # Remove numbering and bullet points
                clean_claim = line.split('.', 1)[-1].strip() if '.' in line else line.strip('•-').strip()
                if clean_claim:
                    claims.append(clean_claim)
        
        return claims
    
    except Exception as e:
        print(f"Error extracting claims: {e}")
        return []

def find_supporting_articles(claim: str) -> List[Dict]:
    """Find supporting articles using Exa API."""
    try:
        headers = {
            'Authorization': f'Bearer {EXA_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'query': claim,
            'type': 'keyword',
            'useAutoprompt': True,
            'numResults': 10,
            'includeDomains': ['scholar.google.com', 'pubmed.ncbi.nlm.nih.gov', 'jstor.org', 'arxiv.org'],
            'contents': {
                'text': True,
                'highlights': {
                    'numSentences': 3,
                    'highlightsPerUrl': 2
                }
            }
        }
        
        response = requests.post('https://api.exa.ai/search', 
                               headers=headers, 
                               json=data)
        
        if response.status_code == 200:
            search_results = response.json()
            articles = []
            
            for result in search_results.get('results', []):
                article = {
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'publishedDate': result.get('publishedDate', ''),
                    'quotes': []
                }
                
                # Extract quotes/highlights
                if 'highlights' in result:
                    article['quotes'] = result['highlights']
                elif 'text' in result:
                    # If no highlights, extract relevant sentences from text
                    text = result['text'][:1000]  # Limit text length
                    article['quotes'] = [text]
                
                articles.append(article)
            
            return articles
        
        return []
    
    except Exception as e:
        print(f"Error finding articles: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)