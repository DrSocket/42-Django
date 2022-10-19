def numbers():
	o_file = open('./numbers.txt', 'r')
	r_file = o_file.read()
	nb_list = r_file.strip().split(',')
	for nb in nb_list:
		print (nb)

if __name__ == '__main__':
	numbers()