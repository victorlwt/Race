import torch

x = torch.eye(3)
y = torch.tensor([1, 2, 3], dtype=torch.float)
print(x, y)
print(x * y)
print(len(x))



