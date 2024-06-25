
def fetch_documentation_url(url: str):
    """
    Given a fully qualified documentation URL with check slugs
    this will function will remove the slugs and return the original URL


    Args:
        url (str): Documentation URL
        E.g., https://github.com/ossf/scorecard/blob/5d5c2ab2a88adac0a18464f0216b/docs/checks.md#pinned-dependencies

    Returns:

        url (str): Documentation URL without the check slugs
        E.g., https://github.com/ossf/scorecard/blob/5d5c2ab2a88adac0a18464f0216b/docs/checks.md

    """

    try:
        if url:
            return url.split("#")[0]

    except ValueError:
        return None


    