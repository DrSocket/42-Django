from django.views import View
from django.shortcuts import render
import random

class Ex00(View):
	template = 'ex00/display.html'

	def ret(self, request):
		random_name = random.choice(['dada', 'toto', 'lala'])
		return render(request, self.template, {'random_name': random_name})