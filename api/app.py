import requests
from cred import calculate_reliability_score
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyCXP6iV_m7bCyki5YX74c40jEgPey0nNV4"
GOOGLE_CSE_ID = "712c853b1be2c4096"


# Configure Gemini API
genai.configure(api_key="AIzaSyBesv-lQ6600jT2oPe3qKd0kOiH9askIUM")

# Google Fact Check Tools API Key
FACT_CHECK_API_KEY = "AIzaSyCXP6iV_m7bCyki5YX74c40jEgPey0nNV4"

def extract_claims_from_article(article_text):
    """Use Gemini API to extract key factual claims from the article."""
    model = genai.GenerativeModel('gemini-pro')

    # Set safety settings to be more permissive
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_ONLY_HIGH"
    }
    
    generation_config = {
        "temperature": 0.3,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    prompt = (
        "Extract only the key factual claims from the following text as a simple list "
        "without any headers or bullet points: \n\n"
        f"{article_text}"
    )
    
    try:
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config=generation_config
        )

        result = response._result.candidates[0].content.parts[0].text
        
        return result.split('\n')
        
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return ["Error processing content"]


def search_claim_with_cse(claim):
    """Search for the claim across multiple news sources using Google Custom Search Engine."""
    search_url = f"https://www.googleapis.com/customsearch/v1?q={claim}&cx={GOOGLE_CSE_ID}&key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            search_results = response.json().get("items", [])
            if not search_results:
                return "No results found for this claim"
            
            scores = []
            for item in search_results:
                # title = item['title']
                # print(title)
                link = item['link']
                # print(link)
                reliability_score = calculate_reliability_score(link)
                scores.append({'link': link, 'reliability_score': reliability_score})

            return scores


        else:
            return f"Error (Status {response.status_code}): {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
    
def detect_fake_news(article_text):
    """Main pipeline for fake news detection."""
    print("\n🔹 Extracting Claims using Gemini API...")
    claims = extract_claims_from_article(article_text)
    


    results = []
    for claim in claims:
        print(f"\n🔹 Analyzing Claim: {claim}")
        scores = search_claim_with_cse(claim)

        results.append({
            "claim": claim,
            "scores": scores,
        })

    return results


# def print_results(results):
#     print("\n📊 FACT CHECK ANALYSIS REPORT")
#     print("=" * 50)
    
#     for idx, result in enumerate(results, 1):
#         print(f"\n📌 Claim {idx}: {result['claim']}")
#         print(f"├── Scores: {result['scores']}")
#         print("-" * 50)

# news_article = """A National Mission on High Yielding Seeds to be launched aiming at strengthening the research ecosystem, targeted development and propagation of seeds with high yield, and commercial availability of more than 100 seed varieties.
# """
# result = detect_fake_news(news_article)
# print_results(result)