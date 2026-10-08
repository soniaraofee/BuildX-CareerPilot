from auth import (
    init_db,
    register_user,
    login_user,
)


init_db()

username = "test_user"
password = "123456"


registered = register_user(
    username,
    password,
)

print("Registered:", registered)


logged_in = login_user(
    username,
    password,
)

print("Logged in:", logged_in)