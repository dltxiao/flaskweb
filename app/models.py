from app import db

class Role(db.Model):                                            
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key = True)               
    name = db.Column(db.String(64), unique = True)               
    # 增加这个关系声明后，可以使用user.role来获取Role模型对象,可以使用user.role.id, user.role.name来获取对应的值。
    users = db.relationship('User', backref='role')              
                                                                 
    def __repr__(self):                                          
        return '<Role %r>' % self.name                           
                                                                 
class User(db.Model):
    __tablename__ = 'Users'                                      
    id = db.Column(db.Integer, primary_key=True)                 
    username = db.Column(db.String(64), unique=True, index=True) 
    sexy = db.Column(db.SmallInteger)                            
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))   
    
    def __repr__(self):                                          
        return '<User %r>' % self.username
