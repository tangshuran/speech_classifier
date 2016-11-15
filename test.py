import pickle
import operator
dicts=pickle.load(open("dic_path_duration.p","rb"))
sorted_duration=sorted(dicts[0].items(), key=operator.itemgetter(1))
for i, f in enumerate(sorted_duration):
    if f[1]>0.35:
        print i
        break
duration_list=[]
for f in sorted_duration:
    duration_list.append(f[1])
sum(duration_list[60000:])
