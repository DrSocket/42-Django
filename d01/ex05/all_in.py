import sys

def get_k_from_v(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

def print_all(arg):
	states = {
		"Oregon" : "OR", 
		"Alabama" : "AL",
		"New Jersey": "NJ",
		"Colorado" : "CO"
	}
	capital_cities = {
		"OR": "Salem",
		"AL": "Montgomery",
		"NJ": "Trenton",
		"CO": "Denver"
	}
	dictionary = dict(zip((v for v in capital_cities.values()), (k for k in states)))
	words = arg.split(',')
	for word in words:
		if word == '' or word.isspace():
			continue
		word = word.strip().title()
		if dictionary.get(word) != None:
			print (f'{word} is the capital of {dictionary.get(word)}')
		elif get_k_from_v(dictionary, word) != None:
			print (f'{get_k_from_v(dictionary, word)} is the capital of {word}')
		else:
			print (f'{word} is neither a capital city nor a state')

if __name__ == "__main__":
	if (len(sys.argv) == 2):
		print_all(sys.argv[1])