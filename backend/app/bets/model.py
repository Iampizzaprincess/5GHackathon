from app import db

class Bet(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    
    def __init__(self, description):
        self.description = description
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }

    def __repr__(self):
        return f'<Bet {self.id}: {self.description[:20]}'
