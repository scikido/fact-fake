# Fact/Fake Verifier Chrome Extension

![alt text](https://i.postimg.cc/YSHwpXFC/Screenshot-2025-02-02-at-11-27-29-PM.png)


A Chrome extension that helps users verify the credibility of information by analyzing claims and checking them against reliable sources.

## Features

- Extract key factual claims from text using Google's Gemini AI
- Analyze claims across multiple trusted news sources
- Calculate reliability scores for source websites
- User-friendly interface with claim navigation
- Visual representation of credibility scores
- Support for multiple claims analysis

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (FastAPI)
- **AI/ML**: Google Gemini AI
- **APIs**: 
  - Google Custom Search Engine
  - Google Fact Check Tools
- **Data Visualization**: Chart.js
- **Build Tools**: Webpack

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd fact-fake-verifier
```


2. Install frontend dependencies:
```bash
npm install
```


3. Install backend dependencies:
```bash
cd api
pip install -r requirements.txt
```


4. Set up environment variables:
Create a `.env` file in the `api` directory with:

```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
GEMINI_API_KEY=your_gemini_api_key
```


5. Build the frontend:
```bash
npm run build
```


6. Start the backend server:
```bash
cd api
uvicorn main:app --reload
```


## Loading the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the extension directory

## How It Works

1. Users input text they want to verify
2. The extension extracts key claims using Gemini AI
3. Each claim is searched across reliable news sources
4. Sources are analyzed for credibility based on multiple factors:
   - Domain authority
   - SSL certification
   - Content quality
   - Author credibility
   - Publication date
   - External links
   - Mobile responsiveness
   - Advertisement presence
   - Writing style

## API Endpoints

- `POST /check_fake_news`: Accepts article text and returns analyzed claims with credibility scores

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Acknowledgments

- Google Gemini AI for claim extraction
- Chart.js for data visualization
- FastAPI for backend services