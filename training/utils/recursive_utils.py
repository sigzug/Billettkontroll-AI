import pandas as pd


class LineMap:
    re10_south = [{"name": "lillehammer", "timedelta": 0}, {"name": "moelv", "timedelta": 26}, 
                  {"name": "brummundal", "timedelta": 16}, {"name": "hamar", "timedelta": 18}, 
                  {"name": "stange", "timedelta": 9}, {"name": "tangen", "timedelta": 13},
                  {"name": "eidsvoll", "timedelta": 23}, {"name": "oslo_lufthavn", "timedelta": 11}, 
                  {"name": "lillestrøm", "timedelta": 13}, {"name": "oslo_s", "timedelta": 13}, 
                  {"name": "nationaltheatret", "timedelta": 2}, {"name": "skøyen", "timedelta": 4},
                  {"name": "lysaker", "timedelta": 4}, {"name": "sandvika", "timedelta": 5}, 
                  {"name": "asker", "timedelta": 6}, {"name": "brakerøya", "timedelta": 9}]

    re10_north = [{"name": "brakerøya", "timedelta": 0}, {"name": "asker", "timedelta": 10},
                  {"name": "sandvika", "timedelta": 6}, {"name": "lysaker", "timedelta": 6},
                  {"name": "skøyen", "timedelta": 3}, {"name": "nationaltheatret", "timedelta": 4}, 
                  {"name": "oslo_s", "timedelta": 6}, {"name": "lillestrøm", "timedelta": 11}, 
                  {"name": "oslo_lufthavn", "timedelta": 14}, {"name": "eidsvoll", "timedelta": 10},
                  {"name": "tangen", "timedelta": 20}, {"name": "stange", "timedelta": 9},
                  {"name": "hamar", "timedelta": 14}, {"name": "brummundal", "timedelta": 11},
                  {"name": "moelv", "timedelta": 12}, {"name": "lillehammer", "timedelta": 25}]

    re11_south = [{"name": "eidsvoll", "timedelta": 0}, {"name": "eidsvoll_verk", "timedelta": 5},
                  {"name": "oslo_lufthavn", "timedelta": 7}, {"name": "lillestrøm", "timedelta": 13},
                  {"name": "oslo_s", "timedelta": 13}, {"name": "nationaltheatret", "timedelta": 2},
                  {"name": "skøyen", "timedelta": 4}, {"name": "lysaker", "timedelta": 4},
                  {"name": "sandvika", "timedelta": 5}, {"name": "asker", "timedelta": 6},
                  {"name": "drammen", "timedelta": 14}, {"name": "sande", "timedelta": 12},
                  {"name": "holmestrand", "timedelta": 7}, {"name": "skoppum", "timedelta": 8},
                  {"name": "tønsberg", "timedelta": 11}, {"name": "stokke", "timedelta": 15},
                  {"name": "torp", "timedelta": 5}, {"name": "sandefjord", "timedelta": 6},
                  {"name": "larvik", "timedelta": 15}, {"name": "porsgrunn", "timedelta": 12},
                  {"name": "skien", "timedelta": 8}]

    re11_north = [{"name": "skien", "timedelta": 0}, {"name": "porsgrunn", "timedelta": 8},
                  {"name": "larvik", "timedelta": 15}, {"name": "sandefjord", "timedelta": 15},
                  {"name": "torp", "timedelta": 4}, {"name": "stokke", "timedelta": 5},
                  {"name": "tønsberg", "timedelta": 12}, {"name": "skoppum", "timedelta": 10},
                  {"name": "holmestrand", "timedelta": 8}, {"name": "sande", "timedelta": 6},
                  {"name": "drammen", "timedelta": 15}, {"name": "asker", "timedelta": 12},
                  {"name": "sandvika", "timedelta": 6}, {"name": "lysaker", "timedelta": 6},
                  {"name": "skøyen", "timedelta": 3}, {"name": "nationaltheatret", "timedelta": 0}, 
                  {"name": "oslo_s", "timedelta": 6}, {"name": "lillestrøm", "timedelta": 11}, 
                  {"name": "oslo_lufthavn", "timedelta": 14}, {"name": "eidsvoll_verk", "timedelta": 6}, 
                  {"name": "eidsvoll", "timedelta": 4}]

    r12_south = [{"name": "eidsvoll", "timedelta": 0}, {"name": "eidsvoll_verk", "timedelta": 5},
                 {"name": "oslo_lufthavn", "timedelta": 7}, {"name": "lillestrøm", "timedelta": 13},
                 {"name": "oslo_s", "timedelta": 13}, {"name": "nationaltheatret", "timedelta": 2}]

    r12_north = [{"name": "nationaltheatret", "timedelta": 0}, {"name": "oslo_s", "timedelta": 6},
                 {"name": "lillestrøm", "timedelta": 11}, {"name": "oslo_lufthavn", "timedelta": 14},
                 {"name": "eidsvoll_verk", "timedelta": 6}, {"name": "eidsvoll", "timedelta": 4}]

    r14_south = [{"name": "kongsvinger", "timedelta": 0}, {"name": "skarnes", "timedelta": 13},
                 {"name": "årnes", "timedelta": 14}, {"name": "haga", "timedelta": 7}, {"name": "auli", "timedelta": 3},
                 {"name": "rånåsfoss", "timedelta": 2}, {"name": "blaker", "timedelta": 3},
                 {"name": "sørumsand", "timedelta": 8}, {"name": "svingen", "timedelta": 5},
                 {"name": "fetsund", "timedelta": 2}, {"name": "nerdrum", "timedelta": 2},
                 {"name": "lillestrøm", "timedelta": 8}, {"name": "oslo_s", "timedelta": 13},
                 {"name": "nationaltheatret", "timedelta": 2}]

    r14_north = [{"name": "nationaltheatret", "timedelta": 0}, {"name": "oslo_s", "timedelta": 6},
                 {"name": "lillestrøm", "timedelta": 11}, {"name": "nerdrum", "timedelta": 5},
                 {"name": "fetsund", "timedelta": 2}, {"name": "svingen", "timedelta": 2},
                 {"name": "sørumsand", "timedelta": 6}, {"name": "blaker", "timedelta": 4},
                 {"name": "rånåsfoss", "timedelta": 3}, {"name": "auli", "timedelta": 3},
                 {"name": "haga", "timedelta": 2}, {"name": "årnes", "timedelta": 7},
                 {"name": "skarnes", "timedelta": 19}, {"name": "kongsvinger", "timedelta": 14}]


def recursive_line_creator(data: dict, line: list[dict], checked_stop: int, first_stop: int, last_stop: int) -> dict:
    """Recursive function that creates a line from a given stop to another given stop."""
    if first_stop == last_stop:
        return data

    if first_stop <= checked_stop < last_stop:
        for key, value in data.items():
            if key == "Sjekket?":
                value.append("ja")
            elif key == "Fra":
                value.append(line[first_stop]["name"])
            elif key == "Til":
                value.append(line[last_stop]["name"])
            else:
                value.append(value[0])
    elif first_stop <= checked_stop and last_stop <= checked_stop:
        for key, value in data.items():
            if key == "Fra":
                value.append(line[first_stop]["name"])
            elif key == "Til":
                value.append(line[last_stop]["name"])
            elif key == "Sjekket?":
                value.append("nei")
            else:
                value.append(value[0])

    data.update(recursive_line_creator(data, line, checked_stop, first_stop + 1, last_stop))
    data.update(recursive_line_creator(data, line, checked_stop, first_stop, last_stop - 1))

    return data


def sjekket_etter(db: pd.DataFrame):
    lines = []
    for index, row in db.iterrows():
        lines.append(find_line(row))

    db["Sjekket etter"] = db.apply(lambda x: sjekket_etter_column(x, lines), axis=1)
    return db


def sjekket_etter_column(series: pd.Series, lines: list[dict]) -> int:
    def contains_subsequence(words: list[str], subseq: list[str]) -> bool:
        """Checks if the list 'words' contains the subsequence 'subseq' in order."""
        subseq_index = 0
        for word in words:
            if word == subseq[subseq_index]:
                subseq_index += 1
                if subseq_index == len(subseq):
                    return True
        return False

    merknad = series["Merknad"]
    merknad = str(merknad)
    if merknad is not "nan" or merknad is not None:
        merknad = merknad.lower()
        merknad = merknad.replace(".", "")

    line = lines[series._name]
    if line is None or merknad == -1 or not isinstance(merknad, str):
        return -1

    if series["Sjekket?"] == "nei":
        checked = series["Til"]
        return next((i for i, x in enumerate(line) if x["name"] == checked), -1)

    words = merknad.split()
    word_seq1 = ["sjekket", "etter"]
    word_seq2 = ["sjekket", "med", "en", "gang"]
    word_seq3 = ["sjekket", "før"]
    word_seq4 = ["sjekket", "på"]

    checked = None
    if contains_subsequence(words, word_seq1) or contains_subsequence(words, word_seq4):
        try:
            checked_index = words.index(word_seq1[-1]) + 1
        except:
            checked_index = words.index(word_seq4[-1]) + 1
        checked = words[checked_index]

        if checked == "oslo":
            checked += f"_{words[checked_index + 1]}"
        elif checked == "eidsvoll":
            if (len(words) > checked_index + 1) and (words[checked_index + 1] == "verk"):
                checked += "_verk"

        return next((i for i, x in enumerate(line) if x["name"] == checked), -1)
    if contains_subsequence(words, word_seq3):
        checked_index = words.index(word_seq3[-1]) + 1
        checked = words[checked_index]

        if checked == "oslo":
            checked += f"_{words[checked_index + 1]}"

        return next((i for i, x in enumerate(line) if x["name"] == checked), -1) - 1
    if contains_subsequence(words, word_seq2):
        checked = line[0]["name"]
        return 0

    if checked is None:
        return -1


def find_line(row: pd.Series | dict) -> list[dict] | None:
    """Finds the matching line from the LineMap class and returns the corresponding list of dicts."""
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
            return None

    fra_i = 0
    til_i = 0
    for i in range(len(south)):
        if south[i]["name"] == fra:
            fra_i = i
        if south[i]["name"] == til:
            til_i = i

    if fra_i < til_i:
        return south
    else:
        return north


def add_time(data: dict, line, start: int):
    """Adds the sum of timedeltas from the start station to the current station to the time and minutes columns."""
    # Get all the fra stations in this slice
    fras = data["Fra"]
    for i in range(len(fras)):
        if fras[i] != line[start]["name"]:
            fra_index = next(k for k, d in enumerate(line) if d['name'] == fras[i])
            total_timedelta = sum(line[j]["timedelta"] for j in range(start, fra_index + 1))

            # Add the timedelta to minutes and handle overflow to hours
            data["Minutt"][i] += total_timedelta
            overflow_hours, remaining_minutes = divmod(data["Minutt"][i], 60)
            data["Minutt"][i] = remaining_minutes
            data["Time"][i] += overflow_hours
    return data


def handle_recursion(db_in: pd.DataFrame) -> pd.DataFrame:
    """Handles the recursion of the line creator."""
    db = sjekket_etter(db_in)
    db = db.fillna(-1)
    db["Sjekket etter"] = db["Sjekket etter"].astype(int)
    db_dict = db.to_dict()

    # Find the maximum length of the value lists
    max_length = max(len(value_list) for value_list in db_dict.values())

    # Iterate through the indices and create new dictionaries for each index
    slices = []
    for i in range(max_length):
        sliced_dict = {key: [db_dict[key][i]] for key in db_dict if i < len(db_dict[key])}
        slices.append(sliced_dict)

    new_db = pd.DataFrame(db_dict)
    dfs_to_concat = [new_db]

    for slice in slices:
        checked = slice["Sjekket etter"][0]
        if checked != -1:
            line = find_line(slice)

            try:
                first = next(i for i in range(len(line)) if line[i]["name"] == slice["Fra"][0])
                last = next(i for i in range(len(line)) if line[i]["name"] == slice["Til"][0])
            except StopIteration:
                continue

            new_dict = recursive_line_creator(slice, line, checked, first, last)
            new_dict.update(add_time(new_dict, line, first))

            temp_db = pd.DataFrame(new_dict)
            dfs_to_concat.append(temp_db)

    new_db = pd.concat(dfs_to_concat, ignore_index=True)
    new_db = new_db.drop_duplicates()
    new_db = new_db.sort_values(by=["Måned", "Dag", "Time", "Minutt"])
    new_db = new_db.drop(columns=["Sjekket etter"])
    new_db = new_db.reset_index(drop=True)
    return new_db
