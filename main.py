#imports
import json
import PySimpleGUI as sg
import sys


def importjson(FilePath = None):
    if type(FilePath) == None:
        #ask user for input on file location ignored if filepath is passed when calling
        path = input("What is the path to the json?")
    else:
        #If filepath is passed by GUI it skips user input
        path = FilePath
    
    #loading w/ basic error tracking so it doenst just crash randomly
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
    if len(data["grades"]) == 0:
        raise Exception("Grades list is empty, please try again")

    print("json succesfully loaded!")
    return data
    
def exportjson(ngrades,fpath,data):
    #setup things
    data["grades"] = [] #empties the grades section to prepare to fill it
    #ngrades = ngrades.sort() #FOR SOME REASON JUST EMPTIES THE LIST??!

    for x in ngrades:
        #creates dictionary used to store grades and appends it to now empty grades list
        tmpdict = {"name": x[0],"grade": x[1],"weight": x[2]}
        data["grades"].append(tmpdict)

    try:
        with open(fpath, 'w') as json_out:
            json.dump(data,json_out,indent=4)
        print(f"saved at {fpath}")
    except:
        pass #usually caused by user clicking out of Save-as dialog box which passes an empty value as filepath
        # print("Error writing. Either some actual error or you clicked out of the Save-as dialog")

    
def lettergrade(NumberGrade):
    #really hate how this is done but i'm too tired to think of a better way
    #returns Letter grade from float input
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

def WAvgcalc(grades):
    #calculates weighted avergage & letter grade
    returngrade = [0,""]
    denom = 0
    for x in grades:
        returngrade[0] += x[1] * x[2]
        denom += x[2]

    returngrade[0] = round(returngrade[0]/denom,2)
    returngrade[1] = lettergrade(returngrade[0])
    return returngrade

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
            window.close()
            return values[0]
    

def tableValGen(data):
    #the Table GUI element requires a list, this function converts the dictionary input into the nested lists it understands
    returnlist = []
    for i in range(0,len(data["grades"])):
        #values() function does not work here for some reason :(
        #takes the key values from the dictionary and appends them to nested list for the table constructer
        templist = [data["grades"][i]["name"],data["grades"][i]["grade"],data["grades"][i]["weight"]]
        returnlist.append(templist)
    return returnlist    

def gradeGUI(data,finalgrade):
    #I cannot add a checkbox to the table easily so instead double click and edit a grade
    sg.theme('DarkPurple')
    extraGrades = []
    gradesval = tableValGen(data)
    #gradesval.append(extraGrades)
    
    layout = [
        [
            sg.Text(text = data["type"] + " " +data["name"],  font = ("any",20,"bold")) #f strings don't work here so I did it the trad way
        ],
        [
            sg.Table(values = gradesval,
            headings = [
                "Name",
                "Grade",
                "Weight"
            ],
            num_rows = 10,
            alternating_row_color="#0C0A3C",
            #enable_events= True,
            bind_return_key=True,
            key="TableDClick",
            vertical_scroll_only = True)
        ],
        [
            sg.Button(button_text = "Add New Grade", auto_size_button=True,key = "AddGrade"),
            sg.FileSaveAs(button_text = "Save Json", auto_size_button=True,key= "SaveJson",target = "SaveAs", default_extension = ".json") #starts save-as dialog. default extension doesnt work
        ],
        [
            sg.Text(text = f"{finalgrade[0]}%", key="numberGrade"),
            sg.VerticalSeparator(pad=(1,1)),
            sg.VerticalSeparator(pad=(1,1)),
            sg.Text(text = finalgrade[1], key="letterGrade")
        ],
        [
            #Put hidden stuff here for saving
            #make SaveAs dialog point here.
            #events enabled to allow for one-button save-as. When this is filled in by the SaveAs button it triggers an event
            sg.Input(enable_events = True, key = "SaveAs", focus = False, visible = False, disabled = True)
        ]
    ]
    window = sg.Window('Grade Calculator', layout)         

    while True:               
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == "AddGrade":
            print("AddGrade")
            b = gradepopupGUI()
            if b != None:
                gradesval.append(b)
                window["TableDClick"].Update(values = gradesval) #updates table.
                valupdate = WAvgcalc(gradesval)
                window["numberGrade"].Update(value= f"{valupdate[0]}%")
                window["letterGrade"].Update(value = f"{valupdate[1]}")
        if event == "TableDClick":
            print("UpdateGrade")

            b = gradepopupGUI(gradesval[values["TableDClick"][0]],mod = True)
            if b != None:
                gradesval[values["TableDClick"][0]] = b #uses to event values to find the list index, probably the wrong way to do this
                window["TableDClick"].Update(values = gradesval) #updates table.
                valupdate = WAvgcalc(gradesval)
                window["numberGrade"].Update(value= f"{valupdate[0]}%")
                window["letterGrade"].Update(value = f"{valupdate[1]}")
        if event =="SaveAs":
            exportjson(gradesval,values["SaveAs"],data) #passes the updated grades and save-path



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
    
    try:
       filepath = filepathGUI()
       data = importjson(filepath)
    except:
        print("File Picking cancelled, exiting")
        sys.exit()
    # data = importjson("ExampleGrades/grades.json") #bypasses the file picker GUI, for testing only
    
    finalgrade = [0,""]

    print(type(data["grades"]))

    denom = 0
    for x in data["grades"]:
        #loops through grade list and creates weighted average

       denom += x["weight"]
       wg = (x["grade"]) * (x["weight"])
       finalgrade[0] += wg 
    finalgrade[0] = round(finalgrade[0]/denom,2)
    
    finalgrade[0] = round(finalgrade[0],2)

    finalgrade[1] = lettergrade(finalgrade[0])

    gradeGUI(data,finalgrade)

    
    #f-strings sure are funky
   #print(f'Final Grade: \n {data["type"]} {data["name"]}: \n {finalgrade[0]}% ::: {finalgrade[1]}')


if __name__ == main():
    main()

