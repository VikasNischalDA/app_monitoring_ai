import requests
from datetime import datetime, timedelta
from domain.models import ErrorLog

class LogFetchAgent:

    def __init__(self, app_id: str, api_key: str):
        """
        app_id: Application Insights App ID (from portal Overview)
        api_key: API key with 'Read telemetry' permissions
        """
        self.app_id = app_id
        self.api_key = api_key
        self.endpoint = f"https://api.applicationinsights.io/v1/apps/{self.app_id}/query"

    def fetch_logs(self):
        # Query for exceptions in the last 1 hour
        query = """
        exceptions
| where timestamp > ago(30m)
| summarize 
    count(),
    arg_max(timestamp, outerType, details, cloud_RoleInstance, cloud_RoleName)
by outerMessage
| order by count_ desc
        """

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        body = {
            "query": query
        }

        response = requests.post(self.endpoint, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()

        logs = []
        # Application Insights API returns tables -> rows
        for table in data.get("tables", []):
            columns = [col["name"] for col in table["columns"]]
            for row in table["rows"]:
                row_dict = dict(zip(columns, row))
                logs.append(ErrorLog(
                    timestamp=row_dict.get("timestamp"),
                    exception_type=row_dict.get("outerType"),
                    message=row_dict.get("details"),
                    cloud_RoleInstance= row_dict.get("cloud_RoleInstance"),
                    cloud_RoleName= row_dict.get("cloud_RoleName")
                ))

        return logs