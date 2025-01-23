import requests

# ServiceNow credentials and API URL
SERVICENOW_URL = "dev220312.service-now.com"
SERVICENOW_USERNAME = "admin"
SERVICENOW_PASSWORD = "Clab=9!j4LSA"

# BigPanda credentials and API URL
#BIGPANDA_API_URL = "https://api.bigpanda.io/data/v2/alerts"
#BIGPANDA_TOKEN = "<your-bigpanda-token>"

# Incident Details
incident_details = {
    "summary": "System outage in production",
    "description": "Database connection issues causing downtime",
    "required_skills": ["database", "network", "incident management"]
}

def get_knowledge_articles(skill):
    """Fetch knowledge base articles from ServiceNow based on a skill."""
    url = f"{SERVICENOW_URL}?sysparm_query=short_descriptionLIKE{skill}&sysparm_limit=10"
    response = requests.get(url, auth=(SERVICENOW_USERNAME, SERVICENOW_PASSWORD))
    
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"Failed to fetch knowledge articles: {response.status_code}")
        return []

def get_workers_with_skill(skill):
    """Fetch workers from ServiceNow with a specific skill."""
    url = f"{SERVICENOW_URL}?sysparm_query=skillsLIKE{skill}&sysparm_limit=10"
    response = requests.get(url, auth=(SERVICENOW_USERNAME, SERVICENOW_PASSWORD))
    
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"Failed to fetch workers: {response.status_code}")
        return []

def post_incident_to_bigpanda(incident):
    """Post the incident details to BigPanda."""
    headers = {
        "Authorization": f"Bearer {BIGPANDA_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(BIGPANDA_API_URL, json=incident, headers=headers)
    
    if response.status_code == 202:
        print("Incident posted to BigPanda successfully.")
    else:
        print(f"Failed to post incident to BigPanda: {response.status_code}")

def main():
    # Fetch relevant workers and knowledge articles
    relevant_workers = []
    knowledge_articles = []
    
    for skill in incident_details["required_skills"]:
        workers = get_workers_with_skill(skill)
        articles = get_knowledge_articles(skill)
        
        relevant_workers.extend(workers)
        knowledge_articles.extend(articles)
    
    # Remove duplicates
    relevant_workers = {worker["name"]: worker for worker in relevant_workers}.values()
    knowledge_articles = {article["sys_id"]: article for article in knowledge_articles}.values()
    
    # Post the incident to BigPanda
    post_incident_to_bigpanda(incident_details)
    
    # Display the results
    print("\nRelevant Workers:")
    for worker in relevant_workers:
        print(f"Name: {worker['name']}, Skills: {worker.get('skills', 'N/A')}")
    
    print("\nKnowledge Articles:")
    for article in knowledge_articles:
        print(f"Title: {article['short_description']}, Link: {article['sys_id']}")
    
if __name__ == "__main__":
    main()
