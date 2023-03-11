from collections import deque
import pandas as pd


data = {"Linje": ["r12"], 
          "Vogn": [2],
          "Fra": ["eidsvoll"], 
          "Til": ["oslo_s"], 
         "Fullt?": ["ja"],
         "Sjekket?": ["ja"],
         "Merknad": ["sjekket med en gang"],
         "Dag": [1],
         "Måned": [3],
         "Time": [6],
         "Minutt": [52]}


r12_line_south = deque(["eidsvoll", "eidsvoll_verk", "oslo_lufthavn", "lillestrøm", "oslo_s", "nationaltheateret"])
r12_line_north = reversed(r12_line_south)


def line_creator(db: pd.DataFrame):
    pass
    

def recursive_line_creator(data: dict, line: deque, checked_stop: int, first_stop: int, last_stop: int) -> dict:
    if first_stop == last_stop:
        return data
    
    if first_stop <= checked_stop and last_stop > checked_stop:
        for key, value in data.items():
            if key == "Sjekket?":
                value.append("ja")
            elif key == "Fra":
                value.append(line[first_stop])
            elif key == "Til":
                value.append(line[last_stop])
            else:
                value.append(value[0])
    elif first_stop <= checked_stop and last_stop <= checked_stop:
        for key, value in data.items():
            if key == "Fra":
                value.append(line[first_stop])
            elif key == "Til":
                value.append(line[last_stop])
            elif key == "Sjekket?":
                value.append("nei")
            else:
                value.append(value[0])
        
    data.update(recursive_line_creator(data, line, checked_stop, first_stop+1, last_stop))
    data.update(recursive_line_creator(data, line, checked_stop, first_stop, last_stop-1))
     
    return data
    
    
def find_checked_stop(data: dict) -> int:
    if "sjekket" in data["Merknad"]:
        
    
        
checked_stop = find_checked_stop(data)
new_data = recursive_line_creator(data, r12_line_south, checked_stop, r12_line_south.index(data["Fra"][0]), r12_line_south.index(data["Til"][0]))
db = pd.DataFrame(new_data)
db = db.drop_duplicates()
db = db.reset_index()
print(db)