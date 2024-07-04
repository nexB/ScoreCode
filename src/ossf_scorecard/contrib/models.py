import attr

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
