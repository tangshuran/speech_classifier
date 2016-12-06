import gc
import re
gc.enable()
origin_features=open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output.arff")
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
features_name=",".join(features_list)+"\n"
with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output.csv","w") as new_output:
    new_output.write(features_name)
for i2,line2 in enumerate(origin_features):
    if i2>=996:
        file_path=line2.split(",")[0]
        line2=line2.strip(file_path).strip(",")
        file_path=file_path.replace("\\","/").strip("'").strip(".wav")
        found=False
        for line3 in labels:
            found=re.search(file_path,line3)
            if found:
                label=line3.split(";")[1].strip()
                break
            else:
                pass
        info=file_path.replace("/",",")
        info=info[:12]+","+info[12:]
        if found:
            line2=info+","+line2.strip()+","+label+"\n"
        else:
            line2=info+","+line2.strip()+","+"Not Labelled"+"\n"
        f_num=len(line2.split(","))
        if f_num==995:
            with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output.csv","a") as new_output:
                new_output.write(line2)
        else:
            raise Exception('error!')
        print i2,"     "+file_path,"     "+str(f_num)+"    "+str(found)

################
for i2,line2 in enumerate(origin_features):
    if i2==2251:
        file_path=line2.split(",")[0]
        file_path=file_path.replace("\\","/").strip("'").strip(".wav")
        break
for line3 in labels:
    found=re.search(file_path,line3)
    if found:
        label=line3.split(";")[1].strip()
        break
    else:
        pass
print file_path,found