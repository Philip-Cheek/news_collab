from system.core.model import Model
from werkzeug import secure_filename
import random
import time
import os 
import re

class NewsModel(Model):
    def __init__(self):
        super(NewsModel, self).__init__()


    def search(self, info):
        query = "SELECT * FROM cities WHERE name = %s"
        data = [info['name']]
        cities = self.db.query_db(query, data)

        if len(cities) < 1:
            queryish = "SELECT * FROM cities WHERE name SOUNDS LIKE %s"
            candidates = self.db.query_db(queryish, data)
            results = {"results": True, "cities" : candidates}
        elif len(cities) > 1:
            return {"results": True, "cities" : cities}
        else:
            return {"results": False, "city": cities[0]}

        a_aquery = "SELECT * FROM articles WHERE name = %s"

        a_queryish = "SELECT * FROM articles WHERE name SOUNDS LIKE %s"

        u_query = "SELECT * FROM users WHERE name =%s"
        u_queryish = "SELECT * FROM users WHERE name SOUNDS LIKE %s"
                
    def render_articles (self, info):
        query = "SELECT articles.title as article_title, CONCAT(users.first_name,' ', users.last_name) as author_name, articles.created_at as date_created, articles.updated_at as edit_commit, CONCAT(editors.first_name,' ', editors.last_name) as editor_name FROM articles JOIN users ON articles.author_id = users.id LEFT JOIN edits on edits.article_id = articles.id JOIN users as editors on editors.id = edits.user_id WHERE articles.paper_id = %s ORDER BY date_created DESC LIMIT 75"
        data = [info['paper_id']]
        return self.db.query_db(query, data)
    

    '''working on flexible models to cannibalize nearly repetitive queries'''
    def get_table_flex(self, info):
        query = "SELECT * FROM %s WHERE %s = %s"
        data = [info['table'], [info['where']], info['data']]
        return self.db.query_db(query, data)
    
    def get_paper(self, info):
        query = "SELECT papers.name as title,cities.name as city_name FROM papers JOIN cities on cities.id = papers.city_id WHERE papers.id = %s"
        data = [info['paper_id']]
        paper = self.db.query_db(query, data)
        return paper[0]

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

    

    def upload_image(self,info):
        query = "UPDATE users SET url = %s where id = %s"
        data = [info['url'], info['user_id']]
        url = self.db.query_db(query, data)
        

    def log_user(self, info):
        password = info['password']

        g_query = "SELECT *, users.id as user_id FROM users JOIN papers on papers.id = users.paper_id WHERE email = %s"
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

    def paper_city(self, info):
        data = [info['paper_id']]
        query = "SELECT papers.id as paper_id, papers.name as paper_name," 

    def get_user(self,info):
        query = "SELECT * FROM users WHERE id = %s"
        data = [info['user_id']]
        user = self.db.query_db(query, data)
        return user[0]

    def render_full_city(self, info):
        data = [info['id']]
        query = "SELECT cities.name as city_name, countries.name as country_name FROM cities JOIN countries on countries.code = cities.country_code WHERE cities.id = %s"
        city = self.db.query_db(query,data)
        return city[0]

    def get_articles(self, info):
        data = [info['paper_id']]
        query = "SELECT *, articles.id as article_id FROM articles join papers on articles.paper_id = papers.id where papers.id = %s"
        articles = self.db.query_db(query,data)


        if len(articles) < 1:
            return{"status": False, "article_list": None}
        
        return {"status": True, "article_list": articles}


    def new_article(self, info): 
        ile = info['file']

        if not file:
            url = '/static/default.png'
        else:
            img_path = (os.path.dirname('/users/philipcheek/Desktop/news_collab/app/static/uploads'))
            filename = secure_filename(file.filename)
            file.save(os.path.join(img_path + "/uploads", filename))
            url =  "/static/uploads/" + filename

        data = [info['title'], info['content'], info['paper_id'], info['author_id'], info['category'], url]
        query = "INSERT INTO articles (title, content, paper_id, author_id, category, url, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
        self.db.query_db(query, data)

    def render_editors(self, info):
        query = "SELECT * FROM users WHERE paper_id = %s ORDER BY created_at DESC LIMIT 15"
        data = [info['paper_id']]
        return self.db.query_db(query, data)

    def up_vote_article(self, info):
        query = "UPDATE articles SET votes = votes + 1 WHERE id = %s"
        data = [info['article_id']]
        self.db.query_db(query, data)

        return None

    def down_vote_article(self, info):
        query = "UPDATE articles SET votes = votes - 1 WHERE id = %s"




   
