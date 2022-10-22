from django.shortcuts import render, HttpResponse, redirect
from django.views import View
import random
from django.conf import settings

class Index(View):
	index_page = "ex/index.html"

	def get(self, request):
		# if request.COOKIES.get('')


		# random_name = random.choice(settings.USER_NAMES)
		return render(request, self.index_page)