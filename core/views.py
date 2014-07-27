import logging
import json
from django.template.loader import get_template
from django.template.context import Context

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

logger = logging.getLogger('andreffs.' + __name__)

class BlogView(TemplateView):
	template_name = "blog/blog.html"

	def get_context_data(self, **kwargs):
		context = super(BlogView, self).get_context_data(**kwargs)


		article = { "title" : "Something about something", 
					"slug" : "12/08/2013/something-about-something/",	
					"date" : "12 August 2013, 13h30",
					"body" : "I work swell, i sd jasldk njasoidkl jasdk asmdshad the luck to become a internshipjjjjjjjjjjjjjjjjjjjjjjjj on the first Portugues Startup to enter in YCombinator.. Unbabel! The just make a way for machine translation and a human have a baby and awesome text birth fromave a baby and awesome text birth fromave a baby and awesome text birth from it's windows",
					"comments" : "12",
					"categories" : ["aha", "beads", "hasd", "ajsd"] 
					} 

		entries = []
		for i in range(10):
			entries.append(article)

		context["tags"] = ["aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "ajsd"]
		context["recent_posts"] = [" asdljksa dlksja dlskasdasdasdas ds ds adajd lsakj daslkjd ossidasdsae", "somthing nice to say to ppl", "hellow owrlds"]

		paginator = Paginator(entries, 2)
		page = self.request.GET.get('page')
		try:
			order_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			order_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			order_list = paginator.page(paginator.num_pages)

		context["entries"] =  order_list
		return context


class BlogDetailView(TemplateView):
	template_name = "blog/blog-detail.html"

	def get_context_data(self, **kwargs):
		context = super(BlogDetailView, self).get_context_data(**kwargs)


		article = { "title" : "Something about something", 
					"slug" : "12/08/2013/something-about-something/",	
					"date" : "12 August 2013, 13h30",
					"body" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of \"de Finibus Bonorum et Malorum\" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, \"Lorem ipsum dolor sit amet..\", comes from a line in section 1.10.32.The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from \"de Finibus Bonorum et Malorum\" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.",
					"comments" : "12",
					"timereading" : "4",
					"categories" : ["aha", "beads", "hasd", "ajsd"] 
					} 

		comments  = [{
			"date" : "August 12, 2013",
			"hour" : "4:15 PM",
			"author" : "anonymous",
			"e-mail" : "none@asd.com",
			"message" : "ajksdflajsnk dasdkjasldk asn dkasndklasndnlsdsalk ds dksj kdaj"
		},{
			"date" : "August 12, 2013",
			"hour" : "4:15 PM",
			"author" : "anonymous",
			"e-mail" : "none@asd.com",
			"message" : "ajksdflajsnk dasdkjasldk asn dkasndklasndnlsdsalk ds dksj kdaj"
		},{
			"date" : "August 12, 2013",
			"hour" : "4:15 PM",
			"author" : "anonymous",
			"e-mail" : "none@asd.com",
			"message" : "ajksdflajsnk dasdkjasldk asn dkasndklasndnlsdsalk ds dksj kdaj"
		},{
			"date" : "August 12, 2013",
			"hour" : "4:15 PM",
			"author" : "anonymous",
			"e-mail" : "none@asd.com",
			"message" : "ajksdflajsnk dasdkjasldk asn dkasndklasndnlsdsalk ds dksj kdaj"
		}]


		context["entry"] = article
		context["comments"] = comments

		context["tags"] = ["aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "ajsd"]
		context["recent_posts"] = [" asdljksa dlksja dlskasdasdasdas ds ds adajd lsakj daslkjd ossidasdsae", "somthing nice to say to ppl", "hellow owrlds"]


 		return context

class ProjectsView(TemplateView):
	template_name = "projects.html"

	def get_context_data(self, **kwargs):
		context = super(ProjectsView, self).get_context_data(**kwargs)

		projects = []
		for i in range(20):
			projects.append({ "img" : "../static/img/workshowreel/img%s.jpg" % ((i%3) +1), "title": "Title %s" % (i), "subtitle": "asnd kja hls dk"})

		context["projects"] = projects
		
		return context



class AdminView(TemplateView, FormView):
	template_name = "admin/admin.html"

	def get_context_data(self, **kwargs):
		context = super(AdminView, self).get_context_data(**kwargs)


		article = { "title" : "Something about something", 
			"slug" : "12/08/2013/something-about-something/",	
			"date" : "12 August 2013, 13h30",
			"body" : "I work swell, i sd jasldk njasoidkl jasdk asmdshad the luck to become a internshipjjjjjjjjjjjjjjjjjjjjjjjj on the first Portugues Startup to enter in YCombinator.. Unbabel! The just make a way for machine translation and a human have a baby and awesome text birth fromave a baby and awesome text birth fromave a baby and awesome text birth from it's windows",
			"comments" : "12",
			"time" : "3",
			"categories" : ["aha", "beads", "hasd", "ajsd"] 
			} 

		entries = []
		for i in range(10):
			entries.append(article)
		context['articles'] = entries
		return context
