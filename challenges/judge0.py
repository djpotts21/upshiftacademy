"""Judge0 API client for submitting code and retrieving results."""
import time
import requests
from django.conf import settings
import os


JUDGE0_URL = f"https://{settings.JUDGE0_API_HOST}/submissions"


def submit_code_to_judge0(student_code, test_code):
    """Submits student code and test code to Judge0 API for execution."""
    full_code = f"{student_code}\n\n{test_code}"

    payload = {
        "language_id": 71,  # Python 3
        "source_code": full_code,
        "stdin": "",
    }

    headers = {
        "x-rapidapi-key": os.environ["JUDGE0_API_KEY"],
        "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
        "content-type": "application/json"
    }

    response = requests.post(JUDGE0_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["token"]


def get_submission_result(token):
    """Retrieves the result of a submission from Judge0 API."""
    headers = {
        "x-rapidapi-host": settings.JUDGE0_API_HOST,
        "x-rapidapi-key": settings.JUDGE0_API_KEY,
    }

    for _ in range(10):  # retry a few times
        res = requests.get(
            f"{JUDGE0_URL}/{token}?base64_encoded=false",
            headers=headers,
            timeout=30)
        res.raise_for_status()
        result = res.json()

        if result["status"]["id"] in [1, 2]:  # In queue or Processing
            time.sleep(1)
            continue

        return result

    return {"status": {
        "description": "Timeout"},
            "stdout": "", "stderr": "Execution timed out"}
