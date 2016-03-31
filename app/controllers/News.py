from system.core.controller import *
from collections import defaultdict
import time

class News(Controller):
    def __init__(self, action):
        super(News, self).__init__(action)
        self.load_model('NewsModel')
    
    def index(self):
        return self.load_view('index.html')

    def search(self):
        info = {'name': request.form['search']} 
        result = self.models['NewsModel'].search(info)
        if result["results"] == True:
            if len(result["cities"]) < 1:
                flash("No search results found. Try typing your query again.") 
            else:
                session['results'] = result["cities"]

            return redirect("/results")

        return redirect('/paper/' + str(result["city"]['id']))

    def results(self):
        return self.load_view("results.html", results = session['results'])

    def city_page(self, id):
        data = {"id": id}
        city = self.models['NewsModel'].get_city(data)
        data["name"] = city["name"] 

        paper = self.models['NewsModel'].render_paper(data)
        data["paper_id"] = paper['id']
        articles = self.models['NewsModel'].get_articles(data)

        if articles['status'] == False:
            flash('No articles for this city... yet')
            return self.load_view("template_" + str(paper['style']) + ".html", paper = paper)
        
        return self.load_view("template_" + str(paper['style']) + ".html", paper = paper, articles = articles['article_list'])

    def new(self):
        return self.load_view("new.html")

    def create(self):
        data = {
            "email": request.form['email'],
            "first_name": request.form['fname'],
            "last_name": request.form['lname'],
            "city": request.form['city'],
            "zipcode": request.form['zipcode']
            "dob": request.form['dob'],
            "password": request.form['pword'],
            "pw_confirm": request.form['cword']
        }

        print request.form['email']
        print data 
        reg = self.models['NewsModel'].create_user(data)

        if reg['status'] == False:
            for error in reg['errors']:
                flash(error)
            return redirect('/new')

        session['user_id'] = reg['user']['user_id']
        session['user_paper'] = reg['user']['paper_id']
        session['name'] = reg['user']['first_name'] + " " + reg['user']['last_name']

        return redirect("/dashboard/" + str(reg['city_id']) + "_" + str(session['user_id']))

    def login(self):
        data = {
            "email": request.form['email'],
            "password": request.form['pword']
        }

        log = self.models['NewsModel'].log_user

        if log['status'] == False:
            flash("Incorrect information.")
            return redirect('/log_page')

        session['user_id'] = log['user']['id']
        session['user_paper'] = log['user']['paper_id']
        session['name'] = log['user']['first_name'] + " " + log['user']['last_name']

        return redirect("/dashboard/" + str(log['user']['city_id']) + "_" + str(session['user_id']))

    def log_page(self):
        return self.load_view("log_page.html")

    def dashboard(self, double_id):
        info = double_id.split('_')
        data = {
            "city_id": info[0],
            "user_id": info[1]
        }

        print data
        return self.load_view('register.html')









