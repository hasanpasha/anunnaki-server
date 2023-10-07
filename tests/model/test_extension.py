from anunnaki_server.model import Extension
import pytest


@pytest.fixture
def ext1() -> Extension:
    return Extension(
        id=40113167690652825,
        pkg='shabakaty_cinemana',
        name='cinemana',
        version='0.0.1',
        lang='en',
        base_url='https://cinemana.shabakaty.com'
    )


@pytest.fixture
def ext2() -> Extension:
    return Extension(
        id=40113167690652825,
        pkg='shabakaty_cinemana',
        name='cinemana',
        version='0.0.1',
        lang='en',
        base_url='https://cinemana.shabakaty.com'
    )


def test_equals(ext1: Extension, ext2: Extension):
    assert ext1 == ext2


def test_not_equal(ext1: Extension, ext2: Extension):
    ext2.id += 1
    assert ext1 != ext2


def test_version_equals(ext1: Extension, ext2: Extension):
    assert ext1.is_same_version(ext2)


def test_version_not_equal(ext1: Extension, ext2: Extension):
    ext1.version = '0.0.2'
    assert not ext1.is_same_version(ext2)


def test_version_major_older(ext1: Extension, ext2: Extension):
    ext2.version = '2.0.1'
    assert ext1 < ext2


def test_version_major_not_older(ext1: Extension, ext2: Extension):
    ext1.version = '1.0.1'
    ext2.version = '0.0.3'
    assert ext1 > ext2


def test_version_minor_older(ext1: Extension, ext2: Extension):
    ext2.version = '0.1.1'
    ext1.version = '0.0.1'
    assert ext1 < ext2


def test_version_minor_not_older(ext1: Extension, ext2: Extension):
    ext2.version = '0.1.9'
    ext1.version = '0.2.1'
    assert ext1 > ext2


def test_version_patch_older(ext1: Extension, ext2: Extension):
    ext2.version = '0.1.9'
    ext1.version = '0.1.1'
    assert ext1 < ext2


def test_version_patch_not_older(ext1: Extension, ext2: Extension):
    ext1.version = '1.0.8'
    ext2.version = '1.0.3'
    assert ext1 > ext2