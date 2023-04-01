from tests.fixtures import *
from conf_test_db import override_db_session
from database.models import DbUsers
from database.hash import Hash


def pytest_sessionstart():
    sess = next(override_db_session())
    sess.add(DbUsers(id=1,
                     login="admin",
                     password=Hash().bcrypt_pass("admin"),
                     )
             )
    sess.commit()
