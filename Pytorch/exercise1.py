import pandas as pd

df = pd.read_csv('data.csv');
df = df.drop(df.columns[0], axis=1)
d = df[df.columns[9]]
new_d = []
for i in d:
    if i<4:
        new_d.append(1)
    else:
        new_d.append(0)
df[df.columns[9]] = new_d
print df