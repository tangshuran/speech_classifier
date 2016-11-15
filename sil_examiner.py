from pydub import AudioSegment
import scipy.io.wavfile as wavfile
import numpy as np
def get_energy(data):
    return np.log(sum([x**2 for x in data]))
    
def sil_examine(file_path,window_size=0.025,step=0.025,threshold=16,endurance=3):
    temp= AudioSegment.from_mp3(file_path)
    temp.export("temp.wav",format="wav")
    rate, data= wavfile.read("temp.wav")
    frames_num=rate*window_size
    steps_num=rate*step
    windows_num=int((len(data)-frames_num)/float(steps_num))+1
    energy_list=[]
    for i in range(windows_num):
        window=data[i*steps_num:i*steps_num+frames_num]
        energy_list.append(get_energy(window))
    energy_list=np.array(energy_list)
    energy_list=energy_list[~np.isnan(energy_list)]
    exceeds=len([x for x in energy_list if x >= threshold])
    return (exceeds<=endurance,energy_list)

def get_list_energy_duration(file_path,window_size=0.025,step=0.025):
    temp= AudioSegment.from_mp3(file_path)
    temp.export("temp.wav",format="wav")
    rate, data= wavfile.read("temp.wav")
    duration=len(data)/float(rate)
    frames_num=rate*window_size
    steps_num=rate*step
    windows_num=int((len(data)-frames_num)/float(steps_num))+1
    if temp.channels==1:
        energy_list=[]
        for i in range(windows_num):
            window=data[int(i*steps_num):int(i*steps_num+frames_num)]
            energy_list.append(get_energy(window))
        energy_list=np.array(energy_list)
        energy_list=energy_list[~np.isnan(energy_list)]
        return energy_list,duration,temp.channels
    else:
        energy_list1=[]
        energy_list2=[]
        for i in range(windows_num):
            window=data[int(i*steps_num):int(i*steps_num+frames_num)]
            window1=window[:,0]
            window2=window[:,1]
            energy_list1.append(get_energy(window1))
            energy_list2.append(get_energy(window2))
        energy_list1=np.array(energy_list1)
        energy_list1=energy_list1[~np.isnan(energy_list1)]
        energy_list2=np.array(energy_list2)
        energy_list2=energy_list2[~np.isnan(energy_list2)]
        return [energy_list1,energy_list2],duration,temp.channels


############################
#print np.mean(energy_list1),np.std(energy_list1)
#print np.mean(energy_list2),np.std(energy_list2)
