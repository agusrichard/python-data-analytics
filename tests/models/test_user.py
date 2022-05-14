import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User

TEST_EMAIL = "test@test.com"


def create_user(db, num: int = 0):
    uname_pass = f"test{num}"
    email = f"test{num}@test.com"
    if num == 0:
        uname_pass = "test"
        email = TEST_EMAIL
    user = User(email=email, username=uname_pass)
    user.set_password(uname_pass)

    db.session.add(user)
    db.session.commit()

    return user


def test_positive_create_user_uncommitted():
    user = User(email=TEST_EMAIL, username="test")

    assert user.id is None
    assert user.email == TEST_EMAIL
    assert user.username == "test"


def test_negative_create_user_set_plain_password():
    with pytest.raises(ValueError) as e:
        User(email=TEST_EMAIL, username="test", password="test")

    assert str(e.value) == "Can't set plain password, use set_password instead"


def test_negative_create_user_try_read_password():
    user = User(email=TEST_EMAIL, username="test")

    with pytest.raises(AttributeError) as e:
        user.password

    assert str(e.value) == "Password is not a readable attribute"


def test_positive_create_user_committed(db):
    create_user(db)

    user: User = User.query.filter_by(email=TEST_EMAIL).first()

    assert user.id is not None
    assert user.email == TEST_EMAIL
    assert user.username == "test"
    assert user.check_password("test")
    assert user.bio is None
    assert user.fullname is None
    assert user.last_login is None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.avatar is None


def test_positive_create_user_from_dict(db):
    user = User.from_dict({"email": TEST_EMAIL, "username": "test", "password": "test"})

    db.session.add(user)
    db.session.commit()

    user: User = User.query.filter_by(email=TEST_EMAIL).first()

    assert user.id is not None
    assert user.email == TEST_EMAIL
    assert user.username == "test"
    assert user.check_password("test")
    assert user.bio is None
    assert user.fullname is None
    assert user.last_login is None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.avatar is None


def test_positive_create_user_to_dict(db):
    create_user(db)

    user: User = User.query.filter_by(email=TEST_EMAIL).first()

    assert str(user) == f"User('{user.username}', '{user.email}')"

    user_dict = user.to_dict()
    assert user_dict["id"] == user.id
    assert user_dict["username"] == user.username
    assert user_dict["email"] == user.email
    assert user_dict["fullname"] == user.fullname
    assert user_dict["bio"] == user.bio
    assert user_dict["avatar"] == user.avatar
    assert user_dict["last_login"] == None
    assert user_dict["created_at"] == user.created_at.isoformat()
    assert user_dict["updated_at"] == user.updated_at.isoformat()


def test_positive_user_generate_token(db):
    user = create_user(db)

    db.session.add(user)
    db.session.commit()

    user: User = User.query.filter_by(email=TEST_EMAIL).first()
    assert user.generate_token() is not None


def test_negative_create_user_without_password(db):
    with pytest.raises(IntegrityError) as e:
        user = User(email=TEST_EMAIL, username="test")
        db.session.add(user)
        db.session.commit()


def test_negative_create_user_without_password_from_dict():
    data = {"email": TEST_EMAIL, "username": "test"}
    with pytest.raises(ValueError) as e:
        User.from_dict(data)

    assert str(e.value) == "Password is required"


def test_positive_user_follow(db):
    user = create_user(db)
    user1 = create_user(db, 1)

    user.follow(user1)


def test_positive_user_unfollow(db):
    user = create_user(db)
    user1 = create_user(db, 1)

    user.follow(user1)

    assert user.is_following(user1)

    user.unfollow(user1)

    assert not user.is_following(user1)


def test_positive_user_is_not_following(db):
    user = create_user(db)
    user1 = create_user(db, 1)

    db.session.add(user)
    db.session.add(user1)
    db.session.commit()

    assert not user.is_following(user1)


def test_positive_user_is_following(db):
    user = create_user(db)
    user1 = create_user(db, 1)

    db.session.add(user)
    db.session.add(user1)
    db.session.commit()

    user.follow(user1)
    user1.follow(user)

    assert user.is_following(user1)
    assert user1.is_following(user)


def test_positive_user_get_followers(db):
    user = create_user(db)
    user1 = create_user(db, 1)
    user2 = create_user(db, 2)

    db.session.add(user)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    user.follow(user1)
    user.follow(user2)

    user1.follow(user)
    user1.follow(user2)

    user2.follow(user)
    user2.follow(user1)

    assert user.get_followers() == [user1, user2]
    assert user1.get_followers() == [user, user2]
    assert user2.get_followers() == [user, user1]


def test_positive_user_get_followed(db):
    user = create_user(db)
    user1 = create_user(db, 1)
    user2 = create_user(db, 2)

    db.session.add(user)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    user.follow(user1)
    user.follow(user2)

    user1.follow(user)
    user1.follow(user2)

    user2.follow(user)
    user2.follow(user1)

    db.session.commit()

    assert user.get_followed() == [user1, user2]
    assert user1.get_followed() == [user, user2]
    assert user2.get_followed() == [user, user1]
