# Citation Crawler

A web application that analyzes essays and finds supporting citations and research papers from academic sources.

## Features

- **Essay Analysis**: Uses OpenAI's GPT to extract key factual claims from submitted essays
- **Citation Finding**: Searches for supporting articles and research papers using Exa API
- **Academic Sources**: Focuses on scholarly sources including Google Scholar, PubMed, JSTOR, and arXiv
- **Quote Extraction**: Displays relevant quotes from found articles that support each claim

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - `OPENAI_API_KEY`: Get from [OpenAI](https://platform.openai.com/api-keys)
     - `EXA_API_KEY`: Get from [Exa](https://exa.ai/)

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Open your browser to `http://localhost:5001`

## Usage

1. Paste your essay into the text area
2. Click "Find Citations"
3. The application will:
   - Extract key claims from your essay
   - Search for supporting articles for each claim
   - Display links and relevant quotes from found sources

## API Endpoints

- `GET /` - Main page with essay input form
- `POST /analyze` - Analyzes essay and returns citations
  - Request body: `{"essay": "your essay text"}`
  - Response: `{"claims": [...], "results": [...]}`

## Dependencies

- Flask - Web framework
- OpenAI - For essay analysis and claim extraction
- Requests - For API calls
- python-dotenv - For environment variable management