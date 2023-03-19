from collections import deque
import pandas as pd


data = {"Linje": ["r12", "r12"], 
          "Vogn": [2, 7],
          "Fra": ["eidsvoll", "eidsvoll"], 
          "Til": ["oslo_s", "nationaltheateret"], 
         "Fullt?": ["ja", "nei"],
         "Sjekket?": ["ja", "ja"],
         "Merknad": ["sjekket etter oslo lufthavn", "sjekket med en gang"],
         "Dag": [1, 10],
         "Måned": [3, 3],
         "Time": [6, 8],
         "Minutt": [52, 1]}


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
    
        
# new_data = recursive_line_creator(data, r12_line_south, 3, r12_line_south.index(data["Fra"][0]), r12_line_south.index(data["Til"][0]))
# db = pd.DataFrame(new_data)
# db = db.drop_duplicates()
# db = db.reset_index()
# print(db)

def sjekket_etter(merknad: str, line: deque):
    merknad = merknad.lower()
    words = merknad.split()
    word_seq1 = ["sjekket", "etter"]
    word_seq2 = ["sjekket", "med", "en", "gang"]
    
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
       
       
def handle_recursion(db: pd.DataFrame, line: deque) -> pd.DataFrame:
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
        first = next(i for i in range(len(line)) if line[i] == slice["Fra"][0])
        last = next(i for i in range(len(line)) if line[i] == slice["Til"][0])
        
        new_dict = recursive_line_creator(slice, line, checked, first, last)
        temp_db = pd.DataFrame(new_dict)
        new_db = pd.concat([new_db, temp_db])
    
    new_db = new_db.drop_duplicates()
    new_db = new_db.reset_index()
    
    return new_db
    
    
    
db = pd.DataFrame(data)
db["Sjekket etter"] = db["Merknad"].apply(lambda x: sjekket_etter(x, r12_line_south))
print(db)

#db = db.apply(lambda x: handle_recursion(x, r12_line_south), axis=1)
db = handle_recursion(db, r12_line_south)
print(f"\n{db}")

