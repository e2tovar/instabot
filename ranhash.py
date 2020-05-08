import pandas as pd
import os
import sys


#read data
my_file = os.path.join(sys.path[0], "hashtag.xlsx")
hasht = pd.read_excel(my_file, usecols=[1,2,3])
#divide
rang1 = hasht.iloc[:,0].dropna()
rang2 = hasht.iloc[:,1].dropna()
rang3 = hasht.iloc[:,2].dropna()

lista = (rang1.sample(14).tolist() + rang2.sample(10).tolist() + rang3.sample(5).tolist())
lista.append("#idiliodigital")
print(lista)

with open('your_file.txt', 'w') as f:
    f.truncate(0)
    for item in lista:
        f.write("%s\n" % item)