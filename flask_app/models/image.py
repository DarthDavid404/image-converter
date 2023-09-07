from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app


db = 'imgconverter_db'



class Img:
    def __init__( self , data ):
        self.id = data['id']
        self.filepath = data['filepath']
        self.filename = data['filename']
        self.user_id = data['user_id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        


    @classmethod
    def save_file(cls, data):
            
            query = "INSERT INTO image (filepath, filename, user_id, created_at, updated_at ) VALUES (%(filepath)s, %(filename)s, %(users_id)s, NOW(),NOW());"
            
            return connectToMySQL(db).query_db(query,data)
        
        
    @classmethod
    def get_saved_files(cls):
        query = query = "SELECT * FROM image LEFT JOIN users ON users.id = user_id"
        
        results = connectToMySQL(db).query_db(query)
        file_list = []
        
        if len(results) < 1:
            return
    
        for result in results:
            file_list.append(cls(result))
        
        
        
        
        return file_list
    
    
    @classmethod
    def delete_file(cls, data):
        query = 'DELETE from image where id = %(id)s'
        
        return connectToMySQL(db).query_db(query, data)
        

        
       