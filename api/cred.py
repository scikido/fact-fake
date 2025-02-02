import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import datetime

def calculate_reliability_score(url):
    """
    Calculate a reliability score for a given website URL.
    Returns a score between 0 and 100, where higher scores indicate higher reliability.
    """
    try:
        # Initialize score
        score = 0
        
        # Make request to the website
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10, verify=True)  # Enable SSL verification
        start_time = datetime.now()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Domain Authority Check (increase to 25 points)
        domain = urlparse(url).netloc
        trusted_domains = ['.edu', '.gov', '.org', '.int']  # Added .int for international organizations
        trusted_specific_domains = ['wmo.int', 'who.int', 'un.org', 'unesco.org']  # Add specific trusted domains
        
        if any(domain == td for td in trusted_specific_domains):
            score += 25  # Maximum score for known authoritative domains
        elif any(domain.endswith(td) for td in trusted_domains):
            score += 20
        elif domain.endswith('.com'):
            score += 8

        # 2. Organization Verification (new - 10 points)
        org_indicators = ['world meteorological organization', 'united nations', 'international']
        content_text = soup.get_text().lower()
        if any(ind in content_text for ind in org_indicators):
            score += 10

        # 3. SSL Certificate Check (up to 10 points)
        if url.startswith('https'):
            score += 10
            
        # 4. Load Speed Check (up to 5 points)
        load_time = (datetime.now() - start_time).total_seconds()
        if load_time < 1:
            score += 5
        elif load_time < 2:
            score += 3
        elif load_time < 3:
            score += 1
            
        # 5. Content Analysis (up to 20 points)
        scientific_indicators = ['research', 'study', 'analysis', 'data', 'report', 
                               'scientists', 'experts', 'findings', 'evidence']
        scientific_content_score = sum(1 for ind in scientific_indicators 
                                     if ind in content_text.lower())
        score += min(scientific_content_score * 2, 20)
        
        # 6. Author Credibility (up to 10 points)
        author_elements = soup.find_all(['author', 'byline', 'meta[name*=author]'])
        if author_elements:
            score += 10
            
        # 7. Date Check (up to 10 points)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'\w+ \d{1,2}, \d{4}'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, response.text)
            if dates:
                try:
                    latest_date = max(datetime.strptime(date, '%Y-%m-%d') for date in dates)
                    years_old = (datetime.now() - latest_date).days / 365
                    if years_old < 1:
                        score += 10
                    elif years_old < 2:
                        score += 7
                    elif years_old < 5:
                        score += 4
                except ValueError:
                    continue
                break
                
        # 8. External Links Quality (up to 10 points)
        external_links = [link.get('href') for link in soup.find_all('a', href=True)
                         if link.get('href').startswith('http')]
        reliable_links = sum(1 for link in external_links 
                           if any(td in link for td in trusted_domains))
        score += min(reliable_links * 2, 10)
        
        # 9. Content Length and Quality (up to 10 points)
        content_text = soup.get_text()
        content_length = len(content_text)
        if content_length > 3000:
            score += 10
        elif content_length > 1500:
            score += 7
        elif content_length > 500:
            score += 4
            
        # 10. Mobile Responsiveness Check (up to 5 points)
        viewport_meta = soup.find('meta', {'name': 'viewport'})
        responsive_elements = soup.find_all(['picture', 'source', 'srcset'])
        if viewport_meta:
            score += 3
        if responsive_elements:
            score += 2
            
        # 11. Advertisement Analysis (up to 5 points)
        ad_indicators = ['advertisement', 'sponsored', 'ad-', '-ad', 'banner']
        ad_elements = soup.find_all(class_=lambda x: x and any(ind in x.lower() for ind in ad_indicators))
        if not ad_elements:
            score += 5
        elif len(ad_elements) < 3:
            score += 3
            
        # 12. Writing Style Analysis (up to 5 points)
        # Check for professional writing indicators
        professional_indicators = ['research', 'study', 'analysis', 'conclusion', 'methodology']
        if any(indicator in content_text.lower() for indicator in professional_indicators):
            score += 5
            
        return min(score, 100)  # Cap the score at 100
        
    except Exception as e:
        print(f"Error analyzing URL: {str(e)}")
        return 0

# Example usage
if __name__ == "__main__":
    test_url = "https://www.facebook.com/photo.php?fbid=10166189455015300&id=50576790299&set=a.10151908674545300"
    reliability_score = calculate_reliability_score(test_url)
    # print(f"Reliability Score: {reliability_score}/100")
    
