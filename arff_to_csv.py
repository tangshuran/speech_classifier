import gc
import re
from datetime import datetime
import sys
gc.enable()
origin_features=open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output1.arff","r").readlines()
labels=open("D:\speech_recognition\Tang_Shuran/LabelingResult","r").readlines()
features_list=[]
for i1,line1 in enumerate(origin_features):
    if i1<=994 and "@attribute" in line1:
        feature_name=line1.strip("@attribute ").rsplit(" ",1)[0]
        features_list.append(feature_name)
    elif i1>995:
        break
    else:
        pass
features_list.append("label")
del features_list[0]
features_list=["iteraction","date","person","file_time"]+features_list
features_name=",".join(features_list)
data_csv=[]
data_csv.append(features_name)

def separate_name(feat_line):
    feat_list=feat_line.strip("\n").split(",")
    name=feat_list[0]
    info=name.strip("'").strip(".wav").replace("\\",",")
    info=info[:12]+","+info[12:]
    feat_list[0]=info
    return ",".join(feat_list)

def audit_after_sep(line):
    feat_list=line.split(",")
    if len(feat_list)!=994:
        print ','.join(feat_list[:4])," length is not correct."
        raise
    string_index=[0,2,3,993]
    date_index=[1]
    #float_index=range(4,993)
    for i,feat in enumerate(feat_list):
        if i in string_index:
            if type(feat)!=str:
                print ','.join(feat_list[:4])," string type is not correct."
                raise
        elif i in date_index:
            try:
                datetime.strptime(feat , '%Y%m%d')
            except:
                print ','.join(feat_list[:4])," date type is not correct: ",sys.exc_info()[0]
                raise
        else:
            try:
                float(feat)
            except:
                print ','.join(feat_list[:4])," float type is not correct: ", sys.exc_info()[0]
                raise
    return True

def find_label(feat_line):
    name=feat_line.strip("\n").split(",")[0].strip("'").strip(".wav")
    name=name.replace("\\","/")
    this_label="Not Labelled"
    found=False
    this_label_index=None
    for i,line in enumerate(labels):
        found=re.search(name,line)
        if found:
            this_label=line.split(";")[1].strip()
            this_label_index=i
            break
    return this_label,this_label_index

def shape_element(separated_line,label):
    return separated_line+","+label

for i,ob in enumerate(origin_features[996:]):
    print "processing: ",i+996
    element=separate_name(ob)
    if audit_after_sep(element):
        label,label_index=find_label(ob)
        print "audited, and the label is ", label," index: ",label_index
        element=shape_element(element,label)
        data_csv.append(element)

with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output.csv","a") as new_output:
    for f in data_csv:
        new_output.write(f+"\n")

#for i2,line2 in enumerate(origin_features):
#    if i2>=996:
#        file_path=line2.split(",")[0]
#        line2=line2.strip(file_path).strip(",")
#        file_path=file_path.replace("\\","/").strip("'").strip(".wav")
#        found=False
#        for line3 in labels:
#            found=re.search(file_path,line3)
#            if found:
#                label=line3.split(";")[1].strip()
#                break
#            else:
#                pass
#        info=file_path.replace("/",",")
#        info=info[:12]+","+info[12:]
#        if found:
#            line2=info+","+line2.strip()+","+label+"\n"
#        else:
#            line2=info+","+line2.strip()+","+"Not Labelled"+"\n"
#        f_num=len(line2.split(","))
#        if f_num==995:
#            with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output.csv","a") as new_output:
#                new_output.write(line2)
#        else:
#            raise Exception('error!')
#        print i2,"     "+file_path,"     "+str(f_num)+"    "+str(found)

################
#for i2,line2 in enumerate(origin_features):
#    if i2==2251:
#        file_path=line2.split(",")[0]
#        file_path=file_path.replace("\\","/").strip("'").strip(".wav")
#        break
#for line3 in labels:
#    found=re.search(file_path,line3)
#    if found:
#        label=line3.split(";")[1].strip()
#        break
#    else:
#        pass
#print file_path,found


