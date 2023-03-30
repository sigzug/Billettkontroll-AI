from collections import deque
import pandas as pd
from datetime import timedelta


data = {"Linje": ["re10", "r12"], 
          "Vogn": [2, 7],
          "Fra": ["eidsvoll", "eidsvoll"], 
          "Til": ["oslo_s", "nationaltheateret"], 
         "Fullt?": ["ja", "nei"],
         "Sjekket?": ["ja", "ja"],
         "Merknad": ["penis pikk", "sjekket etter lillestrøm"],
         "Dag": [1, 10],
         "Måned": [3, 3],
         "Time": [6, 8],
         "Minutt": [52, 1]}

class LineMap:
    re10_south = [{"name": "eidsvoll", "timedelta": 0}, {"name": "oslo_lufthavn", "timedelta": 11}, {"name": "lillestrøm", "timedelta": 13},
                  {"name": "oslo_s", "timedelta": 13}, {"name": "nationaltheateret", "timedelta": 2}]
    
    re10_north = [{"name": "nationaltheateret", "timedelta": 0}, {"name": "oslo_s", "timedelta": 6}, 
                  {"name": "lillestrøm", "timedelta": 11}, {"name": "oslo_lufthavn", "timedelta": 14}, {"name": "eidsvoll", "timedelta": 9}]
    
    re11_south = [{"name": "eidsvoll", "timedelta": 0}, {"name": "eidsvoll_verk", "timedelta": 5}, {"name": "oslo_lufthavn", "timedelta": 7}, 
                  {"name": "lillestrøm", "timedelta": 13}, {"name": "oslo_s", "timedelta": 13}, {"name": "nationaltheateret", "timedelta": 2}]
    
    re11_north = [{"name": "nationaltheateret", "timedelta": 0}, {"name": "oslo_s", "timedelta": 6}, {"name": "lillestrøm", "timedelta": 11}, 
                  {"name": "oslo_lufthavn", "timedelta": 14}, {"name": "eidsvoll_verk", "timedelta": 6}, {"name": "eidsvoll", "timedelta": 4}]
    
    r12_south = deque(["eidsvoll", "eidsvoll_verk", "oslo_lufthavn", "lillestrøm", "oslo_s", "nationaltheateret"])
    r12_north = reversed(r12_south)
    
    r14_south = deque(["kongsvinger", "skarnes", "årnes", "haga", "auli", "rånåsfoss", "blaker", "sørumsand", "svingen", "fetsund", "nerdrum", "lillestrøm", "oslo_s", "nationaltheateret"])
    r14_north = reversed(r14_south)


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
    
        
# new_data = recursive_line_creator(data, r12_line_south, 3, r12_line_south.index(data["Fra"][0]), r12_line_south.index(data["Til"][0]))
# db = pd.DataFrame(new_data)
# db = db.drop_duplicates()
# db = db.reset_index()
# print(db)

def sjekket_etter(db: pd.DataFrame):
    lines = []
    for index, row in db.iterrows():
        lines.append(find_line(row))
        
    db["Sjekket etter"] = db.apply(lambda x: sjekket_etter_column(x, lines), axis=1)
    return db
        
       
def sjekket_etter_column(merknad: pd.Series, lines: list[deque]):
    line = lines[merknad._name]
    merknad = merknad["Merknad"]
    merknad = merknad.lower()
    words = merknad.split()
    word_seq1 = ["sjekket", "etter"]
    word_seq2 = ["sjekket", "med", "en", "gang"]
    
    checked = None
    for i in range(len(words) - len(word_seq1)):
        if words[i:i+len(word_seq1)] == word_seq1:
            checked = words[i + len(word_seq1)]
            if checked == "oslo":
                checked += f"_{words[i + len(word_seq1) + 1]}"
            
            for i in range(len(line) - 1):
                if line[i] == checked:
                    return i       
        if words[i:i+len(word_seq2)] == word_seq2:
            checked = line[0]
            return 0
    
    if checked == None:
        return -1
        
       
def find_line(row: pd.Series):
    line_map = LineMap()
    
    if isinstance(row["Linje"], list) and isinstance(row["Fra"], list) and isinstance(row["Til"], list):
        linje = row["Linje"][0]
        fra = row["Fra"][0]
        til = row["Til"][0]
    else:
        linje = row["Linje"]
        fra = row["Fra"]
        til = row["Til"]
    
    match linje:
        case "re10":
            south = line_map.re10_south
            north = line_map.re10_north
        case "re11":
            south = line_map.re11_south
            north = line_map.re11_north
        case "r12":
            south = line_map.r12_south
            north = line_map.r12_north
        case "r14":
            south = line_map.r14_south
            north = line_map.r14_north
        case _:
            return
                
                
    for i in range(len(south)):
        if south[i] == fra:
            fra_i = i
        if south[i] == til:
            til_i = i
            
    if fra_i < til_i:
        return south
    else:
        return north
    

       
def handle_recursion(db: pd.DataFrame) -> pd.DataFrame:
    db = sjekket_etter(db)
    db_dict = db.to_dict()
    
    # Find the maximum length of the value lists
    max_length = max(len(value_list) for value_list in db_dict.values())

    slices = []
    # Iterate through the indices and create new dictionaries for each index
    for i in range(max_length):
        sliced_dict = {key: [db_dict[key][i]] for key in db_dict if i < len(db_dict[key])}
        slices.append(sliced_dict)
        
    new_db = pd.DataFrame(db_dict)
   
    for slice in slices:
        checked = slice["Sjekket etter"][0]
        if checked != -1:
            line = find_line(slice)
            
            first = next(i for i in range(len(line)) if line[i] == slice["Fra"][0])
            last = next(i for i in range(len(line)) if line[i] == slice["Til"][0])
            
            new_dict = recursive_line_creator(slice, line, checked, first, last)
            temp_db = pd.DataFrame(new_dict)
            new_db = pd.concat([new_db, temp_db])
    
    new_db = new_db.drop_duplicates()
    new_db = new_db.reset_index()
    
    return new_db
    
    
    
db = pd.DataFrame(data)
print(db)

#db = db.apply(lambda x: handle_recursion(x, r12_line_south), axis=1)
db = handle_recursion(db)
print(f"\n{db}")

