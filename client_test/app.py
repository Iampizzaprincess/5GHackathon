from flask import Flask 
from flask import url_for
from flask import render_template
from flask import jsonify
app = Flask(__name__)

class Fake_Bet():
    def __init__(self, d, a1=None, a2=None):
        self.description = d
        self.action1 = a1
        self.action2 = a2

    def get_bet(self):
        return {
            'description':self.description,
            'action1':self.action1,
            'action2':self.action2
        }

class Bet_Container():
    def __init__(self, size):
        self.all_bets = [Fake_Bet(f'bet {i}', 'action1', 'action2').get_bet() for i in range(size)]

    def get_all_bets(self):
        return jsonify(self.all_bets)

bets = Bet_Container(20)

@app.route('/')
def index():
    return "Hello World, I am trapped in a computer"

@app.route("/bets")
def secret():
    return bets.get_all_bets()