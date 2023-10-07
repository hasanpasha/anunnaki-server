from anunnaki_server.ext_manager.repo import Repo
from anunnaki_server.model import Extension
import pytest


@pytest.fixture
def repo() -> Repo:
    return Repo()

@pytest.fixture
def extension() -> Extension:
    return Extension(
        id=40113167690652825,
        pkg='shabakaty_cinemana',
        name='cinemana',
        version='0.0.1',
        lang='en',
        base_url='https://cinemana.shabakaty.com'
    )

def test_pkg_name(repo: Repo, extension: Extension):
    assert repo.unique_version_name(extension) == "en_shabakaty_cinemana_v0.0.1"
    assert repo.unique_version_name(extension) != "en_shabakaty_cinemana_v0.0.2"

def test_zip_file(repo: Repo, extension: Extension):
    assert repo.zip_file(extension) == "en_shabakaty_cinemana_v0.0.1.zip"
    assert repo.zip_file(extension) != "en_shabakatycinemana_v0.0.1.zip"

def test_icon_file(repo: Repo, extension: Extension):
    assert repo.icon_file(extension) == "en_shabakaty_cinemana_v0.0.1.png"
    assert repo.icon_file(extension) != "en_shabakatycinemana_v0.0.1.png"