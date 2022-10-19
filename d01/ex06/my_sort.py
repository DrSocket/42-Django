def mysort():
	d = {
		'Hendrix' : '1942',
		'Allman' : '1946',
		'King' : '1925',
		'Clapton' : '1945',
		'Johnson' : '1911',
		'Berry' : '1926',
		'Vaughan' : '1954',
		'Cooder' : '1947',
		'Page' : '1944',
		'Richards' : '1943',
		'Hammett' : '1962',
		'Cobain' : '1967',
		'Garcia' : '1942',
		'Beck' : '1944',
		'Santana' : '1947',
		'Ramone' : '1948',
		'White' : '1975',
		'Frusciante': '1970',
		'Thompson' : '1949',
		'Burton' : '1939',
		}
	my_d = dict(sorted(d.items(), key=lambda item: item[1]))
	print ("Ascending order:\n")
	last = ""
	for i in my_d.items():
		print (i[0])
	same_years = []
	i = 0
	for val in my_d.items():
		if last != val[1]:
			same_years.append([val[0]])
			i+=1
		elif last == val[1]:
			same_years[i-1].append(val[0])
		last = val[1]
	print ("\nYear + alphabetic order:\n")
	for l in same_years:
		if len(l) > 1:
			l = sorted(l)
		for i in l:
			print (i)

if __name__ == "__main__":
	mysort()