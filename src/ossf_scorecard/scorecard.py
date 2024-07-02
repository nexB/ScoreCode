import requests


def get_scorecard(platform, org, repo):
    url = f"https://api.securityscorecards.dev/projects/{platform}/{org}/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def print_scorecard(platform, org, repo):
    try:
        data = get_scorecard(platform, org, repo)
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenSSF Scorecard API: {e}")

#
# if __name__ == '__main__':
#     print_scorecard("github.com", "nexB", "scancode-toolkit")