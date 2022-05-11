from app.models.user import User

TEST_EMAIL = "test@example.com"


def test_create_user_uncommitted():
    user = User(email=TEST_EMAIL, username="test", password="test")

    assert user.id is None
    assert user.email == TEST_EMAIL
    assert user.username == "test"
    assert user.password == "test"


def test_create_user_committed(app, db):
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
