from src.chaozzDBPy import ChaozzDBPy

db = ChaozzDBPy()

sql = "INSERT INTO test (name, age, grade) VALUES ('Jarbas','35','5')"

db.run(sql)
