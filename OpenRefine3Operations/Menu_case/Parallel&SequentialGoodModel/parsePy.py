import json

with open('Menu_caseJsonfile.json','rb')as f:
    data=json.load(f)

newlist=sorted(data,key=lambda k:k['columnName'])
with open('newJson.json','w')as f:
    f.writelines(json.dumps(newlist))




