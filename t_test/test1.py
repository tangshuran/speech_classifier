import csv
import pandas as pd
import random
import pickle
import numpy as np
import math
original_path=r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/new_output_m1.csv"
data_list=[]
with open(original_path,"rb") as f:
    data=csv.reader(f)
    for row in data:
        data_list.append(row)
#data1=pd.read_csv(original_path)

#grouped=data1.groupby(["person","iteraction"])
new_data_list=[]
for entry in data_list:
    if entry[2][-1]=="i":
        entry[2]=entry[2][:-1]
    elif entry[2][-1].isdigit():
        entry[2]=entry[2][:-2]
    new_data_list.append(entry)
#make list into dataframe
data1=pd.DataFrame(new_data_list)
data1.columns = data1.iloc[0]
data1.reindex(data1.index.drop(0))
grouped=data1.groupby(["person","iteraction"])
#len(grouped.groups.keys())
test_data=[["person","sample_size","HCI_mean","HCI_variance","HHI_mean_list","HHI_variance_list"]]
person_list=[]
for k in grouped.groups.keys():
    person_list.append(k[0])
#get rid of unique name
person_set=set([x for x in person_list if person_list.count(x) > 1])
HHI_random_times=30
for p in person_set:
    HCI_group=grouped.get_group((p, 'HCI'))
    HHI_group=grouped.get_group((p, 'HHI'))
    size=min(len(HCI_group),len(HHI_group))
    HHI_mean_list=[]
    HHI_variance_list=[]
    for i in range(HHI_random_times):
        HHI_group_sample= HHI_group.ix[random.sample(HHI_group.index,size)]
        HHI_group_sample_features=HHI_group_sample.ix[:,5:993].astype(float)
        HHI_mean=list(HHI_group_sample_features.mean(axis=0))
        HHI_var=list(HHI_group_sample_features.var(axis=0))
        HHI_mean_list.append(HHI_mean)
        HHI_variance_list.append(HHI_var)
    HCI_group_features=HCI_group.ix[:,5:993].astype(float)
    HCI_mean=list(HCI_group_features.mean(axis=0))
    HCI_var=list(HCI_group_features.var(axis=0))
    test_data.append([p,size,HCI_mean,HCI_var,HHI_mean_list,HHI_variance_list])

pickle.dump(test_data, open( "new_mean_and_var_each_person.p", "wb" ))

#test_data=pickle.load(open( "new_mean_and_var_each_person.p", "rb" ))

#perform Welch's t-test
from scipy import stats
#test_data_array=np.array(test_data)
#print stats.t.ppf(1-0.025, 68)
test_result=[["person","sample_size","t","significant_different","effekt_staerke"]]
for each_person in test_data[1:]:
    degree_of_freedom=each_person[1]-1
    t_result=[]
    significant_different_result=[]
    effekt_staerke_result=[]
    for i in range(HHI_random_times):
        t_list=[]
        significant_different_list=[]
        effekt_staerke_list=[]
        for j in range(988):
            t=(each_person[2][j]-each_person[4][i][j])*(degree_of_freedom**0.5)/((each_person[3][j]+each_person[5][i][j])**0.5)
            effekt_staerke=abs(each_person[2][j]-each_person[4][i][j])/(((each_person[3][j]+each_person[5][i][j])/2)**0.5)
            #if math.isnan(effekt_staerke):
            #    raise
            t_table_value=stats.t.ppf(1-0.025, degree_of_freedom)
            t_list.append(t)
            effekt_staerke_list.append(effekt_staerke)
            if abs(t)<abs(t_table_value):
                significant_different_list.append(False)
            else:
                significant_different_list.append(True)
        t_result.append(t_list)
        significant_different_result.append(significant_different_list)
        effekt_staerke_result.append(effekt_staerke_list)
    result=[each_person[0],each_person[1],t_result,significant_different_result,effekt_staerke_result]
    test_result.append(result)

#e=29
#for k in range(10):
#    print len([i for i in test_result[e][3][k] if i ==True])
    
pickle.dump(test_result, open( "test_result.p", "wb" ))

##calculate statistical power for each test
#x_bar=0+
#t_95threshold=stats.t.ppf(1-0.025,test_data[1][1])*test_data[1][1]/((test_data[1][3][j]+test_data[1][5][i][j])**0.5)
#i=0
#effektstaerke=(test_data[1][2][1]-test_data[1][4][i][1])/(((test_data[1][3][1]+test_data[1][5][i][1])/2)**0.5)
for kk in range(1,55):
    ef=test_result[kk][4]
    mean_list=[]
    for i in ef:
        mean_list.append(np.mean([j for j in i if not np.isnan(j)]))
    print np.mean(mean_list)
