# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app import detect_fake_news

# FastAPI app instance
app = FastAPI()

# Request model to capture article text
class ArticleRequest(BaseModel):
    article_text: str

# FastAPI endpoint for checking fake news
@app.get("/check_fake_news")
async def check_fake_news(request: ArticleRequest):
    try:
        # Calling the detect_fake_news function from the fake_news_detector.py file
        result = detect_fake_news(request.article_text)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
