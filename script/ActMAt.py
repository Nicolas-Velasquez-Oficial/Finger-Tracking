import json
import os
import pandas as pd
MILISTA = []
for i in range(1, 3):
    for j in range(1, 136):
        ruta = 'Data\G' + str(i) + 'S' + str(j) + "_"
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

                MILISTA.append([PROPERTIES["ID"], PROPERTIES["Carrera"], PROPERTIES["Semestre"],PROPERTIES["Edad"], PROPERTIES["Genero"],
                                 PROPERTIES["res5"]
                                 ,PROPERTIES["resP"],
                                PROPERTIES["Resp"][0], PROPERTIES["Resp"][1],
                               PROPERTIES["Resp"][2], PROPERTIES["Resp"][3], PROPERTIES["Resp"][4],
                                PROPERTIES["Resp"][5], PROPERTIES["Resp"][6], PROPERTIES["Resp"][7],
                                PROPERTIES["Resp"][8], PROPERTIES["Resp"][9], PROPERTIES["Resp"][10],
                                PROPERTIES["Resp"][11], PROPERTIES["Resp"][12], PROPERTIES["Resp"][13]])
              else:
                print("  NEXT")

df = pd.DataFrame(MILISTA)
cabecera=["ID", "Carrera", "Semestre", "Edad", "Genero","Municipio","Municipio_Padres","Resp1","Resp2","Resp3","Resp4","Resp5","Resp6","Resp7","Resp8","Resp9",
          "Resp10","Resp11","Resp12","Resp13","Resp14"]


