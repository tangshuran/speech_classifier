from pydub import AudioSegment
import os
import wave
import struct
import audioBasicIO
import audioFeatureExtraction
import matplotlib.pyplot as plt
import audioBasicIO as aIO
cwd=os.getcwd()
os.chdir(cwd)
audio= AudioSegment.from_mp3("42.80787899706809-53.111849871339004.mp3")
duration=audio.duration_seconds
count=audio.frame_count()
rate=audio.frame_rate
audio.export("first.wav",format="wav")
wav=wave.open("first.wav","r")
frame_number=wav.getnframes()
print float.fromhex("c8")
frames=wav.readframes(frame_number-1)
sample_frame=wav.readframes(1)
frame_amplitute=struct.unpack("h",sample_frame)[0]
print frame_amplitute
print struct.pack("h",-175)
import scipy.io.wavfile as wavfile
rate1, data1= wavfile.read("first.wav")
rate2, data2= wavfile.read("toms.wav")
###########################################
[Fs, x] = audioBasicIO.readAudioFile("first.wav")
window_lenth=0.050*Fs
step_length=0.025*Fs
F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs)
features_number=len(F)
windows_number=len(F[0])
import audioSegmentation as aS
[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("first.wav", "D:\github\modules\pyAudioAnalysis\data/svmSM", "svm", True,"first.segments")
######################### silence removal
[Fs, x] = aIO.readAudioFile("mixture.wav")
segments = aS.silenceRemoval(x, Fs, 0.020, 0.020, smoothWindow = 1.0, Weight = 0.3, plot = True)
