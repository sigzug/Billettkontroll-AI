from collections import deque
import pandas as pd


data = {"Linje": "r12", 
          #"Vogn": [findCatCode(vognCat, vogn)],
          "Fra": "eidsvoll", 
          "Til": "oslo_s", 
         "Fullt?": "ja",
         "Merknad": "Sjekket med en gang",
         "Dag": 1,
         "Måned": 3,
         "Time": 6,
         "Minutt": 52}

db = pd.DataFrame(data)

r12_line_south = deque(["eidsvoll", "eidsvoll_verk", "oslo_lufthavn", "lillestrøm", "oslo_s", "nationaltheateret"])
r12_line_north = reversed(r12_line_south)

def line_creator(db: pd.DataFrame):
    db.apply(lambda x: recursive_line_creator(x, ))

def recursive_line_creator(db: pd.DataFrame, line_map: deque, first_stop, last_stop):
    if first_stop < last_stop:
        