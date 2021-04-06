#imports
import json
import PySimpleGUI as sg
import sys
#import sys

def importjson(FilePath = None):
    if type(FilePath) == None:
        #ask user for input on file location
        path = input("What is the path to the json?")
    else:
        path = FilePath
        #take arguments when run
    
    #loading
    try: 
        with open(path) as file:
            data = json.load(file)
    except:
        raise Exception("An error occured while loading json, check filepath")
    #formatting check
    try:
        #test a random operation on the first grade to check if present
        float(data["grades"][0]["grade"]) 
    except:
        raise Exception("Could not acess grades, try again")
    if len(data["grades"]) <= 0:
        raise Exception("Grades list is empty, please try again")

    print("json succesfully loaded!")
    return data
    
def lettergrade(NumberGrade):
    #really hate how this is done but i'm too tired to think of a better way
    if NumberGrade >= 93:
        LetterReturn = "A"
    elif NumberGrade >= 90:
        LetterReturn = "A-"
    elif NumberGrade >= 87:
        LetterReturn = "B+"
    elif NumberGrade >= 83:
        LetterReturn = "B"
    elif NumberGrade >= 80:
        LetterReturn = "B-"
    elif NumberGrade >= 77:
        LetterReturn = "C+"
    elif NumberGrade >= 73:
        LetterReturn = "C"
    elif NumberGrade >= 70:
        LetterReturn = "C-"
    elif NumberGrade >= 67:
        LetterReturn = "D+"
    elif NumberGrade >= 60:
        LetterReturn = "D"
    else:
        LetterReturn = "F"
    return LetterReturn

def filepathGUI():
    #adds a gui ontop of the code
    sg.theme('DarkPurple')
    #file loading gui
    layout = [
        [sg.Text("No .json file loaded!!!")],
        [sg.Text("Filename")],
        [sg.Input(), sg.FileBrowse()],
        [sg.OK(),sg.Cancel()]
    ]

    window = sg.Window('Grade Calculator', layout)

    event, values = window.read()
    if event in (sg.WIN_CLOSED,'cancel'):
        window.close()
        sys.exit()
    if event in (sg.WIN_CLOSED, 'OK'):
            return values[0]
    
def tableValGen(data):
    returnlist = []
    for i in range(0,len(data["grades"])):
        #values() function does not work here for some reason :(
        #takes the key values from the dictionary and appends them to nested list for the table constructer
        templist = [data["grades"][i]["name"],data["grades"][i]["grade"],data["grades"][i]["weight"],sg.Checkbox(text = "Drop")]
        returnlist.append(templist)
    return returnlist    

def gradeGUI(data,finalgrade):
    #I cannot add a checkbox to the table easily so instead there is a input box to remove a specifc number
    sg.theme('DarkPurple')
    extraGrades = []
    gradesval = tableValGen(data)
    #gradesval.append(extraGrades)

    layout = [[sg.Table(values = gradesval,
        headings = ["Name", "Grade", "Weight"],
        num_rows = 10,
        alternating_row_color="#0C0A3C",
        #enable_events= True,
        bind_return_key=True,
        key="TableDClick",
        vertical_scroll_only = True)],
        [sg.Button(button_text = "Add New Grade", auto_size_button=True,key = "AddGrade")],
        [sg.Text(f"{finalgrade[0]}%"),sg.VerticalSeparator(pad=(1,1)),sg.VerticalSeparator(pad=(1,1)),sg.Text(finalgrade[1])]]

    window = sg.Window('Grade Calculator', layout)         
    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == "AddGrade":
            print("piss")
            gradepopupGUI()
        if event == "TableDClick":
            print(values)
            #Modify Grade function
            b = gradepopupGUI(gradesval[values["TableDClick"][0]]) #uses to event values to find the list index, probably the wrong way to do this
            #str(5)
            gradesval[values["TableDClick"][0]] = b
            window.refresh()
            
    # event, values = window.read()



def gradepopupGUI(curDat = ["Name","Score","Weight"],mod = False):
    #mod param is a bit redundant but, im too lazy to add a check to make it useless
    #curDat specified what data is shown in the text-box by default. defaults to info
    sg.theme('DarkPurple')

    #changes the prompt text depending if new grade is being added or if grade is being updated.
    if mod == True:
        flavtext = "Update Grade"
    else:
        flavtext = "Add New Grade"
    layout = [
        [sg.Text(text = f"{flavtext}:",font = ("any",20,"bold"))],
        [sg.Input(default_text=curDat[0],justification="left",tooltip = "Name of Assigment",size = (20,1)),
        sg.Input(default_text=curDat[1],justification="left",tooltip = "% Score of Assigment", size = (7,1)),
        sg.Input(default_text=curDat[2],justification="left",tooltip = "weight of assigment, between 0 & 1", size = (7,1))],
        [sg.OK(),sg.Cancel()]
    ]
    
    window = sg.Window(flavtext, layout)  
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            break
        if event in (sg.WIN_CLOSED, 'OK'):
            if (values[1] == "Score") or (values[2] == "Weight"):
                #to make sure **someone** doesnt not change anything and brick it
                window.close()
                break

            print(values)
            neovalues = [values[0],float(values[1]),float(values[2])] #for some reason the values is a dictionary instead of a list
            window.close()
            print(neovalues)
            return neovalues
            


def main():
    
    # try:
    #     data = importjson(filepathGUI())

    # except:
    #     print("File Picking cancelled, exiting")
    #     sys.exit()
    data = importjson("ExampleGrades/grades.json") #bypasses the file picker GUI, for testing only
    
    finalgrade = [0,""]

    print(type(data["grades"]))

    for x in data["grades"]:
        #loops through grade list and creates weighted average
       wg = round(x["grade"] * x["weight"],3)
       finalgrade[0] += wg 
    finalgrade[0] = round(finalgrade[0],2)

    finalgrade[1] = lettergrade(finalgrade[0])

    gradeGUI(data,finalgrade)

    
    #f-strings sure are funky
    print(f'Final Grade: \n {data["type"]} {data["name"]}: \n {finalgrade[0]}% ::: {finalgrade[1]}')










if __name__ == main():
    main()
    print("Wtf")

