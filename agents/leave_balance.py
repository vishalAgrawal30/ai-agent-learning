import json
import requests
from langchain_core.tools import tool
import agents.shared as shared

API_URL = "https://uat.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"

@tool
def leave_balance(authorization: str) -> dict:
    """
    Fetch leave balance using loginId and empId from the authorization JSON.
    The API requires them in the request body (LeaveBalanceRequestDto).
    """
    try:
        # Parse the authorization JSON (passed as string)
        auth_data = json.loads(authorization)
    except json.JSONDecodeError:
        return {"chatbot": "❌ Invalid Authorization header JSON", "leave_balance": {}}

    # Extract required values from authorization JSON
    auth_token = auth_data.get("authToken")
    device_id = auth_data.get("deviceId")
    fcm_token = auth_data.get("fcmToken")
    emp_id = auth_data.get("empId")
    login_id = auth_data.get("loginId")

    if not all([login_id, emp_id, auth_token]):
        return {"error": "❌ Missing loginId, empId, or authToken in header JSON"}

    # Save token globally (optional for reuse)
    shared.AUTH_TOKEN_PROD = auth_token

    # Build headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": auth_token,   # only token here
        "content-type": "application/json",
        "referer": "https://uat.fuzionhr.com/",
        "x-device-id": device_id,
        "x-fcm-token": fcm_token,
    }

    # Build body using empId & loginId from authorization JSON
    payload = {"loginId": login_id, "employeeId": emp_id}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": f"❌ API call failed: {e}"}
