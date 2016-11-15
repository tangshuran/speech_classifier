from sil_examiner import get_list_energy_duration
from pydub import AudioSegment
import numpy as np
import pickle
import time
import sys
import scipy.io.wavfile as wavfile
dic_path_energy_label_duration=pickle.load(open("dic_path_energy_label_duration.p","rb"))[0]
def sil_check2(el,threshold=13.5):
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
def sil_check1(el,threshold=15.5,endurance=2):
    #endurance=0.2*len(el)
    exceeds=len([x for x in el if x >= threshold])
    return exceeds<=endurance
total_result_list=[]
silence_file_path_list=[]
for audio in dic_path_energy_label_duration.items():
    if audio[1][3]==1:
        if sil_check1(audio[1][0]) == True:
            silence_file_path_list.append(audio[0])
            if audio[1][1]=='Silence':
                total_result_list.append("true positive")
            else:
                total_result_list.append("false positive")
        else:
            if audio[1][1]=='Silence':
                total_result_list.append("false nagetive")
            else:
                total_result_list.append("true nagetive")
    if audio[1][3]==2:
        if sil_check2(audio[1][0]) == True:
            silence_file_path_list.append(audio[0])
            if audio[1][1]=='Silence':
                total_result_list.append("true positive")
            else:
                total_result_list.append("false positive")
        else:
            if audio[1][1]=='Silence':
                total_result_list.append("false nagetive")
            else:
                total_result_list.append("true nagetive")
for x in ["true positive","false positive","false nagetive","true nagetive"]:
    print x,total_result_list.count(x)
with open("predicted_silence.data","w") as f:
    f.writelines(silence_file_path_list)