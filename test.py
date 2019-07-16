import pickle as pk

f = open('./Data/Results/20190714_result.dfl', 'rb')
x = pk.load(f)
for df in x:
    print(df)



