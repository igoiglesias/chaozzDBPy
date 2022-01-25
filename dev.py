from src.chaozzDBPy import ChaozzDBPy

db = ChaozzDBPy()

# sql = "INSERT INTO test (name, age, grade) VALUES ('Jarbas','35','5')"
sql = "INSERT INTO test (name, age, grade) VALUES ('Fulda','35','5'), ('Jarbas','35','5'), ('Fulano','35','5'), ('Ciclano','35','5'), ('Beltrano','35','5')"

db.run(sql)
