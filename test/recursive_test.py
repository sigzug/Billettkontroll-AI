from training.utils.recursive_utils import *


def extractDay(dt):
    return dt.day


def extractMonth(dt):
    return dt.month


def extractYear(dt):
    return dt.year


def extractHour(x):
    return x.hour


def extractMinute(x):
    return x.minute


def strCleaner(x: str):
    if isinstance(x, str):
        x = x.lower()
        x = x.replace(" ", "_")
        x = x.strip("_")

        if "ja" in x:
            return "ja"

        return x
    else:
        return -1


def convert_linje_to_new(linje_inn):
    match linje_inn:
        case 'l14':
            return 'r14'
        case 'l12':
            return 'r12'
        case 'r11':
            return 're11'
        case 'r10':
            return 're10'
    return linje_inn


# data = {"Linje": ["r12", "r14"],
#           "Vogn": [2, 7],
#           "Fra": ["eidsvoll", "skarnes"],
#           "Til": ["oslo_s", "oslo_s"],
#          "Fullt?": ["ja", "nei"],
#          "Sjekket?": ["nei", "ja"],
#          "Merknad": [-1, "Sjekket akkurat på Lillestrøm"],
#          "Dag": [30, 30],
#          "Måned": [3, 3],
#          "Time": [15, 19],
#          "Minutt": [52, 54]}
#
# db = pd.DataFrame(data)

db_main = pd.read_excel("/Users/sigurdskyrud/OneDrive/Dokumenter/Andre Dokumenter/Billettkontroll data/Billettkontroll data.xlsx")
db_aanerud = pd.read_excel(
    "/Users/sigurdskyrud/OneDrive/Dokumenter/Andre Dokumenter/Billettkontroll data/Billettkontroll data-aanerud.xlsx")
db = pd.concat([db_main, db_aanerud])
db = db.apply(lambda col: col.apply(lambda x: strCleaner(x) if isinstance(x, str) else x) if col.name != "Merknad" else col)

db["Time"] = db["Klokke"].apply(lambda x: extractHour(x))
db["Minutt"] = db["Klokke"].apply(lambda x: extractMinute(x))
db = db.drop("Klokke", axis=1)

db["Dag"] = db["Dato"].apply(lambda x: extractDay(x))
db["Måned"] = db["Dato"].apply(lambda x: extractMonth(x))
# db["År"] = db["Dato"].apply(lambda x: extractYear(x)) # Not relevant for the timescale I have
db = db.drop("Dato", axis=1)

db["Linje"] = db["Linje"].apply(lambda x: convert_linje_to_new(x))

db = handle_recursion(db)
print(f"\n{db.to_string()}")
db.to_excel("/Users/sigurdskyrud/Desktop/pd_data.xlsx", index=False)

