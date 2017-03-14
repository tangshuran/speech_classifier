import pickle
import numpy as np
#import test1

test_result=pickle.load(open("test_result.p", "rb" ))
#select features
new_test_result=[["person","sample_size","t","significant_different","effekt_staerke","significant_score"]]
for each in test_result[1:]:
    significant_score_result=[]
    A=np.array(each[3])
    B=np.array(each[4])
    for i in range(988):
        significant_score=[]
        for j in range(30):
            if not np.isnan(B[j,i]):
                temp=A[j,i]*B[j,i]
                significant_score.append(temp)
        significant_score_result.append(sum(significant_score))
    each.append(significant_score_result)
    new_test_result.append(each)

"""
oo=[]
for each in test_result[1:]:
    B=np.array(each[4])
    for i in range(988):
        for j in range(30):
            if type(B[j,i])!=np.float64:
                oo.append(B[j,i])
"""
significant_score_all=[]
for each in new_test_result[1:]:
    significant_score_all.append(each[5])
significant_score_array=np.array(significant_score_all)
score_list=np.mean(significant_score_array,axis=0)


#import matplotlib.pyplot as plt

#plt.hist(score_list, bins=100)


sorted_features=sorted(score_list)
sorted_features_index=[i[0] for i in sorted(enumerate(score_list), key=lambda x:x[1])]
selected_features_index=sorted_features_index[-701:-1]

import csv

with open("shape_arff1.arff","rb") as template:
    tem=template.readlines()
new_tem=[]
new_selected_features_index=[0,1,2]+[x+3 for x in selected_features_index]
for i,t in enumerate(tem):
    if i in new_selected_features_index:
        new_tem.append(t)
new_tem=new_tem+tem[-3:]
original_path=r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/new_output_m1.csv"
features_list=[]
with open(original_path,"rb") as f:
    data=csv.reader(f)
    for i,row in enumerate(data):
        if i >0 and row[2] in "tkoi":
            features=row[5:-2]
            new_row=[str(i-1)]
            for j,feature in enumerate(features):
                if j in selected_features_index:
                    new_row.append(feature)
            string_row=",".join(new_row)+","+row[0]+"\r\n"
            features_list.append(string_row)
with open("tttt.arff","wb") as tttt:
    for line in new_tem+features_list:
        tttt.write(line)