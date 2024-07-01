# -*- coding: utf-8 -*-
#
# Copyright (c) nexB
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Visit https://github.com/nexB/ScoreCode for support and
# download.

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class PackageScoreMixin(models.Model):
    """
    Abstract Model for saving OSSF scorecard data.
    """

    scoring_tool = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Defines the source of a score or any other scoring metrics"
            "For example: ossf-scorecard for scorecard data"
        ),
    )

    scoring_tool_version = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Defines the version of the scoring tool used for scanning the"
            "package"
            "For Eg : 4.6 current version of OSSF - scorecard"
        ),
    )

    score = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Score of the package which is scanned"),
    )

    scoring_tool_documentation_url = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Documentation URL of the scoring tool used"),
    )

    score_date = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        help_text=_(
            "Date when the scoring was calculated on the package"
        ),
    )

    class Meta:
        abstract = True


class ScorecardChecksMixin(models.Model):

    check_name = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Defines the name of check corresponding to the OSSF score"
            "For example: Code-Review or CII-Best-Practices"
            "These are the some of the checks which are performed on a scanned package"
        ),
    )

    check_score = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Defines the score of the check for the package scanned"
            "For Eg : 9 is a score given for Code-Review"
        ),
    )

    reason = models.CharField(
        max_length=300,
        blank=True,
        help_text=_("Gives a reason why a score was given for a specific check"
                    "For eg, : Found 9/10 approved changesets -- score normalized to 9"),
    )

    details = models.JSONField(
        default=list,
        blank=True,
        help_text=_(
            "A list of details/errors reharding the score"
        ),
    )

    class Meta:
        abstract = True




