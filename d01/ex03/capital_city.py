import sys

def find_state_capital(arg):
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
	res = capital_cities.get(states.get(arg))
	if res == None:
		return ("Unknown state")
	return (res)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		print (find_state_capital(sys.argv[1]))