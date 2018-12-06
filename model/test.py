from model import Model


model = Model()
data = model.table('test').field('').fetchSQL(1).group('account').order('id desc,account').select()
for d in data:
	print(d)