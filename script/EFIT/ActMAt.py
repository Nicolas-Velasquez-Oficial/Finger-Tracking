import json
import os
import pandas as pd

MILISTA_SURV = []
MILISTA_PROS_PERCEP = []
MILISTA_RISK_PERCEP = []
MILISTA_TEMP_PERCEP = []
MILISTA_PROSOCIAL = []
MILISTA_INTERTEMP = []
MILISTA_RISK = []

for i in range(1, 3):
    for j in range(1, 136):
        ruta = 'Toda\Data\G' + str(i) + 'S' + str(j) + "_"
        arr_strings = ["actMat" , "INTERTEMP_data" , "INTERTEMP_PERCEPT", "PROSOCIAL_data" , "PROSOCIAL_PERCEPT",
                       "RISK_data", "RISK_PERCEPT"]
               # arr_strings = ["actMat"]
        for x in arr_strings:
            print("Reading->>", ruta + x + ".json", end=" ")
            PATH = "%s/%s" % (os.getcwd(), ruta + x + ".json")
            PROPERTIES = {}
            found = True
            try:
                with open(PATH) as datafile:
                    PROPERTIES = json.load(datafile)
            except  (IOError, KeyError ) as ex:

                 found = False
            print("not found")
            if found == True:
              if x == "actMat":

                MILISTA_SURV.append([PROPERTIES["ID"], PROPERTIES["Carrera"], PROPERTIES["Semestre"],PROPERTIES["Edad"], PROPERTIES["Genero"],
                                PROPERTIES["Resp"][0], PROPERTIES["Resp"][1],
                               PROPERTIES["Resp"][2], PROPERTIES["Resp"][3], PROPERTIES["Resp"][4],
                                PROPERTIES["Resp"][5], PROPERTIES["Resp"][6], PROPERTIES["Resp"][7],
                                PROPERTIES["Resp"][8], PROPERTIES["Resp"][9], PROPERTIES["Resp"][10],
                                PROPERTIES["Resp"][11], PROPERTIES["Resp"][12], PROPERTIES["Resp"][13]])

              if x == "INTERTEMP_PERCEPT":

                MILISTA_TEMP_PERCEP.append([PROPERTIES["subjID"], PROPERTIES["ROL"], PROPERTIES["task"],PROPERTIES["percept"]])

              if x == "PROSOCIAL_PERCEPT":

                MILISTA_PROS_PERCEP.append([PROPERTIES["subjID"], PROPERTIES["ROL"], PROPERTIES["task"],PROPERTIES["percept"]])

              if x == "RISK_PERCEPT":

                MILISTA_RISK_PERCEP.append([PROPERTIES["subjID"], PROPERTIES["ROL"], PROPERTIES["task"],PROPERTIES["percept"]])
              if x == "INTERTEMP_data":
                for l in range(0, 9):
                    MILISTA_INTERTEMP.append([PROPERTIES[l]["start_time"],PROPERTIES[l]["click_time"],PROPERTIES[l]["finger_time"],
                               PROPERTIES[l]["fix_duration"],PROPERTIES[l]["trial"],PROPERTIES[l]["RT"],PROPERTIES[l]["MT"],PROPERTIES[l]["xSR"],
                               PROPERTIES[l]["ySR"],PROPERTIES[l]["xT1"],PROPERTIES[l]["xT2"],PROPERTIES[l]["yT2"],
                               PROPERTIES[l]["sideResp"],PROPERTIES[l]["xmouse"],PROPERTIES[l]["ymouse"],PROPERTIES[l]["timestamp_mouse"],
                               PROPERTIES[l]["ROL"][0],PROPERTIES[l]["choiceLeft"],
                               PROPERTIES[l]["choiceRight"],PROPERTIES[l]["subjID"],
                               PROPERTIES[l]["otherID"],PROPERTIES[l]["gender"]])

              if x == "RISK_data":
                for m in range(0, 12):
                    MILISTA_RISK.append([PROPERTIES[m]["start_time"],PROPERTIES[m]["click_time"],PROPERTIES[m]["finger_time"],
                               PROPERTIES[m]["fix_duration"],PROPERTIES[m]["trial"],PROPERTIES[m]["RT"],PROPERTIES[m]["MT"],PROPERTIES[m]["xSR"],
                               PROPERTIES[m]["ySR"],PROPERTIES[m]["xT1"],PROPERTIES[m]["xT2"],PROPERTIES[m]["yT2"],
                               PROPERTIES[m]["sideResp"],PROPERTIES[m]["xmouse"],PROPERTIES[m]["ymouse"],PROPERTIES[m]["timestamp_mouse"],
                               PROPERTIES[m]["ROL"][0],PROPERTIES[m]["choiceLeft"],
                               PROPERTIES[m]["choiceRight"][0],PROPERTIES[m]["choiceRight"][1],PROPERTIES[m]["subjID"],PROPERTIES[m]["risk"],PROPERTIES[m]["win_lose"],
                               PROPERTIES[m]["otherID"],PROPERTIES[m]["gender"]])


              if x == "PROSOCIAL_data":
                for n in range(0, 24):
                    MILISTA_PROSOCIAL.append([PROPERTIES[n]["start_time"],PROPERTIES[n]["click_time"],PROPERTIES[n]["finger_time"],
                               PROPERTIES[n]["fix_duration"],PROPERTIES[n]["trial"],PROPERTIES[n]["RT"],PROPERTIES[n]["MT"],PROPERTIES[n]["xSR"],
                               PROPERTIES[n]["ySR"],PROPERTIES[n]["xT1"],PROPERTIES[n]["xT2"],PROPERTIES[n]["yT2"],
                               PROPERTIES[n]["sideResp"],PROPERTIES[n]["xmouse"],PROPERTIES[n]["ymouse"],PROPERTIES[n]["timestamp_mouse"],
                               PROPERTIES[n]["ROL"][0],PROPERTIES[n]["ROL"][1],PROPERTIES[n]["choiceLeft"][0], PROPERTIES[n]["choiceLeft"][1],
                               PROPERTIES[n]["choiceRight"][0],PROPERTIES[n]["choiceRight"][1],PROPERTIES[n]["subjID"],
                               PROPERTIES[n]["otherID"],PROPERTIES[n]["gender"]])
            else:
                print("  NEXT")


survey_data = pd.DataFrame(MILISTA_SURV)
prosocial_data = pd.DataFrame(MILISTA_PROSOCIAL)
intertemp_data = pd.DataFrame(MILISTA_INTERTEMP)
risk_data = pd.DataFrame(MILISTA_RISK)
prosocial_percep =pd.DataFrame(MILISTA_PROS_PERCEP)
risk_percep =pd.DataFrame(MILISTA_RISK_PERCEP)
temp_percep =pd.DataFrame(MILISTA_TEMP_PERCEP)

survey_data.columns = ["ID", "Carrer", "semester",
                   "age", "gender","Resp1","Resp2","Resp3","Resp4","Resp5","Resp6",
                   "Resp7","Resp8","Resp9","Resp10","Resp11","Resp12","Resp13","Resp14"]

prosocial_percep.columns = ["subjID", "ROL", "task", "perception"]

risk_percep.columns = ["subjID", "ROL", "task", "perception"]

temp_percep.columns = ["subjID", "ROL", "task", "perception"]


prosocial_data.columns = ["start_time","click_time","finger_time",
                         "fix_duration","trial","RT","MT","xSR",
                         "ySR","xT1","xT2","yT2","sideResp","xmouse","ymouse","timestamp_mouse",
                          "ROL_YO","ROL_OTRO","choiceLeft_1", "choiceLeft_2","choiceRight_1",
                          "choiceRight_2","subjID", "otherID","gender"]
intertemp_data.columns = ["start_time","click_time","finger_time",
                          "fix_duration","trial","RT","MT","xSR",
                          "ySR","xT1","xT2","yT2","sideResp","xmouse",
                          "ymouse","timestamp_mouse","ROL","choiceLeft","choiceRight_1",
                          "choiceRight_2","subjID","risk","win_lose","otherID","gender"]

risk_data.columns = ["start_time","click_time","finger_time","fix_duration","trial","RT","MT","xSR",
                    "ySR","xT1","xT2","yT2","sideResp","xmouse","ymouse","timestamp_mouse",
                     "ROL_YO","ROL_OTRO","choiceLeft", "choiceLeft","choiceRight_1","choiceRight_2","subjID",
                     "otherID","gender"]

survey_data.to_csv(r'..\Toda\Processed\survey.csv', index=False)
prosocial_percep.to_csv(r'..\Toda\Processed\prosocial_percep.csv', index=False)
risk_percep.to_csv(r'..\Toda\Processed\risk_percep.csv', index=False)
temp_percep.to_csv(r'..\Toda\Processed\temp_percep.csv', index=False)
prosocial_data.to_csv(r'..\Toda\Processed\prosocial_data.csv', index=False)
intertemp_data.to_csv(r'..\Toda\Processed\intertemp_data.csv', index=False)
risk_data.to_csv(r'..\Toda\Processed\risk_data.csv', index=False)



