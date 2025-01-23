import requests

# ServiceNow API Configuration
SERVICENOW_INSTANCE = ""
SERVICENOW_USERNAME = ""
SERVICENOW_PASSWORD = ""

# Mapping of skills to departments
skills_to_department = {
    "database": "Database Administration",
    "network": "Network Operations",
    "incident management": "Incident Management Team"
}

# Helper Function: ServiceNow API Request
def service_now_api_request(endpoint, query_params=None, method="GET", data=None):
    url = f"https://{SERVICENOW_INSTANCE}/{endpoint}"
    auth = (SERVICENOW_USERNAME, SERVICENOW_PASSWORD)
    headers = {"Content-Type": "application/json"}
    
    if method == "GET":
        response = requests.get(url, params=query_params, auth=auth, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=data, auth=auth, headers=headers)
    else:
        raise ValueError("Unsupported HTTP method.")
    
    if response.status_code in [200, 201]:
        return response.json().get("result", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Fetch Users by Skill
def fetch_users_by_skill(skill):
    """Fetch users with a specific skill from ServiceNow."""
    endpoint = "api/now/table/sys_user"
    query_params = {"sysparm_query": f"skillsLIKE{skill}", "sysparm_limit": 10}
    return service_now_api_request(endpoint, query_params)

# Assign Incident
def assign_incident(incident_id, user_sys_id):
    """Assign an incident to a specific user."""
    endpoint = f"api/now/table/incident/{incident_id}"
    data = {"assigned_to": user_sys_id}
    return service_now_api_request(endpoint, method="PUT", data=data)

# Main Function to Find and Assign Work
def find_and_assign_work(incident_id, required_skills):
    """Find relevant users or departments and assign the incident."""
    print("\nFinding relevant users or departments for the incident...")
    
    for skill in required_skills:
        print(f"\nSearching for users with skill: {skill}")
        users = fetch_users_by_skill(skill)
        
        if users:
            print("Matching Users:")
            for user in users:
                print(f"- Name: {user['name']}, Department: {user.get('department', 'N/A')}, Email: {user['email']}")
            
            # Choose the first user for simplicity
            chosen_user = users[0]
            user_name = chosen_user["name"]
            user_sys_id = chosen_user["sys_id"]
            
            # Assign the incident to this user
            print(f"Assigning the incident to {user_name}...")
            assign_result = assign_incident(incident_id, user_sys_id)
            if assign_result:
                print(f"Incident assigned to {user_name} successfully.")
            else:
                print(f"Failed to assign the incident to {user_name}.")
            
            return  # Exit after assigning to the first match
        else:
            # No matching users found; fall back to department
            department = skills_to_department.get(skill, "General IT Support")
            print(f"No users found for skill: {skill}. Escalating to department: {department}")
    
    print("No suitable users or departments found. Please review manually.")

# Example Workflow
def main():
    # Example incident details
    incident_id = "INC0010008"
    required_skills = ["IT", "network"]
    
    # Find and assign work
    find_and_assign_work(incident_id, required_skills)

if __name__ == "__main__":
    main()
