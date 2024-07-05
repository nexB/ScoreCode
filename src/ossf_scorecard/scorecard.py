import requests


def GetScorecard(platform, org, repo):
    url = f"https://api.securityscorecards.dev/projects/{platform}/{org}/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_message = response.json().get('message', 'No error message provided')
        except ValueError:
            error_message = response.text or 'No error message provided'

        if response.status_code == 400:
            raise requests.exceptions.HTTPError(f"400 Bad Request: {error_message}")
        elif response.status_code == 401:
            raise requests.exceptions.HTTPError(f"401 Unauthorized: {error_message}")
        elif response.status_code == 403:
            raise requests.exceptions.HTTPError(f"403 Forbidden: {error_message}")
        elif response.status_code == 404:
            raise requests.exceptions.HTTPError(f"404 Not Found: {error_message}")
        elif response.status_code == 500:
            raise requests.exceptions.HTTPError(f"500 Internal Server Error: "
                                                f"{error_message}")
        else:
            response.raise_for_status()

#
# if __name__ == '__main__':
#     print_scorecard("github.com", "nexB", "scancode-toolkit")