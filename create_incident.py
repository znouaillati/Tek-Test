import requests
import json

# ServiceNow instance details
INSTANCE = 'https://dev220312.service-now.com'  # Replace with your instance URL
USER = 'admin'  # Replace with your ServiceNow username
PASSWORD = 'Clab=9!j4LSA'  # Replace with your ServiceNow password

# Define the incident data
sdescription = input("Enter Short Description")
description = input("Write detailed description of the issue: ")
impact = input("Enter impact (1: High, 2: Medium, 3: Low): ")
urgency = input("Enter urgency (1: High, 2: Medium, 3: Low): ")
category = input("Choose category \'Inquiry Help\', \'Software\', \'Hardware\', \'Network\', \'Database\'")
incident_data = {
    "short_description": sdescription,
    "description": description,
    "impact": impact,
    "urgency": urgency,
    
    "category": category  # Specify category as needed
}

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Make the API request to create the incident
response = requests.post(
    f"{INSTANCE}/api/now/table/incident",
    auth=(USER, PASSWORD),
    headers=headers,
    data=json.dumps(incident_data)
)

# Check the response
if response.status_code == 201:
    print("Incident created successfully.")
    print("Incident Number:", response.json()['result']['number'])
else:
    print("Failed to create incident.")
    print("Response Code:", response.status_code)
    print("Response Message:", response.text)
