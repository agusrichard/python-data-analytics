import pytest
from app.models.user import User

TEST_EMAIL = "test@example.com"


def test_create_user_uncommitted():
    user = User(email=TEST_EMAIL, username="test", password="test")

    assert user.id is None
    assert user.email == TEST_EMAIL
    assert user.username == "test"
    assert user.password == "test"


def test_create_user_committed(db):
    data = {"email": TEST_EMAIL, "username": "test", "password": "test"}
    user = User.from_dict(data)

    db.session.add(user)
    db.session.commit()

    user: User = User.query.filter_by(email=TEST_EMAIL).first()

    assert user.id is not None
    assert user.email == TEST_EMAIL
    assert user.username == "test"
    assert user.check_password("test")
    assert user.password != "test"
    assert user.bio is None
    assert user.fullname is None
    assert user.last_login is None
    assert user.created_at is not None
    assert user.updated_at is not None

    assert str(user) == f"User('{user.username}', '{user.email}')"

    user_dict = user.to_dict()
    assert user_dict["id"] == user.id
    assert user_dict["username"] == user.username
    assert user_dict["email"] == user.email
    assert user_dict["fullname"] == user.fullname
    assert user_dict["bio"] == user.bio
    assert user_dict["last_login"] == None
    assert user_dict["created_at"] == user.created_at.isoformat()
    assert user_dict["updated_at"] == user.updated_at.isoformat()


def test_user_generate_token(db):
    data = {"email": TEST_EMAIL, "username": "test", "password": "test"}
    user = User.from_dict(data)

    db.session.add(user)
    db.session.commit()

    user: User = User.query.filter_by(email=TEST_EMAIL).first()
    assert user.generate_token() is not None


def test_create_user_without_password():
    data = {"email": TEST_EMAIL, "username": "test"}
    with pytest.raises(ValueError) as e:
        User.from_dict(data)

    assert str(e.value) == "Password is required"
