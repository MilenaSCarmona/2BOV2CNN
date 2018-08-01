from os import listdir, mkdir, makedirs
from os.path import isdir
from shutil import copy
from random import shuffle

def mk(dir):
	try:
		mkdir(dir, 777)
	except:
		pass

sets = [['train', []], ['validation', []], ['test', []]]

dataset = 'BOV2C2V/'
for class_ in listdir(dataset):
	images = listdir(dataset + class_)
	shuffle(images)
	l = float(len(images))
	train_l = int(l * .64)
	val_l = int(l * .16)
	test_l = int(l * .2)
	init, end = None, train_l
	sets[0][1].append([class_, images[init:end]])
	init, end = train_l, train_l + val_l
	sets[1][1].append([class_, images[init:end]])
	init, end = train_l + val_l, None
	sets[2][1].append([class_, images[init:end]])

for set in sets:
	set_name = set[0]
	for class_ in set[1]:
		class_name = class_[0]
		dir = dataset + class_name + '/'
		new_dir = 'data/' + set_name + '/' + class_name + '/'
		makedirs(new_dir)
		for image_name in class_[1]:
			original = dir + image_name
			new = new_dir + image_name
			copy(original, new)

	#print len(set[1][0][0]),set[1][0][0]
	#print len(set[1][0][1])

