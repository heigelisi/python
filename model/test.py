from model import Model

model1 = Model()
data = model1.table('test').select()
print(data)
print(model1)


model2 = Model()
data2 = model1.table('session').select()
print(data2)
print(model2)