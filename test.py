import pickle as pk

with open('./Data/Odds/20190714_odd.dfdl', 'rb') as f:
    x = pk.load(f)

print(x)