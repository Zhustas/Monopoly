import json, csv, pandas # for GetFields()
from pyllist import sllist 
from field import Field

# Fields format: Name of the field, description of the field, get paid (+) or pay the price (-)

#  0 -> file name is empty
# -1 -> file has a dot, but no format
# -2 -> file does not have a dot
# -3 -> wrong file format (acceptable: .csv, .json, .xls, .xlsx)
# -4 -> file does not exist
# -5 -> .json file is empty or the information in the file is invalid
# -6 -> .csv file is empty
# -7 -> .xls or .xlsx file is empty
# -8 -> given point value is not numeric
# -9 -> given point value is higher than 999 999 999

FILEFORMATS = [".csv", ".json", ".xls", ".xlsx"]

def get_fields(fileName: str):
    if fileName == "":
        return 0

    fileformat = ""
    lenfileformat = len(fileName) - 1
    dotgood = False
    while lenfileformat != -1:
        fileformat += fileName[lenfileformat]
        if fileName[lenfileformat] == '.':
            dotgood = True
            break
        lenfileformat -= 1
    if lenfileformat == len(fileName) - 1:
        return -1
    if not dotgood:
        return -2
    fileformat = fileformat[::-1]

    fileformat = fileformat.lower()

    fileformatgood = False
    for ff in FILEFORMATS:
        if fileformat == ff:
            fileformatgood = True
            break
    if not fileformatgood:
        return -3
    
    fields = sllist()

    if fileformat == ".json":
        try:
            openedFile = open(fileName)
        except FileNotFoundError:
            return -4
        filedatatxt = openedFile.read()
        data = json.loads(filedatatxt)

        values = list(data.values())
        
        if len(values) % 3 != 0 or len(values) == 0:
            return -5

        index = 0
        while index < len(values):
            title = values[index]
            desc = values[index + 1]
            try:
                points = int(values[index + 2])
            except ValueError:
                return -8
            if points > 999999999:
                return -9
            fields.append(Field(title, desc, points))
            index += 3

        return fields
    
    if fileformat == ".csv":
        try:
            openedFile = open(fileName)
        except FileNotFoundError:
            return -4
        filedata = csv.reader(openedFile)

        went_through_loop = 0
        for row in filedata:
            try:
                points_value = int(row[2])
            except ValueError:
                return -8
            if points_value > 999999999:
                return -9
            fields.append(Field(row[0], row[1], points_value))
            went_through_loop += 1
        
        if went_through_loop == 0:
            return -6

        return fields
    
    if fileformat == ".xls" or fileformat == ".xlsx":
        try:
            openedFile = pandas.read_excel(fileName)
        except FileNotFoundError:
            return -4
    
        index = 0
        while index < openedFile.shape[0]:
            listas = list(openedFile.loc[index])
            try:
                points_value = int(listas[2])
            except ValueError:
                return -8
            if points_value > 999999999:
                return -9
            fields.append(Field(listas[0], listas[1], points_value))
            index += 1
        
        if index == 0:
            return -7

        return fields

def add_field(listas, title: str, desc: str, points: int, index: int):
    if listas.size == 0:
        listas.append(Field(title, desc, points))
        return listas

    if index == 0:
        listas.appendleft(Field(title, desc, points))
    elif index == listas.size:
        listas.appendright(Field(title, desc, points))
    else:
        node = listas.nodeat(index)
        listas.insert(Field(title, desc, points), before=node)
    
    return listas

def delete_field(listas, what_to_delete: str, index = False):
    if index:
        ind = int(what_to_delete)
        if ind == 0:
            listas.popleft()
        elif ind == listas.size:
            listas.popright()
        else:
            node = listas.nodeat(ind)
            listas.remove(node)
        
        return listas

    if not index:
        i = 0
        while listas.nodeat(i).next != None:
            node = listas.nodeat(i)
            if node.value.title == what_to_delete:
                listas.remove(node)
                i -= 1
            i += 1
        node = listas.nodeat(i)
        if node.value.title == what_to_delete:
            listas.remove(node)
        
        return listas

def find_error(listas, what: str, what_to_delete = "", del_index = False, listas_good = 0, title = "", description = "", points = 0, index = 0,
               how_many = "", points_to_win = ""):
    if what == "file":
        if type(listas) == sllist:
            print("Fields loaded")
            return 1

        if listas == 0:
            print("Error: file name is empty")
            return 0
        
        if listas == -1:
            print("Error: file does not have a format")
            return 0
        
        if listas == -2:
            print("Error: file does not have a dot")
            return 0
        
        if listas == -3:
            print("Error: wrong file format (acceptable formats: .csv, .json, .xls, .xlsx)")
            return 0
        
        if listas == -4:
            print("Error: file does not exist")
            return 0
        
        if listas == -5:
            print("Error: .json file is empty or the information in the file is invalid")
            return 0
        
        if listas == -6:
            print("Error: .csv file is empty")
            return 0
        
        if listas == -7:
            print("Error: .xls or .xlsx file is empty")
            return 0
        
        if listas == -8:
            print("Error: given point value is not numeric")
            return 0

        if listas == -9:
            print("Error: given point value is higher than 999 999 999")
            return 0
    
    if what == "add":
        if len(title) == 0:
            print("Error: title can not be empty")
            return 0
        
        if description == "":
            print("Error: description can not be empty")
            return 0

        if index > listas.size:
            print("Error: index is out of bounds")
            return 0
        
        print("Field added")
        return 1

    if what == "delete":
        if listas_good == 0:
            print("Error: there are no fields to delete")
            return 0
        
        if len(what_to_delete) == 0:
            print("Error: no information given")
            return 0

        if del_index:
            if what_to_delete.isnumeric() != True:
                print("Error: given information is not numeric or is negative")
                return 0
            
            if int(what_to_delete) > listas.size:
                print("Error: index is out of bounds")
                return 0
            
            print("Field deleted")
            return 1
        
        if not del_index:
            found = False
            for i in range(len(listas)):
                if listas[i].title == what_to_delete:
                    found = True
                    break
            if not found:
                print("Error: field with this title does not exist")
                return 0
            
            print("Field deleted")
            return 1
    
    if what == "delete all":
        if listas_good == 0:
            print("Error: there are no fields to delete")
            return 0
        
        print("All fields deleted")
        return 1
    
    if what == "game":
        if listas_good < 3 or listas_good > 12:
            print("Error: fields count is less than 3 or bigger than 12")
            return 0
        
        if how_many == "":
            print("Error: players size was not set")
            return 0

        if points_to_win == "":
            print("Error: 'points to win' was not set")
            return 0
        
        if points_to_win == "0":
            print("Error: 'points to win' has to be higher than 0")
            return 0

        return 1
