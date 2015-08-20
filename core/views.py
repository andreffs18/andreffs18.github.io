#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView, View

import json

class HomepageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomepageView, self).get_context_data(**kwargs)

        ctx['cv'] = [
            {'employment': [
                {
                    'period': 'June 2013 - Present',
                    'place': "<a href='https://www.unbabel.com/' target='_blank'>Unbabel</a><br/>@Lisboa, Portugal",
                    'description': 'Used to be Backend Engineer, also did a little of Android Development.<br>Currently, Software Engineer. Platforms used: Django, MongoDB, Heroku.'
                },
                {
                    'period': 'June 2010 - August 2011',
                    'place': "<a href='http://vitopal.pt/' target='_blank'>Vitopal Informatica Lda</a><br/>@Samora Correia, Portugal",
                    'description': 'IT Technician (Software and Hardware).<br>Setting up Servers and Networks in Windows Server 2008.<br>Management and Administration.'
                }
            ]},
            {'education': [
                {
                    'period': 'September 2012 - Present',
                    'place': "<a href='http://tecnico.ulisboa.pt/' target='_blank'>Instituto Superior Tecnico</a><br/>@Lisboa, Portugal",
                    'description': '<a href="https://fenix.tecnico.ulisboa.pt/cursos/leic-a" target="_blank">Information Systems and Computer Science Engineering</a><br>'
                },
                {
                    'period': 'September 2008 - June 2012',
                    'place': "<a href='#'>Escola Secund&aacute;ria de Benavente</a><br/>@Benavente, Portugal",
                    'description': 'Curso Prof. de Tecnico de Gest&atilde;o e Programa&ccedil;&atilde;o de Sistemas Inform&aacute;ticos,'
                },
            ]},
            {'experience': [
                {
                    'period': 'Contests',
                    'place': '',
                    'description': 'Codebits 2012/2013<br>SINFO 2014 and 2015'
                },
                {
                    'period': 'Workshops',
                    'place': '',
                    'description': 'SINFO XXI'
                }
            ]},
            {'skills': [
                {
                    'period': 'Languages',
                    'place': '',
                    'description': 'Django, CSS3, LESS, Javascript, HTML5, C, C++, C#, Java. HTML, CSS, JS and experience with popular frameworks for each language including LESS, jQuery. Experience with SVN and Git and Extensive experience developing responsive sites and prototyping.'
                },
                {
                    'period': 'Software',
                    'place': '',
                    'description': 'Using PyCharm on daily basis.<br>Like to play around with Adobe After Effects.'
                }
            ]},
            {'interests': [
                {
                    'period': '',
                    'place': '',
                    'description': 'Gym, Self Defense, Surf, TvShows (lots of them) and Cooking. (not ordered)'
                }
            ]},
        ]

        return ctx


class AboutpageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        ctx = super(AboutpageView, self).get_context_data(**kwargs)
        return ctx


class WorkpageView(TemplateView):
    template_name = "work.html"

    def get_context_data(self, **kwargs):
        ctx = super(WorkpageView, self).get_context_data(**kwargs)
        return ctx