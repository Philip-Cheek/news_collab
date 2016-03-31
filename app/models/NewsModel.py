from system.core.model import Model
import re
import random 

class NewsModel(Model):
    def __init__(self):
        super(NewsModel, self).__init__()

    def search(self, info):
        query = "SELECT * FROM cities WHERE name = %s"
        data = [info['name']]
        print info 
        cities = self.db.query_db(query, data)
        print cities 


        if len(cities) < 1:
            queryish = "SELECT * FROM cities WHERE name SOUNDS LIKE %s"
            candidates = self.db.query_db(queryish, data)
            return {"results": True, "cities" : candidates}
        elif len(cities) > 1:
            return {"results": True, "cities" : cities}
        else:
            return {"results": False, "city": cities[0]}
                
    def get_all_articles_auth(self, info):
        query = "SELECT *,aricles.id as article_id, users.id as orig_user_id FROM articles JOIN users ON articles.author_id = users.id JOIN WHERE articles.paper_id = %s"
        data = [info['paper_id']]
        return self.db.query_db(query, data)

    def get_city(self, info):
        query = "SELECT * FROM cities WHERE id = %s"
        data = [info['id']]
        city = self.db.query_db(query, data)
        return city[0]

    def render_paper(self, info):
        query = "SELECT * from papers WHERE city_id = %s" 
        data = [info['id']]
        paper = self.db.query_db(query, data)

        if len(paper) < 1:
            title = "The " + info['name']
            gen_append = ["Enquirer", "Daily", "Times", "Journal", "Press", "Tribune", "Sun", "Star", "Gazette",
                        "Courier", "Record", "Post", "Sentinel", "Chronicle", "Informer", "Harbinger", "Ledger",
                        "Inquirer", "Inquisitor", "Mirror", "Monitor", "Review", "Outlook", "Pioneer", "Beacon",
                        "Bulletin", "Dispatch", "Herald", "Sun"]

            title += " " + gen_append[random.randint(0, len(gen_append) - 1)]
            style = random.randint(1,3)

            i_query = "INSERT INTO papers (name, style, city_id) VALUES (%s, %s, %s)" 
            i_data = [title, style, info['id']]
            self.db.query_db(i_query, i_data)

            paper = self.db.query_db(query, data)

        return paper[0]

    def create_user(self, info):
        EMAIL_REGEX=re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []


        if not info['first_name'] or not info['last_name']:
            errors.append('A name may not be blank')
        elif len(info['first_name']) < 3 or len(info['last_name']) < 3:
            errors.append('Your name must be longer than two characters')

        if not info['email']:
            errors.append('Email field may not be left blank.')
        elif not EMAIL_REGEX.match(info['email']):
            error.append('Submitted email is not valid.')

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

                paper_city = self.db.query_db(query, data)

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

            pw_hash = self.bcrypt.generate_password_hash(password)
            i_query = "INSERT INTO users (first_name, last_name, email, dob, paper_id, created_at, password) VALUES (%s, %s, %s, %s, %s, NOW(), %s)"
            i_data = [info['first_name'], info['last_name'], info['email'], info['dob'], p_id, pw_hash]
            self.db.query_db(i_query, i_data)
            
            g_query = "SELECT *,users.id as user_id FROM users JOIN papers on users.paper_id = papers.id ORDER BY users.id DESC LIMIT 1"
            users = self.db.query_db(g_query)
            print "watch below"
            print users
            users = self.db.query_db(g_query)
            return {"status": True, "user": users[0], "city_id": city_id}

    def log_user(self, info):
        password = info['password']

        g_query = "SELECT * FROM users JOIN papers on papers.id = users.paper_id WHERE email = %s"
        data = [info['email']]
        users = self.db.query_db(g_query, data)

        if len(users) > 0:
            if self.bcrypt.check_password_hash(users[0]['password'], password):
                return {"status": True, "user": users[0]}

        return {"status": False}

    def city_paper(self, info):
        data = [info['name']]
        query = "SELECT *, papers.id as paper_id FROM cities JOIN papers ON papers.city_id = cities.id WHERE cities.name = %s"
        paper = self.db.query_db(query,data)

        if len(paper) < 1:
            return {"status": False}

        return {"status": True, "paper": paper[0]}

    def get_articles(self, info):
        data = [info['paper_id']]
        query = "SELECT *, articles.id as article_id FROM articles join papers on articles.paper_id = papers.id where papers.id = %s"
        articles = self.db.query_db(query,data)

        if len(articles) < 1:
            return{"status": False, "article_list": None}
        
        return {"status": True, "article_list": articles}





''''

    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.db.query_db(query)

    def create_user(self, info):
        EMAIL_REGEX=re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not info['first_name'] or not info['last_name']:
            errors.append('A name may not be blank')
        elif len(info['first_name']) < 2 or info['last_name'] < 2:
            errors.append('Your name must be longer than two characters')

        if not info['email']:
            errors.append('Email field may not be left blank.')
        elif not EMAIL_REGEX.match(info['email']):
            error.append('Submitted email is not valid.')

        if not info['password']:
            errors.append('Password left blank.')
        elif len(info['password']) < 8:
            errors.append('Password must have more than eight characters.')
        elif info['password'] != info['pw_confirm']:
            errors.append('Passwords don\'t match.')

        if errors:
            return {'status': False, 'errors': errors}
        else:
            password = info['password']

            pw_hash = self.bcrypt.generate_password_hash(password)
            i_query = "INSERT INTO users (first_name, last_name, email, created_at, password) VALUES (%s, %s, %s, NOW(), %s)"
            i_data = [info['first_name'], info['last_name'], info['email'], pw_hash]
            self.db.query_db(i_query, i_data)
            
            g_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(g_query)

            if users[0]['id'] == 1:
                u_query = "UPDATE users SET user_level = 'admin' WHERE id = %s"
                u_data = [users[0]['id']]
                self.db.query_db(u_query, u_data)
                
            else:
                u_query = "UPDATE users SET user_level = 'normal' WHERE id = %s"
                u_data = [users[0]['id']]
                self.db.query_db(u_query, u_data)
                 
            users = self.db.query_db(g_query)
            return {"status": True, "user": users[0]}

    def login_user(self, info):
        password = info['password']

        g_query = "SELECT * FROM users WHERE email = %s LIMIT 1"
        data = [info['email']]
    	users = self.db.query_db(g_query, data)

        if len(users) > 0:
            if self.bcrypt.check_password_hash(users[0]['password'], password):
                return {"status": True, "user": users[0]}

        return {"status": False, "error": "Incorrect information"}

    def get_user(self, info):
        g_query = "SELECT * FROM users WHERE id = %s"
        data = [info['id']]
        user = self.db.query_db(g_query, data)
        return user[0]

    def admin_edit_info(self, info):
        query = "UPDATE users SET email = %s, first_name = %s, last_name = %s, user_level = %s WHERE id = %s"
        data = [info['email'], info['first_name'], info['last_name'], info['user_level'], info['id']]
        self.db.query_db(query, data)
        return None 

    def create_comment(self, info):
        query = "INSERT INTO comments (content, created_at, users_id, wall_id) VALUES (%s, NOW(), (SELECT id from users WHERE users.id = %s), ((SELECT id from wall WHERE id = %s)))"
        data = [info['content'], info['user_id'], info['wall_id']]
        self.db.query_db(query, data)
        return None

    def create_reply(self, info):
        query = "INSERT INTO replies (reply, created_at, users_id, comments_id) VALUES (%s, NOW(), (SELECT id from users WHERE users.id = %s), ((SELECT id from comments WHERE id = %s)))"
        data = [info['reply'], info['user_id'], info['comments_id']]
        self.db.query_db(query, data)
        return None


    def access_wall(self, info):
        g_query = "SELECT * FROM wall WHERE users_id = %s"
        print info['id']
        data = [info['id']]
        wall = self.db.query_db(g_query, data)
        if len(wall) > 0:
            return {"status": True, "wall": wall[0]}
        
        return {"status": False}

    def create_wall(self, info):
        i_query = "INSERT INTO wall (users_id) VALUES ((SELECT id from users WHERE users.id = %s))"
        data = [info['id']]
        self.db.query_db(i_query, data)
        g_query = "SELECT FROM wall WHERE users_id = %s"
        return self.db.query_db(g_query,data)

    def render_comments(self, info):
        r_query = "SELECT *, comments.id as comment_id FROM comments JOIN users ON comments.users_id = users.id where comments.wall_id = %s"
        data = [info['id']]
        return self.db.query_db(r_query, data)

    def render_replies(self, info):
        r_query = "SELECT * FROM replies JOIN users ON replies.users_id = users.id where replies.comments_id = %s"
        data = [info['id']]
        return self.db.query_db(r_query, data)
    def get_all_comments(self):
        query = "SELECT * FROM comments"
        return self.db.query_db(query)

    def get_all_replies(self):
        query = "SELECT * FROM comments"
        return self.db.query_db(query)




    def all_users(self):
        query = ("SELECT * FROM products")
        return self.db.query_db(query)

    def create_user(self, product):
    	query = "INSERT INTO products (first_name, last_name price) VALUE (%s %s, %s, %s)"
    	data = [product['name'], product['description'], product['price']]
    	return self.db.query_db(query, data)

    def update_product(self, product):
    	query = "UPDATE products SET name = %s, description= %s, price = %s WHERE id = %s"
    	data = [product['name'], product['description'], product['price'], product['id']]
        print data
    	return self.db.query_db(query, data)

    def remove_product(self, product):
    	query = "DELETE FROM products WHERE id = %s"
    	data = [product['id']]
    	return self.db.query_db(query, data)
'''

   
