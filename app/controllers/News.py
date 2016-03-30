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
        
        return self.load_view("template_" + str(paper['style']) + ".html", paper = paper)

    def new(self):
        return self.load_view("new.html")

    def create(self):
        data = {
            "email": request.form['email'],
            "first_name": request.form['first_name'],
            "last-name": request.form['last_name'],
            "city": request.form['city']
        }

        reg = self.models['NewsModel'].create_user(data)

        if reg['status'] == False:
            for error in errors:
                flash(error)
            return redirect('/new')

        session['user_id'] = reg['user']['id']
        session['user_paper'] = reg['user']['paper_id']
        session['name'] = reg['user']['first_name'] + " " + reg['user']['last_name']

        return redirect("/paper/" + str(reg['city_id']) +"/dashboard/" + str(session[user_id]))

    def login(self):
        data = {
            "email": request.form['email']
            "password:" request.form['pword']
        }

        log = self.models['NewsModel'].log_user

        if log['status'] == False:
            flash("Incorrect information.")
            return redirect('/log_page')

        session['user_id'] = log['user']['id']
        session['user_paper'] = log['user']['paper_id']
        session['name'] = log['user']['first_name'] + " " + log['user']['last_name']

        return redirect("/" + str(log['user']['city_id']) + "/dashboard/" + str(session[user_id]))

    def log_page(self):
        return self.load_view("log_page.html")






'''
        









    def register(self):
        return self.load_view('register.html')

    def registering(self):
        user_info = {
            "email": request.form['email'],
            "first_name": request.form['fname'],
            "last_name": request.form['lname'],
            "password": request.form['pword'],
            "pw_confirm": request.form['cword']
            }

        reg = self.models['DashboardModel'].create_user(user_info)

        if reg['status'] == True:
            session['id'] = reg['user']['id']
            session['name'] = reg['user']['first_name'] + " " + reg['user']['last_name']
            session['level'] = reg['user']['user_level']
        
            if session['level'] == 'admin':
                flash('The first-ever user is an admin! Go try some stuff.')
            return redirect('/dashboard/admin')
        else:
            for error in reg['errors']:
                flash(error)
            return redirect('/register')

    def login(self):
        return self.load_view('signin.html')

    def loggingin(self):
        user_info = {
            "email": request.form['email'],
            "password": request.form['pword']
        }

        log = self.models['DashboardModel'].login_user(user_info)

        if log['status'] == True:
            session['id'] = log['user']['id']
            session['name'] = log['user']['first_name']
            session['level'] = log['user']['user_level']

            if session['level'] == 'admin':
                return redirect('/dashboard/admin')
            else:
                return redirect('/dashboard')
        else:
            flash(log['error'])
            return redirect('/signin')

    def dash(self):
        users = self.models['DashboardModel'].get_all_users()
        return self.load_view('dashbaord.html', users = users)

    def admindash(self):
        users = self.models['DashboardModel'].get_all_users()
        return self.load_view('admindashboard.html', users = users)

    def new(self):
        return self.load_view('new.html')

    def add(self):
        user_info = {
            "email": request.form['email'],
            "first_name": request.form['fname'],
            "last_name": request.form['lname'],
            "password": request.form['pword'],
            "pw_confirm": request.form['cword']
            }
        print user_info
        add = self.models['DashboardModel'].create_user(user_info)

        if add["status"] == True:
            flash ("Successfully added another beautiful user.")
            if session['level'] == 'admin':
                return redirect ('/dashboard/admin')
            else:
                return redirect ('/dashboard')
        else:
            for error in add['errors']:
                flash(error)
            return redirect('/users/new')

    def show(self, id):
        user_id = id 
        user_info = {
            "id": user_id 
        }
        user = self.models['DashboardModel'].get_user(user_info)
        wall = self.models['DashboardModel'].access_wall(user_info)
        user = self.models['DashboardModel'].get_user(user_info)
        if wall['status'] == False:
            wall = self.models['DashboardModel'].create_wall(user)
        print "this is"
        print wall
        print "WALLLLL!"
        wall_data = {
            "id": wall['wall']['id']
        }
        print wall_data 
        comments = self.models['DashboardModel'].render_comments(wall_data)
        print comments
        page_replies = {}
        for x in comments:
             y = {'id': x['id']} 
             page_replies[x['id']] = self.models['DashboardModel'].render_replies(y)
      
        return self.load_view("show.html",user = user, comments = comments, page_replies = page_replies)

    def edit(self, id):
        user_info = {
            "id":id
        }


        user = self.models['DashboardModel'].get_user(user_info)
        return self.load_view("edit.html", user = user)

    def edit_user_info(self):
        user_info = {
            "email": request.form['email'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "user_level": request.form['user_level'],
            "id": request.form['id']
            }
        print user_info

        done = self.models['DashboardModel'].admin_edit_info(user_info)
        return redirect('/dashboard/admin')

    def comment(self):
        wall_data = {
            'id': request.form['user_id']
        }
        wall = self.models['DashboardModel'].access_wall(wall_data)
        data = {
            "content": request.form['comment'],
            "wall_id": wall['wall']['id'], 
            "user_id": session['id']
        }

        self.models['DashboardModel'].create_comment(data)
        return redirect('/users/show/' + request.form['user_id'])


    def reply(self):
        print request.form
        data = {
            "reply": request.form['reply'],
            "comments_id": request.form['comment_id'],
            "user_id": session['id']
        }

        self.models['DashboardModel'].create_reply(data)
        return redirect('/users/show/' + request.form['user_id'])











        product = {'id': id}
        prod = self.models['SemirestModel'].get_product(product)
        return self.load_view('show.html', product = prod)

    def edit(self,id):
        product = {'id': id}
        prod = self.models['SemirestModel'].get_product(product)
        return self.load_view('edit.html', product = prod)

    def update(self,id):
        product = {'id': id, 'name': request.form['name'], 'description':request.form['description'], 'price':request.form['price']}
        self.models['SemirestModel'].update_product(product)
        return redirect('/')

    def destroy(self, id):
        session['id'] = id
        return self.load_view('destroy.html')

    def remove(self, id):
        product = {'id': id}
        prod = self.models['SemirestModel'].get_product(product)
        self.models['CourseModel'].remove_product(prod[0])
        return redirect('/products')
'''



