import pytest

from src.utils.bcrypt_hash import bcrypt, verify_bcrypt


def test_bcrypt_success():
    password = "testpassword"
    password_hash = bcrypt(password)

    assert password != password_hash
    # has is different every time
    assert bcrypt(password) != password_hash
    assert verify_bcrypt(password, password_hash)


def test_bcrypt_success_empty_password():
    password = ""
    password_hash = bcrypt(password)
    assert verify_bcrypt(password, password_hash)


def test_bcrypt_success_match_failed():
    password = "correctpassword"
    password_hash = bcrypt(password)
    incorrect_password = "incorrectpassword"

    assert not verify_bcrypt(incorrect_password, password_hash)
    assert verify_bcrypt(password, password_hash)


def test_bcrypt_success_none_password():
    password = None
    with pytest.raises(TypeError):
        bcrypt(password)
