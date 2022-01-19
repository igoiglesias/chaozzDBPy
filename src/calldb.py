from chaozzDBPy import ChaozzDBPy

def select_row():
    db = ChaozzDBPy()
    db.set_personalized_location('/home/yagoc/Development/personal/chaozzDBPy/db/user.tsv')
    res = db.query("SELECT * FROM users")

    print(res)
    

select_row()
