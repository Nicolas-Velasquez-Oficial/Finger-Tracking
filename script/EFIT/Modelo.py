##Importar las librerias y bases de datos que se necesitan
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
import matplotlib.pyplot as plt
##Descarga de la base de datos colapsada##
base = pd.read_csv("Colapsadacontodo1nan.csv")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
###Modelos de prosocial########
##Sin Controles
results2 = smf.ols('svo ~ C(par,Treatment(8))', data=base).fit()
print(results2.summary())
###Con controles sociodemográficos y universitarios###
results4 = smf.ols('svo ~ C(par,Treatment(8)) + edad + semestre +Capital_Muni + Capital_Muni_Padres + C(facu,Treatment(3))', data=base).fit()
print(results4.summary())
###Concontroles SD Y ORIENTACIÓN POLÍTICA
results6 = smf.ols('svo ~ C(par,Treatment(8)) + edad + semestre +Capital_Muni + Capital_Muni_Padres +C(facu,Treatment(3)) + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO', data=base).fit()
print(results6.summary())
###Concontroles SD Y ORIENTACIÓN POLÍTICA
results3 = smf.ols('svo ~ C(par,Treatment(8)) + edad + semestre +Capital_Muni + Capital_Muni_Padres +C(facu,Treatment(3)) + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + DR1 + risk_wins + risk_lose', data=base).fit()
print(results3.summary())
###Muestra de tabla con los diferentes modelos
results = summary_col([results2, results4, results6, results3],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)', 'Model\n(3)', 'Model\n(4)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})

###Para poder exportarlos en formato text y latex
results_text = results.as_text()
resultFile = open("table.csv",'w')
resultFile.write(results_text)
resultFile.close()
print(results.as_latex())
results_latex = results.as_latex()
resultFilelatex = open("tabla.txt",'w')
###Para ver si la perdida de potencia estuvo en la categoría EXPARA-EXGUERRILLA
PODER = smf.ols('salida ~ C(par,Treatment(5))', data=base).fit(cov_type='HC3')
print(PODER.summary())

###MODELO DISCOUNT RATE
base2 = pd.read_csv("base2410.csv")
results7 = smf.ols('perception ~ C(rolself,Treatment(2))', data=base2).fit(cov_type='HC3')
results8 = smf.ols('perception ~ C(rolself,Treatment(2)) + DR1', data=base2).fit(cov_type='HC3')
results9 = smf.ols('perception ~ C(rolself,Treatment(2)) + DR1 + gender + semestre + edad + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + C(facu,Treatment(14)) ', data=base2).fit(cov_type='HC3')
results2i = summary_col([results7, results8, results9],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)','Model\n(3)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
print(results2i.as_latex())
##logit
results10 = smf.glm('perception ~ C(rolself,Treatment(2))', data=base2, family=sm.families.Binomial(link=sm.families.links.logit))
results11 = smf.glm('perception ~ C(rolself,Treatment(2)) + DR1', data=base2, family=sm.families.Binomial(link=sm.families.links.logit))
results12 = smf.glm('perception ~ C(rolself,Treatment(2)) + DR1 + gender + semestre + edad + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + C(facu,Treatment(14)) ', data=base2, family=sm.families.Binomial(link=sm.families.links.logit))
results13 = summary_col([results10, results11, results12],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)','Model\n(3)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
print(results13.as_latex())
print(results12.fit().summary())
###MODELO RISK AVERSION Wins
base3 = pd.read_csv("baserisk2510.csv")
results10 = smf.ols('perception ~ C(rolself,Treatment(2))', data=base3[base3.win_lose == 1]).fit(cov_type='HC3')
results11 = smf.ols('perception ~ C(rolself,Treatment(2)) + risk', data=base3[base3.win_lose == 1]).fit(cov_type='HC3')
results12 = smf.ols('perception ~ C(rolself,Treatment(2)) + risk + genero + semestre + edad + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + C(facu,Treatment(14)) ', data=base3[base3.win_lose == 1]).fit(cov_type='HC3')
results6 = summary_col([results10, results11, results12],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)','Model\n(3)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'Log-Likelihood':lambda x: "{:.2f}".format(x.rsquared)})

results13= smf.glm('perception ~ C(rolself,Treatment(2))', data=base3[base3.win_lose == 1], family=sm.families.Binomial(link=sm.families.links.logit))
print(results13.fit().summary())
results14 = smf.glm('perception ~ C(rolself,Treatment(2)) + risk', data=base3[base3.win_lose == 1], family=sm.families.Binomial(link=sm.families.links.logit))
print(results14.fit().summary())
results15 = smf.glm('perception ~ C(rolself,Treatment(2)) + risk + genero + semestre + edad + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + C(facu,Treatment(14)) ', data=base3[base3.win_lose == 1], family=sm.families.Binomial(link=sm.families.links.logit))
print(results15.fit().summary())


results7 = summary_col([results13, results14, results15],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)','Model\n(3)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
print(results7.as_latex())

###MODELO RISK AVERSION Loose
results13 = smf.ols('perception ~ C(rolself,Treatment(2))', data=base3[base3.win_lose == 0]).fit(cov_type='HC3')
results14 = smf.ols('perception ~ C(rolself,Treatment(2)) + risk', data=base3[base3.win_lose == 0]).fit(cov_type='HC3')
results15 = smf.ols('perception ~ C(rolself,Treatment(2)) + risk +genero + semestre + edad + AFECTADO_POR_EL_CONFLICTO + CONOCIMIENTO_CONFLICTO + POLITICO + C(facu,Treatment(14)) ', data=base3[base3.win_lose == 0]).fit(cov_type='HC3')

results4 = summary_col([results13, results14, results15],stars=True,float_format='%0.2f',
                  model_names=['Model\n(1)', 'Model\n(2)','Model\n(3)'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.2f}".format(x.rsquared)})
print(results4.as_latex())