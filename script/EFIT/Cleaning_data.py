import pandas as pd

#### Adjusting ID and Pairs in prosocial data################
prosocial_data = pd.read_csv("prosocial_WIT.csv")

risk_data = pd.read_csv("risk_data_GS.csv")

temporal_data = pd.read_csv("intertemp_data_GS.csv")


#### Importing entropy data for the three games################
matlab_prosocial_entropy =pd.read_csv("prosocial_EFIT_07-May-2023.csv", header=None)
matlab_risk_entropy =pd.read_csv("risk_EFIT_20-Sep-2023.csv", header=None)
matlab_temporal_entropy =pd.read_csv("temp_EFIT_20-Sep-2023.csv", header=None)

matlab_prosocial_entropy.columns = ["trial", "psi", "csi","zeta1", "zeta2"]
matlab_risk_entropy.columns = ["trial", "psi", "csi","zeta1", "zeta2"]
matlab_temporal_entropy.columns = ["trial", "psi", "csi","zeta1", "zeta2"]

prosocial_percep =pd.read_csv("prosocial_percep.csv")
risk_percep =pd.read_csv("risk_percep.csv")
temporal_percep =pd.read_csv("temp_percep.csv")
#### Importing survay################
survey = pd.read_csv("survey_old.csv")
survey.columns = ["GS", "id", "semester", "age", "gender", "Municipality",
                  "From_Capital", "Father_Capital", "Father_Municipality",
                  "Harmed by the conflict","Affected physically/psycologically by the conflict",
                  "Affected directly/indirectly by the conflict","Family affected by the conflict",
                  "Conflict knowledge","Conflict history knowledge",
                  "Peace jurisdiction(JEP) knowledge","Peace jurisdiction(JEP) changes knowledge",
                  "Homosexual Marrige","Adoption by homosexual couples","Euthanasia legalization",
                  "Abortion legalization","Marijuana legalization","Flexible gender roles","Faculty","Rol"]

#### merging data bases################
prosocial_entropy = pd.concat([prosocial_data , matlab_prosocial_entropy], axis=1)
prosocial_merged_pre = pd.merge(prosocial_entropy, survey, on='GS')
prosocial_merged = pd.merge(prosocial_merged_pre, prosocial_percep, on='GS')
file_name = 'prosocial_merged_total.csv'
prosocial_merged.to_csv(file_name)


temporal_entropy = pd.concat([temporal_data , matlab_temporal_entropy], axis=1)
temporal_merged_pre = pd.merge(temporal_entropy, survey, on='GS')
temporal_merged = pd.merge(temporal_merged_pre, temporal_percep, on='GS')
file_name = 'temporal_merged_total.csv'
temporal_merged.to_csv(file_name)

risk_entropy = pd.concat([risk_data , matlab_risk_entropy], axis=1)
risk_merged_pre = pd.merge(risk_entropy, survey, on='GS')
risk_merged = pd.merge(risk_merged_pre, risk_percep, on='GS')
file_name = 'risk_merged_total.csv'
risk_merged.to_csv(file_name)

# The describe method to get n,  means, stds, min, max
df_desc = survey.describe().loc[["count","mean", "std","min","max"]].T
df_desc.to_latex()
