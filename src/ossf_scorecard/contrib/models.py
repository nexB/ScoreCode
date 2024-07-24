import attr
from commoncode.datautils import Date
from commoncode.datautils import List
from commoncode.datautils import String

from ossf_scorecard.contrib.utils import FetchDocumentationUrl


class ModelMixin:
    """
    Base mixin for all package models.
    """

    def to_dict(self, **kwargs):
        """
        Return a mapping of primitive Python types.
        """
        return attr.asdict(self)

    def to_tuple(self, **kwargs):
        """
        Return a hashable tuple of primitive Python types.
        """
        return to_tuple(self.to_dict(**kwargs))

    @classmethod
    def from_dict(cls, mapping):
        """
        Return an object built from ``kwargs`` mapping. Always ignore unknown
        attributes provided in ``kwargs`` that do not exist as declared attributes
        in the ``cls`` class.
        """
        known_attr = attr.fields_dict(cls)
        kwargs = {k: v for k, v in mapping.items() if k in known_attr}
        return cls(**kwargs)


def to_tuple(collection):
    """
    Return a tuple of basic Python values by recursively converting a mapping
    and all its sub-mappings.
    For example::
    >>> to_tuple({7: [1,2,3], 9: {1: [2,6,8]}})
    ((7, (1, 2, 3)), (9, ((1, (2, 6, 8)),)))
    """
    if isinstance(collection, dict):
        collection = tuple(collection.items())
    assert isinstance(collection, (tuple, list))
    results = []
    for item in collection:
        if isinstance(item, (list, tuple, dict)):
            results.append(to_tuple(item))
        else:
            results.append(item)
    return tuple(results)


@attr.attributes(slots=True)
class ScorecardChecksMixin(ModelMixin):

    check_name = String(
        repr=True,
        label="check name",
        help="Defines the name of check corresponding to the OSSF score"
        "For example: Code-Review or CII-Best-Practices"
        "These are the some of the checks which are performed on a scanned "
        "package",
    )

    check_score = String(
        repr=True,
        label="check score",
        help="Defines the score of the check for the package scanned"
        "For Eg : 9 is a score given for Code-Review",
    )

    reason = String(
        repr=True,
        label="reason",
        help="Gives a reason why a score was given for a specific check"
        "For eg, : Found 9/10 approved changesets -- score normalized to 9",
    )

    details = List(
        repr=True, label="score details", help="A list of details/errors regarding the score"
    )

    @classmethod
    def from_data(cls, check_data):
        """
        Return a list of check objects for a package.
        """
        data = []

        for check in check_data:

            final_data = {
                "check_name": check.get("name"),
                "check_score": str(check.get("score")),
                "details": check.get("details", None),
            }

            scorecard_data = cls(**final_data)

            data.append(scorecard_data)

        return data


@attr.attributes(slots=True)
class PackageScoreMixin(ModelMixin):
    """
    Abstract class for storing OSSF scorecard data related to packages.
    This base class is used for all package-like objects, whether they are manifests
    or actual package instances.
    """

    scoring_tool = String(
        repr=True,
        label="scoring tool",
        help="Defines the source of a score or any other scoring metrics"
        "For example: ossf-scorecard for scorecard data",
    )

    scoring_tool_version = String(
        repr=True,
        label="scoring tool version",
        help="Defines the version of the scoring tool used for scanning the package",
    )

    score = String(repr=True, label="score", help="Score of the package which is scanned")

    scoring_tool_documentation_url = String(
        repr=True, label="scoring documentation url", help="Version of the package as a string."
    )

    score_date = Date(repr=True, label="score date", help="score date")

    checks = List(item_type=ScorecardChecksMixin, label="checks", help="List of all checks used")

    @classmethod
    def from_data(cls, scorecard_data):
        """
        Return PackageScore object created out of the package metadata
        present in `scorecard_data` mapping.
        """
        final_data = {
            "score": str(scorecard_data.get("score")),
            "scoring_tool_version": scorecard_data.get("scorecard").get("version"),
            "scoring_tool_documentation_url": FetchDocumentationUrl(
                scorecard_data.get("checks")[0].get("documentation").get("url")
            ),
            "scoring_tool": "OSSF",
            "score_date": scorecard_data.get("date", None),
            "checks": ScorecardChecksMixin.from_data(scorecard_data.get("checks", [])),
        }

        scorecard_data = cls(**final_data)

        return scorecard_data
