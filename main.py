#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


def CvF(x):
   return x * 1.8 + 32

def FvC(x):
   return (x - 32) / 1.8

def KMvM(x):
   return x / 1.609347

def MvKM(x):
   return x * 1.609347

def KMHvMS(x):
   return x / 3.6

def MSVKMH(x):
   return x * 3.6


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")
    def post(self):
        vnos = self.request.get("Vnos")
        pretvorba = self.request.get("pretvorbaVnos")
        vnos = vnos.strip(' ')
        vnos = float(vnos)
        if pretvorba == "CvF":
            zapis = CvF(vnos)
        elif pretvorba == "FvC":
            zapis = FvC(vnos)
        elif pretvorba == "KMvM":
            zapis = KMvM(vnos)
        elif pretvorba == "MvKM":
            zapis = MvKM(vnos)
        elif pretvorba == "KMHvMS":
            zapis = KMHvMS(vnos)
        elif pretvorba == "MSVKMH":
            zapis = MSVKMH(vnos)
        else:
            zapis = "Napaka!"

        podatki = {"rezultat":zapis }
        return self.render_template("pretvornik.html", podatki)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)