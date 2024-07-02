import requests


def GetScorecard(platform, org, repo):
    url = f"https://api.securityscorecards.dev/projects/{platform}/{org}/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

#
# if __name__ == '__main__':
#     print_scorecard("github.com", "nexB", "scancode-toolkit")