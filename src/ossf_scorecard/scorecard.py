import requests
from contrib.models import PackageScoreMixin
import logging
from collections import namedtuple
from urllib.parse import urlparse
import requests
from ossf_scorecard import SCORECARD_API_URL

session = requests.Session()

def GetScorecard(platform, org, repo):

    url = f"{SCORECARD_API_URL}/{platform}/{org}/{repo}"
    response = requests.get(url)

    if response.status_code == 200:
        score_data = response.json()
        return PackageScoreMixin.from_data(score_data)
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



def is_configured():
    """Return True if the required Scorecard settings have been set."""
    if SCORECARD_API_URL:
        return True
    return False


def is_available():
    """Return True if the configured Scorecard server is available."""
    if not is_configured():
        return False

    try:
        response = session.head(SCORECARD_API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as request_exception:
        # logger.debug(f"{label} is_available() error: {request_exception}")
        return False

    return response.status_code == requests.codes.ok


def fetch_scorecard_info(packages, logger):
    """
    Extract platform, org, and repo from a given GitHub or GitLab URL.

    Args
    ----
        url (str): The URL to parse.

    Returns
    -------
        RepoData: Named tuple containing 'platform', 'org', and 'repo' if the URL is
        valid, else None.

    """
    for package in packages:
        url = package.vcs_url
        repo_data = extract_repo_info(url)

        if repo_data:

            scorecard_data = GetScorecard(
                platform=repo_data.platform, org=repo_data.org, repo=repo_data.repo
            )

            logger.info(f"Fetching scorecard data for package: {scorecard_data}")


def extract_repo_info(url):
    """
    Extract platform, org, and repo from a given GitHub or GitLab URL.

    Args:
        url (str): The URL to parse.

    Returns
    -------
        RepoData: Named tuple containing 'platform', 'org', and 'repo' if the URL is
        valid, else None.

    """
    RepoData = namedtuple("RepoData", ["platform", "org", "repo"])

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        return None

    if "github.com" in hostname:
        platform = "github"
    elif "gitlab.com" in hostname:
        platform = "gitlab"
    else:
        return None

    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) < 2:
        return None

    org = path_parts[0]
    repo = path_parts[1]

    return RepoData(platform=platform, org=org, repo=repo)

if __name__ == '__main__':
    if is_configured():
        data = GetScorecard("github.com", "nexB", "scancode-toolkit")
        print(data)
