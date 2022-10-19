def printing(v):
	print (v, 'has a type', type(v))

def my_var():
	my_int = 42
	my_str = '42'
	my_str2 = 'quarante-deux'
	my_float = 42.0
	my_bool = True
	my_list = [42]
	my_dict = {42: 42}
	my_tuple = (42)
	my_set = set()

	printing(my_int)
	printing(my_str)
	printing(my_str2)
	printing(my_float)
	printing(my_bool)
	printing(my_list)
	printing(my_dict)
	printing(my_tuple)
	printing(my_set)

if __name__ == '__main__':
	my_var()