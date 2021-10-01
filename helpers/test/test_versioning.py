import logging
import os

import helpers.git as hgit
import helpers.unit_test as huntes
import helpers.versioning as hversion

_LOG = logging.getLogger(__name__)


class TestVersioning1(huntes.TestCase):
    def test_get_code_version1(self) -> None:
        git_root = hgit.get_client_root(super_module=False)
        file_name = os.path.join(git_root, "version.txt")
        code_version = hversion.get_code_version(file_name)
        _LOG.debug("code_version=%s", code_version)

    def test_get_code_version2(self) -> None:
        code_version = hversion.get_code_version()
        _LOG.debug("code_version=%s", code_version)

    def test_get_container_version1(self) -> None:
        container_version = hversion._get_container_version()
        _LOG.debug("container_version=%s", container_version)

    def test_check_version1(self) -> None:
        git_root = hgit.get_client_root(super_module=False)
        file_name = os.path.join(git_root, "version.txt")
        hversion.check_version(file_name)

    def test__check_version1(self) -> None:
        code_version = "amp-1.0.0"
        container_version = "amp-1.0.2"
        is_ok = hversion._check_version(code_version, container_version)
        self.assertFalse(is_ok)

    def test__check_version2(self) -> None:
        code_version = "amp-1.0.0"
        container_version = "amp-1.0.0"
        is_ok = hversion._check_version(code_version, container_version)
        self.assertTrue(is_ok)
