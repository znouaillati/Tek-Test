import requests

# ServiceNow credentials
SERVICENOW_INSTANCE = "your_instance.service-now.com"
SERVICENOW_USERNAME = "your_username"
SERVICENOW_PASSWORD = "your_password"

# Function to make ServiceNow API requests
def service_now_api_request(endpoint, query_params=None):
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/{endpoint}"
    headers = {"Content-Type": "application/json"}
    auth = (SERVICENOW_USERNAME, SERVICENOW_PASSWORD)

    try:
        response = requests.get(url, params=query_params, auth=auth, headers=headers)
        response.raise_for_status()
        return response.json().get("result", [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return []

# Fetch users by skill
def fetch_users_by_skill(skill):
    endpoint = "sys_user"
    query_params = {
        "sysparm_query": f"skillsLIKE{skill}",
        "sysparm_fields": "sys_id,name,department",
        "sysparm_limit": 10
    }
    return service_now_api_request(endpoint, query_params)

# Assign incident to the selected user
def assign_incident_to_user(incident_id, user_id):
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/incident/{incident_id}"
    data = {"assigned_to": user_id}
    headers = {"Content-Type": "application/json"}
    auth = (SERVICENOW_USERNAME, SERVICENOW_PASSWORD)

    try:
        response = requests.put(url, json=data, auth=auth, headers=headers)
        response.raise_for_status()
        print(f"Incident {incident_id} successfully assigned to User ID: {user_id}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to assign incident: {e}, Response: {response.text if response else 'No response'}")

# Main function
def main():
    # Example inputs
    incident_id = "INC12345"
    required_skills = ["IT", "network"]

    for skill in required_skills:
        print(f"\nSearching for users with skill: {skill}")
        users = fetch_users_by_skill(skill)

        if not users:
            print(f"No users found with skill: {skill}")
            continue

        # Display users with department
        print(f"Users with skill '{skill}':")
        for idx, user in enumerate(users, start=1):
            user_name = user.get("name", "Unknown")
            department = user.get("department", "Unknown Department")
            print(f"{idx}. {user_name} - {department}")

        # Allow the user to select a user
        while True:
            try:
                selection = int(input(f"\nSelect a user to assign the incident (1-{len(users)}): "))
                if 1 <= selection <= len(users):
                    selected_user = users[selection - 1]
                    user_id = selected_user["sys_id"]
                    print(f"Assigning incident to {selected_user['name']}...")
                    assign_incident_to_user(incident_id, user_id)
                    return  # Exit after assigning
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    print("\nFailed to assign the incident to any user.")

if __name__ == "__main__":
    main()
