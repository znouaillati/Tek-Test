import requests

# ServiceNow API Configuration
SERVICENOW_INSTANCE = "<your-instance>.service-now.com"
SERVICENOW_USERNAME = "<your-username>"
SERVICENOW_PASSWORD = "<your-password>"

# BigPanda API Configuration
BIGPANDA_API_URL = "https://api.bigpanda.io/data/v2/alerts"
BIGPANDA_TOKEN = "<your-bigpanda-token>"

# Helper Function: ServiceNow API Request
def service_now_api_request(endpoint, query_params=None, method="GET", data=None):
    url = f"https://{SERVICENOW_INSTANCE}/{endpoint}"
    auth = (SERVICENOW_USERNAME, SERVICENOW_PASSWORD)
    headers = {"Content-Type": "application/json"}
    
    if method == "GET":
        response = requests.get(url, params=query_params, auth=auth, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, auth=auth, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=data, auth=auth, headers=headers)
    else:
        raise ValueError("Unsupported HTTP method.")
    
    if response.status_code in [200, 201]:
        return response.json().get("result", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Fetch Assigned Incidents
def fetch_assigned_incidents():
    endpoint = "api/now/table/incident"
    query_params = {
        "sysparm_query": "assigned_to=me",  # Modify to fetch incidents for a specific manager
        "sysparm_limit": 10
    }
    return service_now_api_request(endpoint, query_params)

# Fetch Knowledge Base Articles
def fetch_knowledge_articles(query):
    endpoint = "api/now/table/kb_knowledge"
    query_params = {
        "sysparm_query": f"short_descriptionLIKE{query}",
        "sysparm_limit": 5
    }
    return service_now_api_request(endpoint, query_params)

# Update Incident Status
def update_incident_status(incident_id, status):
    endpoint = f"api/now/table/incident/{incident_id}"
    data = {"state": status}  # 'state' field can vary by your ServiceNow setup
    return service_now_api_request(endpoint, method="PUT", data=data)

# Main Script Workflow
def main():
    print("Fetching assigned incidents...")
    incidents = fetch_assigned_incidents()
    
    if not incidents:
        print("No incidents assigned.")
        return
    
    # Display incidents
    print("\nAssigned Incidents:")
    for incident in incidents:
        print(f"- {incident['number']} | {incident['short_description']} | Priority: {incident['priority']}")
    
    # Look up knowledge articles
    print("\nSearching for related knowledge base articles...")
    query = input("Enter a keyword for your search: ")
    articles = fetch_knowledge_articles(query)
    
    if articles:
        print("\nKnowledge Base Articles:")
        for article in articles:
            print(f"- {article['short_description']} (ID: {article['sys_id']})")
    else:
        print("No articles found.")
    
    # Update incident status
    print("\nDo you want to update an incident's status?")
    choice = input("Enter 'yes' or 'no': ").strip().lower()
    if choice == "yes":
        incident_id = input("Enter the incident ID: ")
        new_status = input("Enter the new status (e.g., 'Resolved', 'In Progress'): ")
        update_result = update_incident_status(incident_id, new_status)
        if update_result:
            print("Incident status updated successfully.")
        else:
            print("Failed to update the incident status.")

if __name__ == "__main__":
    main()
