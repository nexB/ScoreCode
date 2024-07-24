#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import pytest

from ossf_scorecard.scorecard import GetScorecard

# Define a list of test cases with different platforms, organizations, and repositories
test_cases = [
    ("github.com", "nexB", "scancode-toolkit"),
    ("github.com", "tensorflow", "tensorflow"),
    ("github.com", "apache", "spark"),
    ("gitlab.com", "gitlab-org", "gitlab"),
]


@pytest.mark.parametrize("platform, org, repo", test_cases)
def test_get_scorecard(platform, org, repo):
    data = GetScorecard(platform, org, repo)

    # Check that the data object contains the expected fields
    assert hasattr(data, "scoring_tool")
    assert hasattr(data, "scoring_tool_version")
    assert hasattr(data, "score_date")
    assert hasattr(data, "score")
    assert hasattr(data, "scoring_tool_documentation_url")
    assert hasattr(data, "checks")

    # Validate the types of the fields
    assert isinstance(data.scoring_tool, str)
    assert isinstance(data.scoring_tool_version, str)
    assert isinstance(data.score_date, str)
    assert isinstance(data.score, str)
    assert isinstance(data.scoring_tool_documentation_url, str)
    assert isinstance(data.checks, list)

    # Check that the URL is valid and has the expected structure
    assert data.scoring_tool_documentation_url.startswith("https://github.com/")
    assert "docs/checks.md" in data.scoring_tool_documentation_url
