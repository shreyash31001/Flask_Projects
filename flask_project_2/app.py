from flask import Flask,url_for,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/project'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ' '

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class flask_project2(db.Model):
    __tablename__ = 'flask_project'
    id = db.Column(db.Integer,primary_key=True)
    customer = db.Column(db.String(200),unique=True)
    car_data = db.Column(db.String(200),unique=True)
    price = db.Column(db.Integer)
    deal = db.Column(db.String(200),unique=True)
    rating = db.Column(db.Integer)

    def __init__(self,customer,car_data,price,deal,rating):
        self.customer = customer
        self.car_data = car_data
        self.price = price
        self.deal = deal
        self.rating = rating



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        car_data = request.form['car_data']
        price  = int(request.form['price'])
        deal = request.form['deal']
        rating = request.form['rating']
        print(customer,car_data,price,deal,rating)
        if customer == '' or car_data == '' or price == '' or deal == '' or rating == '':
            return render_template('index.html',message='Please fill all the fields')
        
        if db.session.query(flask_project2).filter(flask_project2.customer == customer).count() == 0:
            data = flask_project2(customer,car_data,price,deal,rating)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html',message='All the fields have been submitted')
        
if __name__ == '__main__':
    app.run(debug=True)