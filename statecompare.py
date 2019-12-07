import json
df_file = open("datafiles.json","r")
df = json.load(df_file)
df_values = []
for x in df.values():
	df_values.append(x.split('&'))
differences = []
for i in range(min(len(df_values[0]),len(df_values[1]))):
	for j in range(min(len(df_values[0][i]),len(df_values[1][i]))):
		if df_values[0][i][j] != df_values[1][i][j]:
			result = str(i) + "," + str(j) +"  "+df_values[0][i][j]+"  "+df_values[1][i][j]
			print(result)
			differences.append(result)
print(str(len(df_values[0])))
print(str(len(differences)))