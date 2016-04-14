from system.core.controller import *
from collections import defaultdict
import time
import os
from werkzeug import secure_filename
from flask import jsonify


class News(Controller):
    def __init__(self, action):
        super(News, self).__init__(action)
        self.load_model('NewsModel')
        self.load_model('UserModel')
    
    def index(self):
        if 'user_id' not in session:
            return self.load_view('index.html')
        return redirect('/dashboard/' + str(session['paper_id']) + "_" + str(session['user_id']))

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
        info = {}
        results = {}
        for x in session['results']:
            info['id'] = x['id']
            info['name'] = x['name']
            city = self.models['NewsModel'].render_full_city(info)
            results[", ".join([city['city_name'], city['country_name']])] = self.models['NewsModel'].render_paper(info)
            print results
        return self.load_view("results.html", results = results)

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
        
        return self.load_view("template_" + str(paper['style']) + ".html", paper = paper, articles = articles['article_list'], city = city)

    def new(self):
        return self.load_view("new.html")

    def create(self):
        data = {
            "email": request.form['email'],
            "first_name": request.form['fname'],
            "last_name": request.form['lname'],
            "city": request.form['city'],
            "zip_code": request.form['zipcode'],
            "dob": request.form['dob'],
            "password": request.form['pword'],
            "pw_confirm": request.form['cword'],
            "file": request.files['image']
        }

        reg = self.models['UserModel'].create_user(data)

        if reg['status'] == False:
            for error in reg['errors']:
                flash(error)
            return redirect('/new')
        

        session['user_id'] = reg['user']['user_id']
        session['paper_id'] = reg['user']['paper_id']
        session['name'] = reg['user']['first_name'] + " " + reg['user']['last_name']
        session['url'] = reg['user']['url']

        return redirect("/dashboard/" + str(session['paper_id']) + "_" + str(session['user_id']))

    def login(self):
        data = {
            "email": request.form['email'],
            "password": request.form['pword']
        }

        log = self.models['UserModel'].log_user(data)

        if log['status'] == False:
            flash("Incorrect information.")
            return redirect('/log_page')

        session['user_id'] = log['user']['user_id']
        session['paper_id'] = log['user']['paper_id']
        session['name'] = log['user']['first_name'] + " " + log['user']['last_name']
        session['url'] = log['user']['url']

        return redirect("/dashboard/" + str(log['user']['paper_id']) + "_" + str(session['user_id']))

    def log_page(self):
        return self.load_view("log_page.html")

    def dashboard(self, double_id):
        data = {
            "paper_id": session['paper_id'],
            "user_id": session['user_id']
        }

        paper = self.models['NewsModel'].get_paper(data)
        user = self.models['NewsModel'].get_user(data)
        articles = self.models['NewsModel'].render_articles(data)
        editors = self.models['NewsModel'].render_editors(data)

        articles = self.models['NewsModel'].render_articles(data)

        return self.load_view('dashboard.html', user = user, articles = articles)

    def new_art(self):
        init_c = request.form['category'][0]
        return redirect('dashboard/write/' + init_c)

    def write_new(self, init_c):
        initial_c = init_c
        full_category = {
            "n": "news",
            "o": "opinion",
            "s": "sports",
            "b": "business",
            "c": "classifieds",
            "e": "entertainment"
        }

        info = {'paper_id': session['paper_id']}
        paper = self.models['NewsModel'].get_paper(info)
        articles = self.models['NewsModel'].render_articles(info)
        return self.load_view('write.html', i_category = initial_c, full_category = full_category, paper = paper)

    def write_submit(self):
        info = {
            'title': request.form['title'],
            'paper_id': session['paper_id'],
            'author_id': session['user_id'],
            'category': request.form['category'],
            'content': request.form['content']
        }

        data = {"info": session['user_id']}
        user = self.models['NewsModel'].get_user(data)

        return redirect("/dashboard/" + str(user['city_id']) + "_" + str(session['user_id']))


    def logout(self):
        session.clear()
        return redirect("/")

    def user(self, id):
        data = {"id": id}
        user = self.models['NewsModel'].get_user(data)

        data['table'] = 'papers'
        data['where'] = 'author_id'
        data['data'] = user['id']
        paper = self.models['NewsModel'].get_table_flex(data)

        data['table'] = 'articles'
        articles = self.models['NewsModel'].get_table_flex(data)

        data['table'] = 'edits'
        edits = self.models['NewsModel'].get_table_flex(data)

        return self.load_view('user.html', user = user, paper = paper[0], articles = articles[0], edits = edits[0])

    def vote(self):
        info = {"article_id": request.args.get('id')}
        if request.args.get('vote') == True:
            self.model['NewsModel'].up_vote_article(info)
        else:
            self.model['NewsModel'].down_vote_article(info)
            
        return None















