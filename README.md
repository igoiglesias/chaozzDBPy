# ChaozzDBPy

## About

   ![image](https://user-images.githubusercontent.com/2658126/94922899-60754800-0491-11eb-8763-573a408fd630.png) [![Testing](https://github.com/igoiglesias/chaozzDBPy/actions/workflows/python-app-testing.yml/badge.svg?branch=master)](https://github.com/igoiglesias/chaozzDBPy/actions/workflows/python-app-testing.yml)
    
   ChaozzDBPy is a python implementation based on the original <a target="_blank" href="https://github.com/chaozznl/chaozzDB">ChaozzDB</a> from <a target="_blank" href="https://github.com/chaozznl">Chaozznl</a> with some new features.

   The main propouse here is to implement a noSQL DB with a simplified SQL syntax.
#### It is still in the first steps, feel free to contribute!

## Setup

   ### Create the virtualenv
     
        virtualenv -p 3.8 venv && source venv/bin/activate
     
   ### Install requirements
        
        pip install -r requirements.txt

## Use

   
    from chaozzDBPy import ChaozzDBPy

    db = ChaozzDBPy()
    insert = db.query(
        "INSERT INTO user (name, password, email) VALUES ('Jane','1234','jane@doh.com')"
    )
