from sil_examiner import get_list_energy_duration
from pydub import AudioSegment
import numpy as np
import pickle
import time
import sys
import scipy.io.wavfile as wavfile
from shutil import copy
with open("D:\speech_recognition\Tang_Shuran/sorted_labeling.data","r") as f:
    audio_list=f.readlines()[1:]
dic_path_energy_label_duration={}
prefix="D:\speech_recognition\Tang_Shuran/"
dic_path_error={}
for i,line in enumerate(audio_list):
    path=prefix+line.strip()
    try:
        energy,duration,channel=get_list_energy_duration(path)
        dic_path_energy_label_duration[path]=(energy,duration,channel)
        print i,"ok"
    except:
        e = sys.exc_info()[0]
        dic_path_error[path]=e
        print i,"error"
       # raise
    print "time:",time.clock()

pickle.dump((dic_path_energy_label_duration,dic_path_error), open( "dic_unlabelled_path_energy_duration_channel.p", "wb" ))
######################################
dic_path_energy_label_duration=pickle.load(open("dic_unlabelled_path_energy_duration_channel.p","rb"))[0]

def sil_check1(el,threshold=16.5,endurance=2):
    #endurance=0.2*len(el)
    exceeds=len([x for x in el if x >= threshold])
    return exceeds<=endurance
def sil_check2(el,threshold=14.4):
    endurance=0.2*len(el)
    if len(el[0])==len(el[1]):
        exceeds=len([x for x in np.vstack(el).T if x[0] >= threshold and x[1] >= threshold])
    elif len(el[0])>len(el[1]):
        temp=el[0][:len(el[1])]
        exceeds=len([x for x in np.vstack([temp,el[1]]).T if x[0] >= threshold and x[1] >= threshold])
    else:
        temp=el[1][:len(el[0])]
        exceeds=len([x for x in np.vstack([temp,el[0]]).T if x[0] >= threshold and x[1] >= threshold])
    return exceeds<=endurance

silence_file_path_list1=[]
silence_file_path_list2=[]
for audio in dic_path_energy_label_duration.items():
    if audio[1][2]==1:
        if sil_check1(audio[1][0]) == True:
            silence_file_path_list1.append(audio[0])
    if audio[1][2]==2:
        if sil_check2(audio[1][0]) == True:
            silence_file_path_list2.append(audio[0])
print len(silence_file_path_list1)
print len(silence_file_path_list2)
########################silence_file_path_list is when threshold == 16, 14.2
dst="D:\speech_recognition\Tang_Shuran\speech_classifier\listen"
interest=set(silence_file_path_list1+silence_file_path_list2)-set(silence_file_path_list)
for f in interest:
    copy(f,dst)

silence_file_path_list=silence_file_path_list1+silence_file_path_list2
result=[x+"; Silence\n" for x in silence_file_path_list]
with open("auto_labelled_silence_result","w") as f:
    f.writelines(result)
with open(r"D:\speech_recognition\backup\2016.11.15/sorted_labeling.data","r") as f:
    audio_list=f.readlines()
for line in result:
    try:
        audio_list.remove(line.replace('D:\\speech_recognition\\Tang_Shuran/',"").replace("; Silence",""))
    except:
        print line
with open("D:\speech_recognition\Tang_Shuran/sorted_labeling.data","w") as f:
    f.writelines(audio_list)