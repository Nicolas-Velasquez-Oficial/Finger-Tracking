import numpy as np
import pandas as pd

#Import database
data_0 = pd.read_csv('TRUST_experimental_session_P1_v6_July+10,+2022_16.32.csv')
Delay = pd.read_csv('Delay.csv')
Extra = pd.read_csv('Data_Extra.csv')
#SEGMENT AND REPLACING VALUES
data_0 = data_0.loc[2:,:]
#data_0.to_excel('sample_data.xlsx', sheet_name='Data', index=False)
data_1 = data_0.replace({'10. Está dispuesto(a) a actuar de esa manera totalmente': 10,
                         '1. No está dispuesto(a) a actuar de esa manera en lo absoluto': 1,
                         '10. Lo describe perfectamente': 10, '1. No lo describe en lo absoluto': 1,
                         '7. Mucho': 7, '1. Nada': 1, '7. Muy probablemente': 7, '1. Poco probable': 1,
                         '7. Muchísimo': 7, '1. Nunca': 1, '7. Siempre': 7, '1. Nada Común': 1,
                         '5. Muy Común': 5, 'Ninguno': np.NaN, 'No Sabe': np.NaN})
data_2 = data_1.merge(Delay, how='outer', left_on='ResponseId', right_on='ResponseId')
data_3 = data_2.merge(Extra, how='outer',left_on='ResponseId', right_on='ResponseId')

data_3['Extra'] = data_3['Extra'].replace([np.NaN],0)
data_3['Delay'] = data_3['Delay'].replace([np.NaN],0)
data_3['Delay12'] = data_3['Delay12'].replace([np.NaN],0)

data_3.to_csv('TRUST_experimental_session_P1_v6_July+10.csv', index=False)