import json

f=open('data.txt','r')
lines=list(f)
# get the position of the start and end
start_position=lines.index('pastEntryCount=7\n')+1
end_position=lines.index('futureEntryCount=0\n')

prejson=lines[start_position:end_position]
prejsonformal=[]

# formalize the dicts
for jsonpart in prejson:
    d=json.loads(jsonpart)
    prejsonformal.append(d)

# generate json file
with open('Datajsonformal.json','wt')as f:
    json.dump(prejsonformal,f,indent=2)
