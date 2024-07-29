=============================
Scorecard
=============================

ScoreCode is a tool for assessing the security and compliance of software projects. It
evaluates various aspects of a project's security posture and generates a scorecard to help organizations understand the security risks associated with the software.

**Features:**
- Automated security assessment
- Comprehensive scoring based on multiple criteria
- Easy integration with existing workflows
- Supports various platforms and repositories

Installation
------------

To install Scorecard, you can use pip:

.. code-block:: bash

    pip install scorecard

Usage
-----

To use Scorecard, you need to call the `GetScorecard` function with the appropriate parameters. Below is a basic usage example:

.. code-block:: python

    from scorecard import GetScorecard

    # Define platform, organization, and repository
    platform = "github.com"
    org = "nexB"
    repo = "scancode-toolkit"

    # Fetch the scorecard
    data = GetScorecard(platform="github.com", org="nexB", repo="scancode-toolkit")

    # Print the results
    print("Scoring Tool:", data.scoring_tool)
    print("Scoring Tool Version:", data.scoring_tool_version)
    print("Score Date:", data.score_date)
    print("Score:", data.score)
    print("Documentation URL:", data.scoring_tool_documentation_url)


Testing
-------

To run the tests, use pytest. Ensure that all dependencies are installed and then execute:

.. code-block:: bash

    pytest tests
