from sql_parser import sql_parser
from chaozzDBPy import ChaozzDBPy


# INSERT
sql = 'INSERT into users (nome, idade, sexo) values ("fulano", "21", "M"), ("ciclana", "22", "F"), ("beltrano", "23", "M"), ("siclana", "24", "F"), ("beltrano", "25", "M"), ("siclana", "26", "F")'
# sql = 'INSERT into users (nome, idade, sexo) values ("fulano", "21", "M")'

# SELECT
# sql = 'SELECT * FROM users'
# sql = 'SELECT (id, name) FROM users WHERE id = 1'

# UPDATE
# sql = 'UPDATE users SET name = "fulano" WHERE id = 1'

# DELETE
# sql = 'DELETE FROM users WHERE id = 1'

parsed_sql = sql_parser(sql)

query = ChaozzDBPy()
res = query.run(parsed_sql)

print(res)
