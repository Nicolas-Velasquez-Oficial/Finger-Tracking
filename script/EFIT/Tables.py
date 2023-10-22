##Importar las librerias y bases de datos que se necesitan
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from matplotlib import pyplot as plt
from linearmodels.panel import PanelOLS
from linearmodels import PanelOLS
from scipy.stats import chi2_contingency
import scipy.stats as stats
####importing Prosocial merged table##############

prosocial = pd.read_csv('prosocial_merged_total.csv')
###Descriptives
cols_to_exclude = ['Unnamed: 0','GS','id_x','trial','trial.1','xSR','ySR','xT1','xT2','yT2','xmouse','ymouse','timestamp_mouse','ROL_YO','ROL_OTRO','choiceLeft_1','choiceLeft_2','choiceRight_1','choiceRight_2','gender_x','par','trial','id_y','Municipality','Father_Municipality','Faculty']  # list of column names to exclude
cols_to_include = [col for col in prosocial.columns if col not in cols_to_exclude]  # list of column names to include
descriptives = prosocial[cols_to_include].describe(include="all").loc[["count", "mean", "std", "min", "max"]].T
#descriptives.to_latex('descriptives.txt')
descriptives.to_latex('descriptives.txt', float_format="%.2f")

####importing Prosocial merged table##############
# plot a histogram of column A with 10 bins, values between 0 and 6, and blue bars
plt.hist(prosocial['csi'], bins=15, range=(0, 2), color='blue')

# add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Column A')

# show the plot
plt.show()


##########################BALANCE TEST#############################################

survey = pd.read_csv("survey_old.csv")
survey.columns = ["GS", "id", "semester", "age", "gender", "Municipality",
                  "From_Capital", "Father_Capital", "Father_Municipality",
                  "Harmed by the conflict","Affected physically/psycologically by the conflict",
                  "Affected directly/indirectly by the conflict","Family affected by the conflict",
                  "Conflict knowledge","Conflict history knowledge",
                  "Peace jurisdiction(JEP) knowledge","Peace jurisdiction(JEP) changes knowledge",
                  "Homosexual Marrige","Adoption by homosexual couples","Euthanasia legalization",
                  "Abortion legalization","Marijuana legalization","Flexible gender roles","Faculty","Rol"]

prosocial_balance = survey.loc[:,['Rol', 'semester', 'age', 'gender', "From_Capital", "Father_Capital", 'Harmed by the conflict', 'Affected physically/psycologically by the conflict', 'Affected directly/indirectly by the conflict', 'Family affected by the conflict', 'Conflict knowledge', 'Conflict history knowledge', 'Peace jurisdiction(JEP) knowledge', 'Peace jurisdiction(JEP) changes knowledge', 'Homosexual Marrige', 'Adoption by homosexual couples', 'Euthanasia legalization', 'Abortion legalization', 'Marijuana legalization', 'Flexible gender roles']]

# Create a contingency table for each variable and treatment combination
contingency_tables = {}
for var in prosocial_balance.columns[1:]:
    contingency_tables[var] = pd.crosstab(prosocial_balance['Rol'], prosocial_balance[var], margins=True)

# Loop through each contingency table and perform the chi-square test
results = []
for var, table in contingency_tables.items():
    chi2, p, dof, expected = chi2_contingency(table.values)
    results.append({'Variable': var, 'Chi-square': chi2, 'p-value': p})

# Combine results into a single dataframe
results_df = pd.DataFrame(results)

# Print results
print(results_df)


# Convert dataframe to LaTeX table
latex_table = results_df.to_latex(index=False, column_format='lrr')

# Print LaTeX table
print(latex_table)

#############################Prosocial Tables######################################


prosocial['par'] = prosocial['par'].astype('category')

##Sin Controles
prosocial_nocontrol = smf.ols('zeta1 ~ C(par,Treatment("YOU_STU"))', data=prosocial).fit()
print(prosocial_nocontrol.summary())

# Create fixed effects model with Categorical Treatment Variable 'treatment_var'
prosocial_fe_model = smf.mixedlm('csi ~ C(par,Treatment("YOU_STU")) ', data=prosocial, groups=prosocial["id_x"])

# Fit model
fe_results = prosocial_fe_model.fit()

# Print results summary
print(fe_results.summary())

# fit the model
#results = prosocial_fixed_effects.fit()

# create dummy variables for fixed effects
prosocial['group'] = prosocial['group'].astype('category')
prosocial['time'] = prosocial['time'].astype('category')

prosocial_fe = smf.ols('csi ~ C(par,Treatment("YOU_STU")) + C(group) + C(time)', data=prosocial).fit()
print(prosocial_fe.summary())
# print summary
print(results.summary())


data = prosocial.set_index(['group', 'time'])

y = data['csi']
X = data['par']

model = PanelOLS.from_formula('csi ~ 1+ C(par,Treatment("YOU_STU"))', data=data, entity_effects=True)

# Fit the model
results = model.fit()

# View the results summary
print(results.summary)

###Muestra de tabla con los diferentes modelos
results = summary_col([prosocial_nocontrol, ],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)', 'Model\n(3)', 'Model\n(4)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})

