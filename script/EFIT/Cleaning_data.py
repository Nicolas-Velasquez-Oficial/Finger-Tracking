import pandas as pd
import numpy as np

survey = pd.read_csv("survey.csv")
survey.columns = ["ID", "career", "semester",
                   "age", "gender","Harmed by the conflict","Affected physically/psycologically by the conflict","Affected directly/indirectly by the conflict","Family affected by the conflict","Conflict knowledge","Conflict history knowledge",
                   "Peace jurisdiction(JEP) knowledge","Peace jurisdiction(JEP) changes knowledge","Homosexual Marrige","Adoption by homosexual couples","Euthanasia legalization","Abortion legalization","Marijuana legalization","Flexible gender roles"]
survey.describe()
survey.unique('carrer')
print(survey.unique(["carrer"]))
# The describe method to get n,  means, stds, min, max
df_desc = survey.describe().loc[["count","mean", "std","min","max"]].T
df_desc.to_latex()
