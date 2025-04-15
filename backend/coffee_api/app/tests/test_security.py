from app.security import Hasher
import pytest

def test_verify_password_success():
    password = "password123"
    wrong_password = "password321"
    hashed_password = Hasher.get_password_hash(password)
    assert Hasher.verify_password(password, hashed_password) == True

def test_verify_password_failure():
    password = "password123"
    wrong_password = "password321"
    hashed_password = Hasher.get_password_hash(password)
    assert Hasher.verify_password(wrong_password, hashed_password) == False