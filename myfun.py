import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import json
import math
import re
from linearmodels import PanelOLS
import copy
import scipy

def my_barplot(data, var, ylab, ylims, title, controls, simple):
    #data = reachData_self
    #var = 'AUC'
    #ylab = 'AUC (px)' #'Velocity (meters per second)'
    #ylims = [-25, 25]
    #title = "AUC selfish choice"
    #controls = 0 no, 1 yes sociodemographic and other controls (see regression below for which ones)
    #simple = 0 no (pairs), 1 yes (roles)
    
    data = data.astype({'trial':'int64'})
    panel = data.set_index(['subjID', 'trial'])
    if controls == 1:
        if simple == 0:
            #reg = smf.ols(var +
            #              "~ C(condition, Treatment(reference='YOU-STU')) + RT + degree + age + gender + res + res_parents + knowledge + exposure + ideology ",
            #              data=data)  
            reg = PanelOLS.from_formula(var + "~ 1+C(condition, Treatment(reference='YOU-STU')) + RT  + EntityEffects", data = panel)
        elif simple == 1:
            #reg = smf.ols(var +
            #              "~ C(condition_general, Treatment(reference='YOU')) + RT + degree + age + gender + res + res_parents + knowledge + exposure + ideology ",
            #              data=data)
            reg = PanelOLS.from_formula(var + "~ 1+C(condition_general, Treatment(reference='YOU')) + RT + EntityEffects", data = panel)
        #reg_fit = reg.fit(cov_type='HC3')
        reg_fit = reg.fit(cov_type='robust')
    else:
        if simple == 0:
            reg = smf.ols(var +
                          "~ C(condition, Treatment(reference='YOU-STU'))",
                          data=data)
        elif simple == 1:
            reg = smf.ols(var +
                          "~ C(condition_general, Treatment(reference='YOU'))",
                          data=data)
        reg_fit = reg.fit(cov_type='HC3')

    estimates = reg_fit.params
    pvalues = reg_fit.pvalues
    conditions = list(pvalues.index)
    # reg = smf.mixedlm(var + "~ C(condition, Treatment(reference='TU-EST'))", data = data, groups=reachData['subjID'], re_formula="~1")
    # reg_fit = reg.fit()
    # print(reg_fit.summary())

    if simple == 0:
        meanC = data.groupby(['subjID', 'condition']).mean().reset_index()
        N = len(meanC['condition'].unique())
        y = data.groupby(['condition']).mean()[var].sort_values()
        y_idx = y.index
        y_err = data.groupby(['condition']).sem().loc[y_idx, var]
    else:
        meanC = data.groupby(['subjID', 'condition_general']).mean().reset_index()
        N = len(meanC['condition_general'].unique())
        y = data.groupby(['condition_general']).mean()[var].sort_values()
        y_idx = y.index
        y_err = data.groupby(['condition_general']).sem().loc[y_idx, var]


    #plt.figure(figsize=[7, 7])
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    #y = meanC.groupby(['condition']).mean()[var].sort_values()
    #y_err = meanC.groupby(['condition']).sem().loc[y_idx, var]
    color_bars = []
    for i in range(len(y_idx)):
        condT = y_idx[i]
        check = 0
        counter = 0
        if condT=='YOU-STU' or condT=='YOU':
            color_bars.append('white')
        else:
            while check == 0:
                rexp = re.findall(condT, conditions[counter])
                if len(rexp) > 0:
                    if pvalues[counter] <= 0.05:
                        if estimates[counter]>0:
                            color_bars.append('orange')
                        else:
                            color_bars.append('gray')
                    else:
                        color_bars.append('white')
                    check = 1
                counter += 1
                if counter > len(conditions):
                    check = 1

    plt.bar(ind, y, width, yerr=y_err, color = color_bars, edgecolor = 'black')
    plt.ylabel(ylab)
    plt.title(title)
    plt.xticks(ind, y.index, rotation=90)
    #plt.xlim(40, 160)
    plt.ylim(ylims[0], ylims[1])
    # plt.yticks(np.arange(0, 81, 10))
    # plt.show()

def str_to_array(list_string):
    #converts a list that is surrounded by quotes to a numpy array
    #e.g. "[0,1,2,3]" to array([0,1,2,3])
    str_split = list_string.split("a")
    first_ele = float(str_split[0].replace("[",""))
    last_ele = float(str_split[-1].replace("]",""))
    other_ele = np.array(list(str_split)[1:-1], dtype = float)
    all_ele = np.insert(other_ele, 0, first_ele)
    all_ele = np.append(all_ele, last_ele)
    return all_ele

def myPlot3(DATA, sub, idx_traj, name_x = 'x', name_y= 'y', conds = ['Gender_Img', 'Gender_Typ'], name_sub='subjID'):
    #plots subject trajectories
    #sub: int; subject to plot
    #name_sub: str; column name with sub
    #conds: list; name of columns with exp. conditions
    
    #see .log psychopy files for the following measures
    dims = np.array([0.3596938775510204,0.25]) #[width, height] of start region
    coordSR = np.array([0, -0.8]) #[x,y] center start region
    
    temp = DATA[name_sub].unique()
    sub = temp[sub]
    idx = (DATA.loc[:, name_sub] == sub) & (idx_traj) #it drops trials were the index finger jumped
    x = DATA.loc[idx, conds+[name_x]]
    y = DATA.loc[idx, conds+[name_y]]
    
    plt.figure(figsize=[7, 7])
    collor = plt.cm.gray(np.linspace(0, 0.7, 20)) #darker colors are later trials
    counter = 1
    titles = ['Man typical', 'Man atypical', 'Woman typical', 'Woman atypical']
    conds_in_titles = [['M','Typical'],['M','Atypical'],
                       ['F','Typical'],['F','Atypical']]
    for idx_tt, tt in enumerate(titles):
        plt.subplot(int(str(22) + str(counter)))
        plt.title(tt)
        idx = (x[conds[0]] == conds_in_titles[idx_tt][0]) & (x[conds[1]] == conds_in_titles[idx_tt][1])
        xt = x.loc[idx,:].reset_index(drop=True)
        yt = y.loc[idx,:].reset_index(drop=True)
        for pps in range(xt.shape[0]):
            xt_plot = str_to_array(xt.loc[pps, name_x])
            yt_plot = str_to_array(yt.loc[pps, name_y])

            idx_next_button = (xt_plot>(coordSR[0]-dims[0])) & (xt_plot<(coordSR[0]+dims[0])) & \
                              (yt_plot>(coordSR[1]-dims[1])) & (yt_plot<(coordSR[1]+dims[1])) # drops position close to the next_button to advance instructions. The start region was on the center.
            plt.plot(xt_plot[idx_next_button.argmax():-1], yt_plot[idx_next_button.argmax():-1], color=collor[pps])
            #plt.plot(xt_plot, yt_plot, color=collor[pps])
        plt.xlabel('Horizontal (a.u)')
        plt.ylabel('Forward (a.u)')
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        counter = counter + 1

    plt.tight_layout()


    
def reach_metrics(data, name_x, name_y, name_time, name_RT, name_MT, name_choice, name_asked, name_subjID, name_task, name_slider_touch, name_slider_appear, conds, dems, plot_trial = 10):
    #Velocity, AUC with reference to a straight trajectory to the center of the target, and direction angle
    #data: pandas dataframes in LONG format
    #name_: string with name of the column with x,y, time axis, MT, RT, response/choice, subj_ID
    #_cat: string or category names of the left and right options
    #conds: list with names of columns of experimental conditions
    #dems: list with demographics
    
    print("WORKING, BE PATIENT")
    printt = 0
    triaal = 0
    #plot_trial = 444  
    y_tol = 0.15
    s_current = data.loc[0,name_subjID]
    count_count = 0
    for choice in range(data.shape[0]):
        #print(choice)
        condCCC = type(data.loc[choice,'screen_resolution']) is str
        if condCCC:
            res_screen = np.array(data.loc[choice,'screen_resolution'].split("x"),dtype=int) #width, height
        else:
            res_screen = 'not available'
        lifted_finger = data.loc[choice,'lifted_finger']
        RTT = data.loc[choice, name_RT] #response time (ms)
        MTT = data.loc[choice, name_MT] #movement time (ms)
        #accept_offer =  data.loc[choice, name_choice]
        selected_option =  data.loc[choice, name_choice]
        asked_option =  data.loc[choice, name_asked]
        exp_conds = data.loc[choice, conds]
        task = data.loc[choice, name_task]
        demog = data.loc[choice, dems]
        s = data.loc[choice, name_subjID]
        if s_current==s:
            triaal = triaal + 1 #trial is counting regardless of task; is the order of presentation
        else:
            s_current=s
            triaal = 1
        if choice/data.shape[0]>0.5 and printt == 0:
            printt = 1
            print('HALFWAY THROUGH!')

        #bad_subj and bad_task are paired. 
        #They indicate weird trajectories e.g. with negative times.
        bad_subj = ['32f77c3b08592cd1_861b49d1857524a8_cc430c747a15dd31_48dea1ea01dca25d2da2be00cc2aba17'] 
        bad_task = ['resp_dictator_1']
        condA = (bad_subj[0]==s and bad_task[0]==task) 
        condDDD = type(data.loc[choice, name_x]) is str
        if not condA and condCCC and condDDD:
            oktraj = str_to_array(data.loc[choice, name_x])
            x = str_to_array(data.loc[choice, name_x])
            y = str_to_array(data.loc[choice, name_y])
            time = str_to_array(data.loc[choice, name_time]) 
            t_end = data.loc[choice, name_slider_touch]
            t_0 = data.loc[choice,  name_slider_appear]
            t_out_start = t_0 + RTT #out of start region
            idx_0 = (np.array((time-t_0)<0.00001) & np.array((time-t_0)>(-0.00001))).argmax()
            idx_end = (np.array((time-t_end)<0.00001) & np.array((time-t_end)>(-0.00001))).argmax()
            idx_out_start = (np.array(np.abs(time-t_out_start))).argmin() #left the start region
            idx_out_tolerance = (y<(y[idx_out_start]-y_tol*res_screen[1])).argmax() #left tolerance region (remember, y is flipped) (i.e. subjs can go through the start region and start outside the bottom square; note that this will be trials with super fast RTs, which one could filter out)
            RT = idx_out_start
            #x_pre = x[idx_0:RT] #up to RT i.e. before the moment it left the start region square
            #y_pre = y[idx_0:RT]
            #time_pre = time[idx_0:RT]
            x_pre = x[idx_0:idx_out_tolerance] #up to the moment it left the tolerance region square
            y_pre = y[idx_0:idx_out_tolerance]
            time_pre = time[idx_0:idx_out_tolerance]
            vel3 = [] #pre-leaving start region
            for npoint in range(1, len(x_pre), 1):
                timediff = time_pre[npoint] - time_pre[npoint - 1]
                if timediff != 0:
                    vel3.append(math.sqrt((x_pre[npoint] - x_pre[npoint - 1]) ** 2 + (y_pre[npoint] - y_pre[npoint - 1]) ** 2) / (
                            time_pre[npoint] - time_pre[npoint - 1]))

            if len(vel3)>0 and len(time_pre)>0:
                min_vel = np.amin(vel3)
                min_vel_idx = np.where(vel3==min_vel)[0][0]
                x0 = x_pre[min_vel_idx] #coordinates when they were not (or minimally) moving inside the start region
                y0 = y_pre[min_vel_idx]
                #print('A')
                x0_idx =  np.where(x0==x)[0][0] 
                y0_idx =  x0_idx 

            else: 
                #count_count = count_count + 1               
                x0 = str_to_array(data.loc[choice, name_x])[RT] 
                y0 = str_to_array(data.loc[choice, name_y])[RT]
                x0_idx =  RT
                y0_idx =  RT
            #print(x0, y0, choice)
            #x0_idx_temp = np.where(x0==x)
            len_traj = idx_end-x0_idx
        else:
            oktraj = 'not ok'
            lifted_finger = 1
            MTT = 0
            len_traj = 0 
        
        if (type(oktraj) is np.ndarray) and not lifted_finger==1 and MTT>100 and len_traj>4 and not condA: #dont do rows that throw error
            

            #Generation of straight trayectory
            coordEND = np.array([x[idx_end], y[idx_end]]) #  
            coordREF = np.array([x0,y0]) #Starting position of subject
            #print(coordREF, coordSR)
            slope = (coordREF[1] - coordEND[1]) / (coordREF[0] - coordEND[0])
            intercept = coordREF[1] - slope*coordREF[0]
            ref_trajY = y[x0_idx:(idx_end+1)] #reference trajectory
            ref_trajX = (ref_trajY - intercept) / slope
            #print(choice, s, task, bad_subj[0]==s, bad_task[0]==task)


            #AUC
            #start_coord = [RT] #from RT i.e. the moment it left the start region square (pros: it discards the initial stillness from the mean)
            start_coord = [x0_idx]
            x = str_to_array(data.loc[choice, name_x])[start_coord[0]:(idx_end+1)] 
            y = str_to_array(data.loc[choice, name_y])[start_coord[0]:(idx_end+1)]
            AUC = np.sqrt((x - ref_trajX)**2 + (y - ref_trajY)**2).sum()
            maxDev = np.abs(x - ref_trajX).max()
            #maxDev = np.sqrt((x - ref_trajX[start_coord[0]:])**2 + (y - ref_trajY[start_coord[0]:])**2).max()
            if choice == plot_trial:
                print("Plotted this choice: ", choice)
                print("Plotted this subject: ", s)
                padding = 10  #px; this is a guess; y padding between questions in qualtrics
                start_vert_pos = 0.4 #in javascript; proportion of section where start button was placed
                coord_start = np.array([data.loc[choice,'coord_bottom_start'],
                                        data.loc[choice,'coord_top_start'],
                                        data.loc[choice,'coord_left_start'],
                                        data.loc[choice,'coord_right_start']]) #just of the LAST trial of the the LAST judgment (empathy)
                dim_start = np.array([np.abs(coord_start[3]-coord_start[2]),
                                      np.abs(coord_start[0]-coord_start[1])]) #width,height
                center_start = np.array([res_screen[0]*0.5 + dim_start[0]/2,
                                         res_screen[1]*start_vert_pos + dim_start[1]/2]) #x,y; Approximate, we didn't record this 

                coord_slider = np.array([data.loc[choice,'coord_bottom_slider'],
                                        data.loc[choice,'coord_top_slider'],
                                        data.loc[choice,'coord_left_slider'],
                                        data.loc[choice,'coord_right_slider']]) #just of the LAST trial of the the LAST judgment (empathy)
                dim_slider = np.array([np.abs(coord_slider[3]-coord_slider[2]),
                                      np.abs(coord_slider[0]-coord_slider[1])]) #width,height
                center_slider = np.array([coord_slider[2]+dim_slider[0]/2,
                                          coord_slider[1]+dim_slider[1]/2])#x,y; Approximate, we didn't record this 
                plt.plot(x, -y)
                plt.plot(ref_trajX, -ref_trajY, ls = '--')
                plt.scatter(x[0], -y[0], c = 'orange')
                plt.scatter(str_to_array(data.loc[choice, name_x])[idx_end], 
                            -str_to_array(data.loc[choice, name_y])[idx_end], c = 'red')
                #plt.scatter(str_to_array(data.loc[choice, name_x])[idx_out_start], 
                #            -str_to_array(data.loc[choice, name_y])[idx_out_start], c = 'green')
                plt.text(50,-1040, 'asked: ' + str(asked_option))
                plt.text(50,-970, 'response: ' + str(np.round(selected_option,2)))
                plt.text(50,-900, task) 
                #plt.text(100,-830, s) 
                #rectangle = plt.Rectangle((res_screen[0]*0.5-dim_start[0],
                #                           str_to_array(data.loc[choice, name_y])[idx_end] + dim_start[1] + res_screen[1]*start_vert_pos + padding), #remember: bottom is top i.e. y coords in javascript are flipped
                #                          dim_start[0], 
                #                          dim_start[1], 
                #                          fc=[1,1,1,0],ec="black")
                #plt.gca().add_patch(rectangle)
                rectangle = plt.Rectangle((coord_slider[2], 
                                           -(str_to_array(data.loc[choice, name_y])[idx_end] )), #remember: bottom is top i.e. y coords in javascript are flipped
                                          dim_slider[0], 
                                          dim_slider[1], 
                                          fc=[1,1,1,0],ec="black") #visual guide; we did not collect start rectangle or slider coordinates for all trials (just for the last trial of all judgments)
                plt.gca().add_patch(rectangle)
                plt.xlim(-50,1.05*coord_slider[3])
                plt.ylim(-1100,0);
                plt.savefig("figures/" + task + "_example_single_trajectory.png")


            #VELOCITY
            x = str_to_array(data.loc[choice, name_x])[start_coord[0]:(idx_end+1)] 
            y = str_to_array(data.loc[choice, name_y])[start_coord[0]:(idx_end+1)] 
            time = str_to_array(data.loc[choice, name_time])[start_coord[0]:] #list(range(0, 20 * len(x), 20))  # 20 is the sampling rate in hz
            vel = []
            checktime = 0
            for npoint in range(1, len(x), 1):
                timediff = time[npoint] - time[npoint - 1]
                if timediff != 0:
                    vel.append(math.sqrt((x[npoint] - x[npoint - 1]) ** 2 + (y[npoint] - y[npoint - 1]) ** 2) / (
                            time[npoint] - time[npoint - 1]))
                if timediff == 0:
                    checktime = 1



            # ANGLE (between point of max velocity and starting point)
            start_coord = [x0_idx]
            x = str_to_array(data.loc[choice, name_x])[start_coord[0]:(idx_end+1)] 
            y = -str_to_array(data.loc[choice, name_y])[start_coord[0]:(idx_end+1)] 
            time = str_to_array(data.loc[choice, name_time])[start_coord[0]:]  
            vel2 = []
            for npoint in range(1, len(x), 1):
                timediff = time[npoint] - time[npoint - 1]
                if timediff != 0:
                    vel2.append(math.sqrt((x[npoint] - x[npoint - 1]) ** 2 + (y[npoint] - y[npoint - 1]) ** 2) / (
                            time[npoint] - time[npoint - 1]))
            max_vel = np.amax(vel2)
            max_vel_idx = np.where(vel2==max_vel)[0][0]
            x_max_vel = x[max_vel_idx]
            y_max_vel = y[max_vel_idx]
            delta_x = x_max_vel - x0 
            delta_y = y_max_vel - (-y0)   
            theta_radians = math.atan2(delta_y, delta_x) #angle between starting point and point of max vel; angle*180/np.pi for degrees i.e. if degrees negative go clockwise starting at 0,0; if positive go counterclockwise starting at 0,0


            #COM (Changes of mind)
            #start_coord = [x0_idx]
            #x_com_0 = str_to_array(data.loc[choice, name_x])[start_coord[0]]
            #x_com_1 = str_to_array(data.loc[choice, name_x])[RT+1] #+1 in case x_com_0 is RT i.e. so delta_x or delta_y is not zero
            #y_com_0 = -str_to_array(data.loc[choice, name_y])[start_coord[0]]
            #y_com_1 = -str_to_array(data.loc[choice, name_y])[RT+1]
            #delta_x = x_com_1 - x_com_0 
            #delta_y = y_com_1 - y_com_0
            #theta_radians_com_0 = math.atan2(delta_y, delta_x) #initial exit angle  
            theta_radians_com_0 = theta_radians #angle between starting point and point of max vel; angle*180/np.pi for degrees 

            x_com_0 = str_to_array(data.loc[choice, name_x])[start_coord[0]]
            x_com_1 = str_to_array(data.loc[choice, name_x])[idx_end] 
            y_com_0 = -str_to_array(data.loc[choice, name_y])[start_coord[0]]
            y_com_1 = -str_to_array(data.loc[choice, name_y])[idx_end]
            delta_x = x_com_1 - x_com_0 
            delta_y = y_com_1 - y_com_0
            theta_radians_com_1 = math.atan2(delta_y, delta_x) #final arrival angle

            theta_diff = np.abs(theta_radians_com_0-theta_radians_com_1)
            COM = 0 #no change of mind
            if theta_diff>0.25 and theta_radians_com_0>np.pi/2 and theta_radians_com_0<np.pi and theta_radians_com_0>theta_radians_com_1: #
                #if moving to the left and initial angle > final angle, then CoM
                #Remember: the second quadrant is 90 to 180 degrees (or pi/2 to pi)
                COM = 1 #yes change of mind
                #print("jugo de bor", theta_diff, theta_radians_com_0, theta_radians_com_1)
            elif theta_diff>0.25 and theta_radians_com_0<np.pi/2 and theta_radians_com_0>0 and theta_radians_com_0<theta_radians_com_1:
                #if moving to the right and initial angle < final angle, then CoM
                #Remember: the first quadrant is 0 to 90 degrees (or 0 to pi/2)
                COM = 1 #yes change of mind
                #print("jugo de makj", theta_diff, theta_radians_com_0, theta_radians_com_1)


            if checktime==0: 
                count_count = count_count + 1
                vel = float(np.array(vel).mean())
                Rtemp = np.array([s, vel, AUC, maxDev, theta_radians, RTT, MTT, selected_option, asked_option,
                                  triaal, COM, task, lifted_finger])
                for e_c in exp_conds:
                    Rtemp = np.append(Rtemp,e_c)

                for g_f in demog:
                    Rtemp = np.append(Rtemp,g_f)

                if choice == 0:
                    REACH = pd.DataFrame([Rtemp], columns=['subjID', 'Vel', 'AUC', 'maxDev', 'Angle', 
                                                           'RT', 'MT', 'selected_option', 'asked_option', 
                                                           'trial', 'CoM', 'task', 'lifted_finger'] + conds + dems)
                else:
                    Rtemp = pd.DataFrame([Rtemp], columns=['subjID', 'Vel', 'AUC', 'maxDev', 'Angle', 
                                                           'RT', 'MT', 'selected_option', 'asked_option',
                                                           'trial', 'CoM', 'task', 'lifted_finger'] + conds + dems)
                    REACH = REACH.append(Rtemp)
        else:
            #print('Bad traj') #this could happen because the subject failed to stop at the start region or lifted their finger
            vel = np.nan
            AUC = np.nan
            maxDev = np.nan
            theta_radians = np.nan
            CoM = np.nan
            Rtemp = np.array([s, vel, AUC, maxDev, theta_radians, RTT, MTT, selected_option, asked_option,
                              triaal, COM, task, lifted_finger])
            for e_c in exp_conds:
                Rtemp = np.append(Rtemp,e_c)

            for g_f in demog:
                Rtemp = np.append(Rtemp,g_f)

            if choice == 0:
                REACH = pd.DataFrame([Rtemp], columns=['subjID', 'Vel', 'AUC', 'maxDev', 'Angle', 
                                                       'RT', 'MT', 'selected_option', 'asked_option', 
                                                       'trial', 'CoM', 'task', 'lifted_finger'] + conds + dems)
            else:
                Rtemp = pd.DataFrame([Rtemp], columns=['subjID', 'Vel', 'AUC', 'maxDev', 'Angle', 
                                                       'RT', 'MT', 'selected_option', 'asked_option',
                                                       'trial', 'CoM', 'task', 'lifted_finger'] + conds + dems)
                REACH = REACH.append(Rtemp)    


    print("DONE!!!", count_count/data.shape[0])


    REACH = REACH.astype({'subjID': 'category', 'Vel': 'float', 'AUC': 'float', 'maxDev':'float', 'Angle': 'float',
                          'RT':'float', 'MT':'float','selected_option': 'float', 'asked_option': 'category',  
                          'trial': 'float', 'CoM': 'float', 'task': 'category', 'lifted_finger': 'float',
                          'treatment': 'category'})

    return REACH.reset_index(drop=True)    
    
    
def annotate_barplot(sns_barplot):
    for p in sns_barplot.patches:
        sns_barplot.annotate(format(p.get_height(), '.3f'), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'left', va = 'center', 
                       xytext = (9, 7), 
                       textcoords = 'offset points')


def my_correction (a,b):

    #a = data_none
    a_f = np.array(a/a.sum()*100, dtype=int)
    #b = data_control
    b_f = np.array(b/b.sum()*100, dtype=int)
    if a_f.sum()>b_f.sum(): #due to changing to int some decimals dissapear, I equate by randomly summing the missing unit to a category
        idx = np.random.randint(b_f.shape[0])
        b_f[idx] = b_f[idx] + np.abs(a_f.sum()-b_f.sum())
    else:
        idx = np.random.randint(a_f.shape[0])
        a_f[idx] = a_f[idx] + np.abs(a_f.sum()-b_f.sum())

    idx = b_f==0
    if idx.sum()>0:
        b_f[idx] = b_f[idx] + 1 #expected freq. can't be 0 in the chi-square test
        for i in range(idx.sum()): #to level up the total sum, I randomly sum the missing unit in the other category
            idxx = np.random.randint(a_f.shape[0])
            a_f[idxx] = a_f[idxx] + 1
    
    return a_f, b_f

def my_group_chi_comparisons (data_none, data_control, data_exfarc, data_migrants):
    a = data_none
    b = data_control
    a,b = my_correction (a,b)
    c1 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('none_control', c1)

    a = data_none
    b = data_exfarc
    a,b = my_correction (a,b)
    c2 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('none_exfarc', c2)

    a = data_none
    b = data_migrants
    a,b = my_correction (a,b)
    c3 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('none_migrants', c3)

    a = data_control
    b = data_exfarc
    a,b = my_correction (a,b)
    c4 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('control_exfarc', c4)

    a = data_control
    b = data_migrants
    a,b = my_correction (a,b)
    c5 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('control_migrants', c5)

    a = data_exfarc
    b = data_migrants
    a,b = my_correction (a,b)
    c6 = scipy.stats.chisquare(f_obs = a, f_exp = b)
    print('exfarc_migrants', c6)
    
    return c1, c2, c3, c4, c5, c6


def my_stars(table1, table1_idx, data_none, data_control, data_exfarc, 
             data_migrants, none_control, none_exf, none_migr, control_exf, control_migr, ex_f_migr):
    str_temp = ""
    if none_control[1]<0.05:
        str_temp = str_temp+"*"
    elif none_exf[1]<0.05:
        str_temp = str_temp+"*"
    elif none_migr[1]<0.05:
        str_temp = str_temp+"*" 
    table1.loc[table1_idx,'none'] = str(list(data_none)) + str_temp
    str_temp = ""
    if control_exf[1]<0.05:
        str_temp = str_temp+"*"
    elif control_migr[1]<0.05:
        str_temp = str_temp+"*"
    table1.loc[table1_idx,'control video'] = str(list(data_control)) + str_temp
    str_temp = ""
    if ex_f_migr[1]<0.05:
        str_temp = str_temp+"*"
    table1.loc[table1_idx,'exfarc video'] = str(list(data_exfarc)) + str_temp
    table1.loc[table1_idx,'migrant video'] = str(list(data_migrants)) 
    return table1