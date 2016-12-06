import os
import subprocess
import gc
import fnmatch
import sys
import pickle
#os.system(r'''D:\github\modules\openSMILE-2.1.0\bin\Win32\SMILExtract_Release.exe -C "D:\github\modules\openSMILE-2.1.0\bin\Win32\config\emobase.conf" -logfile "D:\github\modules\openSMILE-2.1.0\bin\Win32\smile.log" -I "D:\github\modules\openSMILE-2.1.0\bin\Win32\data\temp1.wav" -O "D:\speech_recognition\Tang_Shuran\speech_classifier\features\test\output.arff" -l 1''')
#subprocess.call(r'''D:\github\modules\openSMILE-2.1.0\bin\Win32\SMILExtract_Release.exe 
#-C "D:\github\modules\openSMILE-2.1.0\bin\Win32\config\emobase.conf" 
#-logfile "D:\github\modules\openSMILE-2.1.0\bin\Win32\smile.log" 
#-I "D:\github\modules\openSMILE-2.1.0\bin\Win32\data\temp1.wav" 
#-O "D:\speech_recognition\Tang_Shuran\speech_classifier\features\test\output.arff" 
#-l 1''',creationflags=0x08000000)
##########################################
#gc.enable()
#directories=os.walk(r"D:\speech_recognition\Tang_Shuran\speech_classifier\Tang_Shuran_WAV")
#exe=r'''D:\github\modules\openSMILE-2.1.0\bin\Win32\SMILExtract_Release.exe'''
#config=r'''"D:\github\modules\openSMILE-2.1.0\bin\Win32\config\emobase.conf"'''
#log=r'''"D:\github\modules\openSMILE-2.1.0\bin\Win32\smile.log"'''
#output_path=r'''"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff"'''
#processed=0
#for direct in directories:
#    if direct[2]!=[]:
#        name=direct[0].split("\\")[-1]
#        interaction=direct[0].split("\\")[-2]
#        for f in direct[2]:
#            input_path='''"'''+direct[0]+"\\"+f+'''"'''
#            run=exe+" -C "+config+" -logfile "+log+" -I "+input_path+" -O "+output_path+" -l 1"
#            subprocess.call(run,creationflags=0x08000000)
#            with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff","r") as temp_output:
#                temp=temp_output.readlines()
#            os.remove(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff")
#            feature_list=temp[-1].split(",")
#            if len(feature_list) ==991:                
#                feature_list[0]="'"+interaction+"\\"+name+"\\"+f+"'"
#            temp_features=",".join(feature_list)
#            with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output1.arff","a") as output:
#                output.write(temp_features)
#            processed +=1
#            print processed

#file_paths=[]
#src=os.walk(r"D:\speech_recognition\Tang_Shuran\speech_classifier\Tang_Shuran_WAV")
#i=0
#for root, dirnames, filenames in src:
#    if filenames!=[]:
#        for filename in fnmatch.filter(filenames, '*.wav'):
#            file_paths.append(os.path.join(root, filename))
#            i+=1
#            print i
#pickle.dump(file_paths, open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/file_paths.p", "wb"))

file_paths=pickle.load( open( r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/file_paths.p", "rb" ) )
def extract_from_file(input_path):
    exe=r'''D:\github\modules\openSMILE-2.1.0\bin\Win32\SMILExtract_Release.exe'''
    config=r'''"D:\github\modules\openSMILE-2.1.0\bin\Win32\config\emobase.conf"'''
    log=r'''"D:\github\modules\openSMILE-2.1.0\bin\Win32\smile.log"'''
    output_path=r'''"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff"'''
    new_input_path='''"'''+input_path+'''"'''
    run=exe+" -C "+config+" -logfile "+log+" -I "+new_input_path+" -O "+output_path+" -l 1"
    subprocess.call(run,creationflags=0x08000000)
    with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff","r") as temp_output:
        temp=temp_output.readlines()
    os.remove(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features\temp.arff")
    feature_list=temp[-1].split(",")
    input_path_split=input_path.split("\\")
    file_name=input_path_split[-1]
    date=input_path_split[-2][:8]
    person=input_path_split[-2][8:]
    interaction=input_path_split[-3]
    #feature_list[0]=interaction+","+date+","+person+","+file_name
    feature_list[0]="'"+interaction+"\\"+date+person+"\\"+file_name+"'"
    return ",".join(feature_list).strip()
#num_of_features=991
def audit_feature(features):
    feature_list=features.split(",")
    if len(feature_list)!=991:
        print feature_list[0],"length is not correct."
        raise
    if type(feature_list[990])==str and type(feature_list[0])==str:
        for i,feat in enumerate(feature_list[1:889]):
            try:
                float(feat)
            except:
                print i," of ",feature_list[0]," is not float:", sys.exc_info()[0]
                raise
    else:
        print feature_list[990]," or ",feature_list[0]," is not string"
        raise
    return True


extraction_fails=r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/extraction_fails.txt"
for i,f in enumerate(file_paths):
    print "processing ",i," ",f
    f_feat=extract_from_file(f)
    if len(f_feat.split(","))==1:
        with open(extraction_fails,"a") as fails:
            fails.write(f+"\n")
        continue
    if audit_feature(f_feat):
        with open(r"D:\speech_recognition\Tang_Shuran\speech_classifier\features/output1.arff","a") as out:
            out.write(f_feat+"\n")