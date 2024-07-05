import attr

from commoncode.datautils import Date
from commoncode.datautils import String
from commoncode.datautils import List

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
class PackageScoreMixin(ModelMixin):
    """
    Abstract class for storing OSSF scorecard data related to packages.
    This base class is used for all package-like objects, whether they are manifests
    or actual package instances.
    """
    scoring_tool = String(
        repr=True,
        label='scoring tool',
        help='Defines the source of a score or any other scoring metrics'
             'For example: ossf-scorecard for scorecard data')

    scoring_tool_version = String(
        repr=True,
        label='scoring tool version',
        help='Defines the version of the scoring tool used for scanning the package')

    score = String(
        repr=True,
        label='score',
        help='Score of the package which is scanned')

    scoring_tool_documentation_url = String(
        repr=True,
        label='scoring documentation url',
        help='Version of the package as a string.')

    score_date = Date(
        repr=True,
        label='score date',
        help='score date')


    @classmethod
    def from_data(cls, scorecard_data):
        """
        Return PackageData object created out of the package metadata
        present in `scorecard_data` mapping. Also populate license and
        copyright holder fields by computing them from extracted license
        statement and extracted copyright.

        Skip the license/copyright detection step if `package_only` is True.
        """
        if "purl" in scorecard_data:
            scorecard_data.pop("purl")

        scorecard_data = cls(**scorecard_data)

        if not package_only:
            scorecard_data.populate_license_fields()
            scorecard_data.populate_holder_field()
        else:
            scorecard_data.normalize_extracted_license_statement()

        return scorecard_data


@attr.attributes(slots=True)
class ScorecardChecksMixin(ModelMixin):

    for_package = List(
        item_type=PackageScoreMixin,
        label = 'scoring tool',
        help = 'Defines the source of a score or any other scoring metrics'
           'For example: ossf-scorecard for scorecard data'
    )

    check_name = String(
        repr=True,
        label='scoring tool',
        help='Defines the source of a score or any other scoring metrics'
             'For example: ossf-scorecard for scorecard data')

    check_score = String(
        repr=True,
        label='scoring tool version',
        help='Defines the version of the scoring tool used for scanning the package')

    reason = String(
        repr=True,
        label='score',
        help='Score of the package which is scanned')

    details = String(
        repr=True,
        label='scoring documentation url',
        help='Version of the package as a string.')

    score_date = Date(
        repr=True,
        label='score date',
        help='score date')

