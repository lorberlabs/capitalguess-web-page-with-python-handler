import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class Country():
    name = ""
    capital = ""

    def __init__(self, name, capital):
        self.name = name
        self.capital = capital

def GetData():

    slovenia = Country("Slovenije", "Ljubljana")
    croatia = Country("Hrvaske", "Zagreb")
    austria = Country("Avstrije", "Dunaj")
    italy = Country("Italije", "Rim")
    germany = Country("Nemcije", "Berlin")

    countries = [slovenia, croatia, austria]

    return countries

class MainHandler(BaseHandler):
    def get(self):

        countries = GetData()
        country = countries[random.randint(0, len(countries) - 1)]

        params = {"capital": country.name}

        return self.render_template("index.html", params=params)

    def post(self):
        guess = self.request.get("guess")
        country = self.request.get("country")
        isCorrect = False

        countries = GetData()

        for i in countries:
            if i.name == country:
                if guess == i.capital:
                    isCorrect = True

        country = countries[random.randint(0, len(countries) - 1)]
        params = {"correct": isCorrect, "capital": country.name}

        return self.render_template("index.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)