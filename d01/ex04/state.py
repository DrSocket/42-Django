import sys

def get_k_from_v(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return 'Unknown capital city'

def find_state(arg):
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
	ret = get_k_from_v(states, get_k_from_v(capital_cities, arg))
	return ret

if __name__ == "__main__":
	if len(sys.argv) == 2:
		print (find_state(sys.argv[1]))