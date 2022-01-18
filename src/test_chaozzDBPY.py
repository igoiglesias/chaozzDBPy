from chaozzDBPy import ChaozzDBPy


## should hash password
def test_should_generate_password_with_salt():
    db = ChaozzDBPy(salt="dfsfds!@sdD2")
    password = db.password("eu")
    assert password == "148de90e751abf0f573ca7b699ce32857d1b444a"


def test_should_generate_password_without_salt():
    db = ChaozzDBPy()
    password = db.password("eu")
    assert password == "34635194919f21c1859b36f31790616084d1e90b"


def test_should_return_false_to_not_allowed_query_action():
    db = ChaozzDBPy()
    query_action = "TEST"
    error = ""
    result = db.error(query_action, error)
    assert result is False


def test_should_return_empty_array_to_select_query_action():
    db = ChaozzDBPy()
    query_action = "SELECT"
    error = ""
    result = db.error(query_action, error)
    assert result == []


def test_should_return_zero_to_insert_query_action():
    db = ChaozzDBPy()
    query_action = "INSERT"
    error = ""
    result = db.error(query_action, error)
    assert result is 0


def test_should_return_false_to_delete_and_update_query_action():
    db = ChaozzDBPy()
    query_action = "DELETE"
    error = ""
    result = db.error(query_action, error)
    assert result is False

    query_action = "UPDATE"
    error = ""
    result = db.error(query_action, error)
    assert result is False


def test_should_insert_item():
    db = ChaozzDBPy()
    insert_1 = db.query(
        "INSERT INTO user (nome, senha, email) VALUES ('igor','1234','igor@igor.com')"
    )
    assert not insert_1
    insert_2 = db.query(
        "INSERT INTO user (nome, senha, email) VALUES ('joão','4321','joao@fernando.com')"
    )
    assert not insert_2
