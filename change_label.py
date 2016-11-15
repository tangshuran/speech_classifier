old_label=" Noise Other Speech"
new_label=" Too Short"
with open("LabelingResult","r") as f:
    labels=f.readlines()
with open("./python/shorter_0.35.txt","r") as f:
    need_change=f.readlines()
changed=[]
for j,a in enumerate(need_change):
    b=a.strip("\n")
    for i,line in enumerate(labels):
        if b in line:
            labels[i]=line.strip(" Noise Other Speech\n")+new_label+"\n"
            changed.append(j)
            break
with open("LabelingResult","w") as f:
    f.writelines(labels)