import sys

def parse(lines):
	elems = []
	d = {}
	for line in lines:
		elems.append([item.strip() for item in line.split('=')])
	for data in elems:
		d[data[0]] = ([item.strip().split(':') for item in data[1].split(',')])
	return d

def build():
	site = '''<!DOCTYPE html>
<html lang='en'>
<head>
	<meta charset='UTF-8'>
	<meta name='viewport' content='width=device-width, initial-scale=1.0'>
	<title>My Awesome Periodic Table</title>
	<style>
	table{
		border-collapse: collapse;
	}
	h4 {
		text-align: center;
	}
	ul {
		list-style:none;
		padding-left:0px;
	}
	td {
		box-sizing: border-box;
	}
	</style>
</head>
<body>
	<table>
%s
	</table>
</body>
</html>
'''
	T_DATA_EMPTY = "<td></td>"
	T_DATA = '''
			<td style="border: 1px solid black;padding: 10px">
				<h4>%s</h4>
				<ul>
					<li>%s</li>
					<li><strong>%s</strong></li>
					<li>%s <strong>m</strong></li>
					<li style="border: 0.5px solid black;">%s <strong>electron</strong></li>
				</ul>
			</td>'''
	f = open('periodic_table.txt', 'r')
	periodic_table = parse(f.readlines())
	f.close()
	doc = open('periodic_table.html', 'w')
	pos = -1
	tables = "\t\t<tr>"
	for k, v in periodic_table.items():
		pos+=1
		while int(v[0][1]) != pos:
			tables += T_DATA_EMPTY
			pos+=1
		if int(v[0][1]) == pos:
			tables += T_DATA % (k, v[1][1], v[2][1], v[3][1], v[4][1])
		if pos == 17:
			tables += "\n\t\t</tr>"
			if int(v[1][1]) < 118:
				tables += "\n\t\t<tr>"
			pos = -1
	site = site % tables
	doc.write(site)
	doc.close()

if __name__ == "__main__":
	build()