from system.core.model import Model
from werkzeug import secure_filename
import random
import time
import os 
import re

class UserModel(Model):
    def __init__(self):
        super(NewsModel, self).__init__()

    def get_user(self, info):
    	data = [info['user_id']]
    	query = "SELECT * FROM users WHERE user_id = %s"
    	user = self.db.query_db(query, data)
    	return user[0]

    def get_articles(self, info):
    	data = [info['paper_id']]
    	query = "SELECT * FROM articles WHERE author_id = %S"
    	return self.db.query_db(query, data)

    def get_edits(self, info):
    	data = [info['user_id']]
    	query = "SELECT * FROM articles JOIN edits WHERE edits.user_id = %s"

            file = request.files['image']


    def create_user(self,info):
        EMAIL_REGEX=re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []


        if not info['first_name'] or not info['last_name']:
            errors.append('A name may not be blank')
        elif len(info['first_name']) < 3 or len(info['last_name']) < 3:
            errors.append('Your name must be longer than two characters')

        if not info['email']:
            errors.append('Email field may not be left blank.')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Submitted email is not valid.')

        data = [info['city']]
        query = "SELECT * FROM cities where name = %s"
        check = self.db.query_db(query, data)
        print check 
        if len(check) < 1:
            errors.append('We are sorry. We cannot locate your city in our database.')
        else: 
            paper_query = "SELECT *,papers.id as paper_id, cities.id as city_id FROM cities JOIN papers on papers.city_id = cities.id WHERE cities.id = %s"
            data = [check[0]['id']]

            paper_city = self.db.query_db(paper_query, data)
            print paper_city 
            print data 
            print paper_city

            if len(paper_city) < 1:
                title = "The " + info['city']
                gen_append = ["Enquirer", "Daily", "Times", "Journal", "Press", "Tribune", "Sun", "Star", "Gazette",
                        "Courier", "Record", "Post", "Sentinel", "Chronicle", "Informer", "Harbinger", "Ledger",
                        "Inquirer", "Inquisitor", "Mirror", "Monitor", "Review", "Outlook", "Pioneer", "Beacon",
                        "Bulletin", "Dispatch", "Herald", "Sun"]

                title += " " + gen_append[random.randint(0, len(gen_append) - 1)]
                style = random.randint(1,3)

                i_query = "INSERT INTO papers (name, style, city_id) VALUES (%s, %s, %s)" 
                i_data = [title, style, check[0]['id']]
                self.db.query_db(i_query, i_data)

                paper_city = self.db.query_db(paper_query, data)
                print paper_city 

            print paper_city
            p_id = paper_city[0]['paper_id']
            city_id = paper_city[0]['city_id']

        if not info['password']:
            errors.append('Password left blank.')
        elif len(info['password']) < 9:
            errors.append('Password must have more than eight characters.')
        elif info['password'] != info['pw_confirm']:
            errors.append('Passwords don\'t match.')

        if errors:
            return {'status': False, 'errors': errors}
        else:
            password = info['password']
            file = request.files['image']

            if not file:
            	url = '/static/default.png'
        	else:
            	path = (os.path.dirname('/users/philipcheek/Desktop/news_collab/app/static/uploads'))
            	filename = secure_filename(file.filename)
            	file.save(os.path.join(path + "/uploads", filename))
            	url =  "/static/uploads/" + filename

            pw_hash = self.bcrypt.generate_password_hash(password)
            i_query = "INSERT INTO users (first_name, last_name, email, dob, url, paper_id, zip_code, created_at, password) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)"
            i_data = [info['first_name'], info['last_name'], info['email'], info['dob'], url, p_id, info['zip_code'], pw_hash]
            self.db.query_db(i_query, i_data)
            
            g_query = "SELECT *,users.id as user_id FROM users JOIN papers on users.paper_id = papers.id ORDER BY users.id DESC LIMIT 1"
            users = self.db.query_db(g_query)
            users = self.db.query_db(g_query)
            return {"status": True, "user": users[0]}
