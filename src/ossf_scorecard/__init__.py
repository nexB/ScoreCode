#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import environ

from pathlib import Path

SCORECARD_API_URL = None

try:
    from django.conf import settings
    # Only SCORECARD_URL can be provided through setting
    SCORECARD_API_URL = None
    SCORECARD_URL = settings.SCORECARD_URL
    if SCORECARD_URL:
        SCORECARD_API_URL = f'{SCORECARD_URL.rstrip("/")}/projects/'

except ImportError:

    PROJECT_DIR = environ.Path(__file__) - 1
    ROOT_DIR = PROJECT_DIR - 1

    ENV_FILE = "/etc/scorecode/.env"
    if not Path(ENV_FILE).exists():
        ENV_FILE = ROOT_DIR(".env")

    env = environ.Env()
    environ.Env.read_env(ENV_FILE)

    SCORECARD_URL = env.str("SCORECARD_URL", default="")

    if SCORECARD_URL:
        SCORECARD_API_URL = SCORECARD_URL.rstrip("/") + "/projects"

        if not SCORECARD_API_URL.startswith("https://"):
            SCORECARD_API_URL = "https://" + SCORECARD_API_URL