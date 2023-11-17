



opt_file = open('./includes.inc', 'r')

opt = opt_file.read()

opt_file.close()

opt = opt.split('\n')

opt = [x for x in opt if x != '']

appjs = open('./app.js', 'w')

appjs.writelines("// compiled by compiler.py\n\n")

for i in opt:
	file = open('./' + i, 'r')
	appjs.write(file.read())
	file.close()
	appjs.write('// end of ' + i + '\n\n')

appjs.close()
print('Done!')