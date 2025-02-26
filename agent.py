import requests
from bs4 import BeautifulSoup
from groq import Groq
import json
import time



client = Groq(
    api_key="",
)




def scrape_website(url):
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(" ", strip=True)[:5000]  
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

class AIProductManager:
    
    def __init__(self, website, competitors):
        self.website = website
        self.competitors = competitors
        self.analysis = ""
        self.roadmap = ""

    def analyze_website(self):
        
        website_content = scrape_website(self.website)
        competitor_data = {url: scrape_website(url) for url in self.competitors}
        
        prompt = (
            f"Analyze the website: {self.website} with data: {website_content}.\n"
            f"Compare it with competitors: {json.dumps(competitor_data)}.\n"
            f"Provide insights, improvement areas, and a roadmap for enhancements."
        )
        
        return self.call_openai(prompt)

    def validate_suggestions(self, analysis):
        
        prompt = (
            f"Given the website analysis: {analysis}, validate the suggestions.\n"
            f"Ensure improvements are feasible and impactful. Provide refined roadmap."
        )
        
        return self.call_openai(prompt)

    def call_openai(self, prompt):
        
        response = client.chat.completions.create(
            model="deepseek-r1-distill-qwen-32b",
            messages=[{"role": "system", "content": prompt}],
            
        )
        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    website = input("Enter website URL: ")
    competitors = input("Enter competitor URLs (comma-separated): ").split(",")
    
    pm_agent = AIProductManager(website, competitors)
    
    while True:
        print("\nAnalyzing website...")
        analysis = pm_agent.analyze_website()
        print(f"\nAnalysis Report:\n{analysis}")
        
        print("\nValidating suggestions...")
        roadmap = pm_agent.validate_suggestions(analysis)
        print(f"\nRefined Roadmap:\n{roadmap}")
        
        user_feedback = input("\nIs the roadmap satisfactory? (yes/no): ")
        if user_feedback.lower() == "yes":
            print("\nFinal roadmap approved.")
            break
        else:
            print("\nRe-evaluating suggestions...")
