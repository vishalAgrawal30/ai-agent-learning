import requests
from langchain_core.tools import tool

AUTH_TOKEN = "PZN eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJUQjEwMDEiLCJ0b2tlblZlcnNpb24iOjEzLCJpZCI6NDMyLCJ1c2VyVHlwZSI6ImlzRW1wbG95ZWUiLCJlbXBsb3llZUlkIjo0MjUsImNvbXBhbnlJZCI6NSwiaWF0IjoxNzU1NTk0NTU4fQ.OztB8sjlvY66oOo_tw5-gX_voes1PLvuUCy9Sn-IeznQoEIsBg9PFxQw7ahxvi7xaWKst5C71yhNiVividZwWQ"
API_URL = "https://uat.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"

@tool
def check_leave_balance(
    login_id: int , emp_id: int) -> dict:
    """Fetch leave balance for a given employee.
    Only use this tool if the user asks about leave balances."""


    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": AUTH_TOKEN,
        "content-type": "application/json",
        "referer": "https://uat.fuzionhr.com/",
        "x-device-id": "a3c8e562-8642-42f7-ba3e-68c787e0c605",
        "x-fcm-token": "null",
    }

    payload = {
        "loginId": login_id,
        "employeeId": emp_id
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with {response.status_code}", "details": response.text}
    except Exception as e:
        return f"❌ API call failed: {e}"

