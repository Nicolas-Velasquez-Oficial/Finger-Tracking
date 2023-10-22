import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
def str_to_array(list_string):
    # converts a list that is surrounded by quotes to a numpy array
    # e.g. "[0,1,2,3]" to array([0,1,2,3])
    str_split = list_string.split(",")
    first_ele = float(str_split[0].replace("[", ""))
    last_ele = float(str_split[-1].replace("]", ""))
    other_ele = np.array(list(str_split)[1:-1], dtype=float)
    all_ele = np.insert(other_ele, 0, first_ele)
    all_ele = np.append(all_ele, last_ele)
    return all_ele


def process_trajectory_data(x_traj, y_traj, data):
    # Process x trajectories
    x_list = x_traj.apply(str_to_array).tolist()
    x_list_subtracted = [x - data.loc[i, 'xSR'] for i, x in enumerate(x_list)]

    max_len_x = max(len(x) for x in x_list_subtracted)
    x_df = pd.DataFrame([np.pad(x, (0, max_len_x - len(x)), 'constant') for x in x_list_subtracted],
                        columns=[f'x_{i}' for i in range(max_len_x)])

    # Process y trajectories
    y_list = y_traj.apply(str_to_array).tolist()
    y_list_subtracted = [y - data.loc[i, 'ySR'] for i, y in enumerate(y_list)]

    max_len_y = max(len(y) for y in y_list_subtracted)
    y_df = pd.DataFrame([np.pad(y, (0, max_len_y - len(y)), 'constant') for y in y_list_subtracted],
                        columns=[f'y_{i}' for i in range(max_len_y)])

    # Calculate the length of x and y trajectories using the subtracted lists
    length_df = pd.DataFrame({'length_x': [len(x) for x in x_list_subtracted],
                              'length_y': [len(y) for y in y_list_subtracted]})

    return x_df, y_df, length_df



def process_trajectory_data_1(x_traj, y_traj, data):
    # Process x trajectories
    x_list = x_traj.apply(str_to_array).tolist()

    # Process y trajectories
    y_list = y_traj.apply(str_to_array).tolist()

    # Calculate the length of x and y trajectories
    length_df = pd.DataFrame({'length_x': [len(x) for x in x_list],
                              'length_y': [len(y) for y in y_list]})

    # Create dataframes for x and y trajectories
    x_df = pd.DataFrame(x_list, columns=[f'x_{i}' for i in range(length_df['length_x'].max())])
    y_df = pd.DataFrame(y_list, columns=[f'y_{i}' for i in range(length_df['length_y'].max())])

    return x_df, y_df, length_df

data1 = pd.read_csv("prosocial_data.csv")
data2 = pd.read_csv("risk_data.csv")
data3 = pd.read_csv("intertemp_data.csv")

# Example usage:
x_df, y_df, length_df = process_trajectory_data_1(data1['xmouse'], data1['ymouse'], data1)

x_df2, y_df2, length_df2 = process_trajectory_data_1(data2['xmouse'], data2['ymouse'], data2)

x_df3, y_df3, length_df3 = process_trajectory_data_1(data3['xmouse'], data3['ymouse'], data3)


###################Proving that the two columns are equal####################################

are_columns_equal = length_df['length_x'].equals(length_df['length_y'])
print("Are the two columns equal?", are_columns_equal)

#x_df_2 = x_df.loc[0,:]
#y_df_2 = y_df.loc[0,:]
#plt.plot(x_df_2,y_df_2)
####1200=x x 1920=y pixels, 16:10 ratio######
x_df_1 = (x_df/1200)
y_df_1 = ((y_df*-1)/1920)+1
x_df_2 = (x_df2/1200)
y_df_2 = ((y_df2*-1)/1920)+1
x_df_3 = (x_df3/1200)
y_df_3 = ((y_df3*-1)/1920)+1

def subtract_first_value(x_df, y_df):
    x_df_subtracted = x_df.sub(x_df.iloc[:, 0], axis=0)
    y_df_subtracted = y_df.sub(y_df.iloc[:, 0], axis=0)
    return x_df_subtracted, y_df_subtracted

x_df_centered, y_df_centered = subtract_first_value(x_df_1, y_df_1)
x_df_centered2, y_df_centered2 = subtract_first_value(x_df_2, y_df_2)
x_df_centered3, y_df_centered3 = subtract_first_value(x_df_3, y_df_3)
###################Export x, y , and lenght##################################################

y_df_centered.to_csv('Y_proc.csv', index=False)
x_df_centered.to_csv('X_proc.csv', index=False)
length_df.to_csv('length_proc.csv', index=False)

y_df_centered2.to_csv('Y_risk.csv', index=False)
x_df_centered2.to_csv('X_risk.csv', index=False)
length_df2.to_csv('length_risk.csv', index=False)

y_df_centered3.to_csv('Y_temp.csv', index=False)
x_df_centered3.to_csv('X_temp.csv', index=False)
length_df3.to_csv('length_temp.csv', index=False)


