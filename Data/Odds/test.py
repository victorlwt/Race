import pickle as pk
with open("20190714_odd.dfdl","rb") as f:
	x = pk.load(f)
	print(x[0])