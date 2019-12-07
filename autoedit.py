import json
dog = open('dog.txt','r').read()
print(dog)
print(type(dog))
df_file = open("datafiles.json","r+")
df = json.load(df_file)
df["пес"] = dog
json.dump(df,df_file)