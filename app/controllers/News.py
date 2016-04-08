from system.core.controller import *
from collections import defaultdict
import time
import os
from werkzeug import secure_filename


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
        
        return self.load_view("template_" + str(paper['style']) + ".html", paper = paper, articles = articles['article_list'])

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
            "pw_confirm": request.form['cword']
        }

        print request.form['email']
        print data 
        reg = self.models['NewsModel'].create_user(data)

        if reg['status'] == False:
            for error in reg['errors']:
                flash(error)
            return redirect('/new')
        
       
        file = request.files['image']
        print file 

        session['user_id'] = reg['user']['user_id']
        session['user_paper'] = reg['user']['paper_id']
        session['name'] = reg['user']['first_name'] + " " + reg['user']['last_name']

        if not file:
            info = {"url": '/static/default.png'}
        else:
            x = (os.path.dirname('/users/philipcheek/Desktop/news_collab/app/static/uploads'))
            print x 
            filename = secure_filename(file.filename)
            file.save(os.path.join(x + "/uploads", filename))
            info = {'url': "/static/uploads/" + filename}
        
        session['url'] = info['url']
        print session['url']
        info['user_id'] = session['user_id']
        self.models['NewsModel'].upload_image(info)

        return redirect("/dashboard/" + str(reg['city_id']) + "_" + str(session['user_id']))

    def login(self):
        data = {
            "email": request.form['email'],
            "password": request.form['pword']
        }

        log = self.models['NewsModel'].log_user(data)

        if log['status'] == False:
            flash("Incorrect information.")
            return redirect('/log_page')

        print log
        print log['user']
        session['user_id'] = log['user']['user_id']
        session['user_paper'] = log['user']['paper_id']
        session['name'] = log['user']['first_name'] + " " + log['user']['last_name']
        session['url'] = log['user']['url']

        return redirect("/dashboard/" + str(log['user']['city_id']) + "_" + str(session['user_id']))

    def log_page(self):
        return self.load_view("log_page.html")

    def dashboard(self, double_id):
        info = double_id.split('_')

        data = {"id": info[0]}
        paper = self.models['NewsModel'].render_paper(data)

        print session
        print session['user_id']
        data = {"id": session['user_id']}
        user = self.models['NewsModel'].get_user(data)
        print user

        data = {"paper_id": paper['id']}
        data['id'] = info[0]
        paper = self.models['NewsModel'].render_paper(data)
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
        articles = render_articles(info)
        return render_template(write.html, i_category = initial_c, full_category = full_category)

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

















