from sqlalchemy import select
from app import app, db
from app.bets.model import Bet, BetUserAssociation
from app.users.model import User

with app.app_context():
    db.create_all()
    for i in range(0, 100):
        b = Bet(f'Description {i}')
        db.session.add(b)
    db.session.commit()

    for i in range(0, 100):
        u = User(f'user{i}', 'Bob', f'Jones{i}')
        db.session.add(u)
    db.session.commit()

    stmt = select(User).filter(User.id == 50)
    u = None
    for row in db.session.execute(stmt):
        u = row[0]
    print(u)

    stmt = select(Bet).where(Bet.id == 1)
    b = None
    for row in db.session.execute(stmt):
        b = row[0]
    print(b)

    association = BetUserAssociation(b.id, u.id)
    db.session.add(association)
    db.session.commit()
