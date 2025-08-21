import requests
from langchain_core.tools import tool
import agents.shared as shared   # ✅ import module, not variable
AUTH_TOKEN="PZN eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJUQjEwMDEiLCJ0b2tlblZlcnNpb24iOjEzLCJpZCI6NDMyLCJ1c2VyVHlwZSI6ImlzRW1wbG95ZWUiLCJlbXBsb3llZUlkIjo0MjUsImNvbXBhbnlJZCI6NSwiaWF0IjoxNzU1NzcxMjI4fQ.Om2q-vZ5CZVF2TXTRyF0yR-KVm3xvmiFwFGfWUqZT6hzOltWern31o_-13RNLLunybZsF4KVES2Luz4Y6y4oeQ"
API_URL = "https://uat.fuzionhr.com/api/v1/hrms/leaveApplication/getMyLeaveBalance"

@tool
def check_leave_balance(login_id: int, emp_id: int) -> dict:
    """Fetch leave balance for a given employee."""

    if not shared.AUTH_TOKEN_PROD:   # ✅ access from module
        print('❌ not getting auth token')
        return {"error": "❌ No Authorization token provided"}

    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": shared.AUTH_TOKEN_PROD,
        "content-type": "application/json",
        "referer": "https://uat.fuzionhr.com/",
        "x-device-id": "c9c9d16a-e255-48c1-ba27-287f556c83f9",
        "x-fcm-token": "null",
    }
    
    payload = {"loginId": login_id, "employeeId": emp_id}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": f"❌ API call failed: {e}"}
