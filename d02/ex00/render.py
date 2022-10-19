#!/usr/bin/env python3
import os
import sys
import re
import settings

def get_module_vars(module_name):
	module = globals().get(module_name, None)
	dict = {}
	if module:
		dict = {key: value for key, value in module.__dict__.items() if not (key.startswith('__') or key.startswith('_'))}
	return dict

def main():
	if (len(sys.argv) != 2):
		return print("wrong argument count")
	path = sys.argv[1]
	regex = re.compile(".*\.template")
	if not regex.match(path):
		return print("wrong extension, (required: .template)")
	if not os.path.isfile(path):
		return print(f"({path}) does not exist...")
	f = open(path, "r")
	template = "".join(f.readlines())
	f.close()
	vars = get_module_vars('settings')
	for k, v in vars.items():
		template = template.replace('{'+k+'}', str(v))

	regex = re.compile("(\.template)")
	path = path[0:regex.search(path).start()] + ".html"
	f = open(path, "w")
	f.write(template)
	f.close()

if __name__ == '__main__':
	main()