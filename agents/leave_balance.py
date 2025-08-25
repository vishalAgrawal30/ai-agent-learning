import json
import requests
from langchain_core.tools import tool
import agents.shared as shared

API_URL = "https://uat.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"

@tool
def leave_balance(x_user_context: str) -> dict:
    """
    Fetch leave balance using employeeId & loginId from X-User-Context header.
    Header must be a valid JSON string.
    """
    try:
        auth_data = json.loads(x_user_context)   # ✅ direct JSON (no "data" wrapper)
    except json.JSONDecodeError:
        return {"error": "❌ Invalid X-User-Context header JSON"}

    # Extract fields
    token = auth_data.get("token")
    token_prefix = auth_data.get("tokenPrefix", "")
    employee_id = auth_data.get("employeeId")
    login_id = auth_data.get("id")
    username =  auth_data.get("userName")

    if not token or not login_id:
        return {"error": "❌ Missing token or loginId in header JSON"}
        
    # Save token globally (optional)
    shared.AUTH_TOKEN_PROD = token

    # Build headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"{token_prefix}{token}",
        "content-type": "application/json",
        "referer": "https://uat.fuzionhr.com/",
        "x-device-id": "a997ca51-52ef-4b96-9b3c-5ff29c4b79f5",
        "x-fcm-token": "null"
    }

    # Build body
    payload = {
        "loginId": login_id,
        "employeeId": employee_id
    }

    # Call API
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"UserName:{username}")
            return response.json()
        else:
            return {"error": f"Failed with {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": f"❌ API call failed: {e}"}
