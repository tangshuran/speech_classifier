from sil_examiner import get_list_energy_duration
from pydub import AudioSegment
import numpy as np
import pickle
import time
import sys
import scipy.io.wavfile as wavfile
with open("D:\speech_recognition\Tang_Shuran/LabelingResult","r") as f:
    audio_list=f.readlines()
dic_path_energy_label_duration={}
prefix="D:\speech_recognition\Tang_Shuran/"
dic_path_error={}
for i,line in enumerate(audio_list):
    path=prefix+line.split(";")[0]
    label=line.split(";")[1].strip()
    if label !="Too Short" and label !="Error File":
        try:
            energy,duration,channel=get_list_energy_duration(path)
            dic_path_energy_label_duration[path]=(energy,label,duration,channel)
            print i,"ok"
        except:
            e = sys.exc_info()[0]
            dic_path_error[path]=e
            print i,"error"
            raise
    print "time:",time.clock()

pickle.dump((dic_path_energy_label_duration,dic_path_error), open( "dic_path_energy_label_duration.p", "wb" ) )
#path="D:\speech_recognition\Tang_Shuran/DATA/HCI/20110112afk/1569.7287767078662-1570.208773896512.mp3"
#1572
dic_path_energy_label_duration=pickle.load(open("dic_path_energy_label_duration.p","rb"))[0]
one_channel_file_list=[x[0] for x in dic_path_energy_label_duration.items() if x[1][3]==1]
two_channel_file_list=[x[0] for x in dic_path_energy_label_duration.items() if x[1][3]==2]
one_speech_list=[]
one_silence_list=[]
two_speech_list=[]
two_silence_list=[]
for one in dic_path_energy_label_duration.items():
    energy_list=one[1][0]
    #energy_list=energy_list[~np.isinf(energy_list)]
    label=one[1][1]
    channel=one[1][3]
    if channel==1:
        if label=="Silence":
            one_silence_list.append(energy_list)
        elif label== "Clean Speech":
            one_speech_list.append(energy_list)
    else:
        if label=="Silence":
            two_silence_list.append(energy_list)
        elif label== "Clean Speech":
            two_speech_list.append(energy_list)
################################################################from list to energy
#####channel one
one_silence_mean_list=[np.mean(x) for x in one_silence_list]
one_silence_energy=np.concatenate(one_silence_list)
one_speech_energy=np.concatenate(one_speech_list)
one_low_silence_list=[x for x in one_silence_list if np.mean(x)<np.percentile(one_silence_mean_list,70)]
low_silence_energy=np.concatenate(one_low_silence_list)
print np.mean(low_silence_energy), np.std(low_silence_energy)
#11.2314209027 2.36652871967
print np.mean(one_speech_energy),np.std(one_speech_energy)

    #if float('-inf') < float(energy_list) < float('inf'):
    #    energy_mean_list.append(energy_mean)
############# examine threshold
def sil_check1(el,threshold=17.5,endurance=2):
    #endurance=0.2*len(el)
    exceeds=len([x for x in el if x >= threshold])
    return exceeds<=endurance
result1=[sil_check1(x) for x in one_low_silence_list]
#precision 850/1022.0,  0.8317025440313112
true_silence_rate=sum(result1)/float(len(result1))
print true_silence_rate
result2=[sil_check1(x) for x in one_silence_list]
print sum(result2)/float(len(result2))
result3=[sil_check1(x) for x in one_speech_list]
false_silence_rate=sum(result3)/float(len(result3))
print false_silence_rate
######################################################################
##channel two
two_channel_silence_file_list=[x[0] for x in dic_path_energy_label_duration.items() if x[1][3]==2 and x[1][1]=='Silence']
two_channel_speech_file_list=[x[0] for x in dic_path_energy_label_duration.items() if x[1][3]==2 and x[1][1]=='Clean Speech']
two_silence_mean_list1=[np.mean(x) for x in np.array(two_silence_list)[:,0]]
two_silence_mean_list2=[np.mean(x) for x in np.array(two_silence_list)[:,1]]
two_silence_energy1=np.concatenate(np.array(two_silence_list)[:,0])
two_silence_energy2=np.concatenate(np.array(two_silence_list)[:,1])
two_speech_energy1=np.concatenate(np.array(two_speech_list)[:,0])
two_speech_energy2=np.concatenate(np.array(two_speech_list)[:,1])
two_low_silence_list=[x for x in two_silence_list if np.mean(x[0])<np.percentile(two_silence_mean_list1,85) and np.mean(x[1])<np.percentile(two_silence_mean_list2,85)]
low_silence_energy1=np.concatenate(np.array(two_low_silence_list)[:,0])
low_silence_energy2=np.concatenate(np.array(two_low_silence_list)[:,1])
print np.mean(low_silence_energy1), np.std(low_silence_energy1)
print np.mean(low_silence_energy2), np.std(low_silence_energy2)
print np.mean(two_speech_energy1),np.std(two_speech_energy1)
print np.mean(two_speech_energy2),np.std(two_speech_energy2)
#13.3308091389 1.78757819686
#12.9915765054 1.6697739794
#17.7411736208 2.94098267287
#17.5364260052 2.94342267382
    #if float('-inf') < float(energy_list) < float('inf'):
    #    energy_mean_list.append(energy_mean)
############# examine threshold
def sil_check2(el,threshold=15):
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
result1=[sil_check2(x) for x in two_low_silence_list]
true_silence_rate=sum(result1)/float(len(result1))
print true_silence_rate
result2=[sil_check2(x) for x in two_silence_list]
print sum(result2)/float(len(result2))
# clean two_speech_list
result3=[sil_check2(x) for x in two_speech_list]
false_silence_rate=sum(result3)/float(len(result3))
print false_silence_rate


#############this part is used to find the error files path
#error_index_list=[i[0] for i in enumerate(result3) if i[1]==True]
#error_energy_list=[speech_list[x] for x in error_index_list]
#error_file_list=[]
#for one in dic_path_energy_label_duration.items():
#    for energy in error_energy_list:
#        if np.array_equal(one[1][0],energy):
#            error_file_list.append(one[0])
            

#temp.export("temp.wav",format="wav")
#rate, error_data= wavfile.read("temp.wav")
speech_file_list=[x.split(";")[0] for x in audio_list if x.split(";")[1]=="Clean Speech\n"]
speech_file_list=["D:\speech_recognition\Tang_Shuran/"+x for x in speech_file_list]
right_file_list=list(set(speech_file_list)-set(error_file_list))
error_file_channels=[]
for ef in error_file_list:
    temp= AudioSegment.from_mp3(ef)
    error_file_channels.append(temp.channels)
right_file_channels=[]
for ef in right_file_list:
    temp= AudioSegment.from_mp3(ef)
    right_file_channels.append(temp.channels)
right_energy_list=[]
for one in dic_path_energy_label_duration.items():
    if one[0] in right_file_list:
        energy_list=one[1][0]
        energy_list=energy_list[~np.isinf(energy_list)]
        right_energy_list.append(energy_list)
def sil_check(el,threshold=19,endurance=3):
    #endurance=0.2*len(el)
    exceeds=len([x for x in el if x >= threshold])
    return exceeds<=endurance
result4=[sil_check(x) for x in right_energy_list]
false_positive_rate=sum(result4)/float(len(result4))
print false_positive_rate

