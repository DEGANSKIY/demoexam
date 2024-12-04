from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BAZADANIX.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BAZADANIX(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_zay = db.Column(db.String(20), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vid_org = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    opis_probl = db.Column(db.String(30), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    responsible = db.Column(db.String(100), nullable=True)
    stage_of_executio = db.Column(db.String(50))
    date_completed = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    ordered_parts = db.Column(db.Text)
    
    def __repr__(self):
        return f'<BAZADANIX {self.num_zay}>'  
    
with app.app_context():
    db.create_all() 

@app.route('/add', methods=['GET', 'POST'])
def add_application():    
    if request.method == 'POST':
        num_zay = request.form['num_zay']
        vid_org = request.form['vid_org']
        model = request.form['model']
        opis_probl = request.form['opis_probl']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = request.form['status']
        new_application = BAZADANIX(
           num_zay=num_zay,
           vid_org=vid_org,
           model=model,
           opis_probl=opis_probl,
           client_name=client_name,
           phone_number=phone_number,
           status=status
        )
        db.session.add(new_application)
        db.session.commit() 
        return redirect(url_for('index'))
    
    return render_template('add_application.html')

@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('index'))

@app.route('/update/<int:application_id>', methods=['GET', 'POST']) # Or use another appropriate method
def update_application(application_id):
    # Fetch the application from the database based on application_id
    application = BAZADANIX.query.get_or_404(application_id)

    if request.method == 'POST':
        application.num_zay = request.form.get('num_zay', application.num_zay)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_application.html', application=application)

@app.route('/')
def index():
    try:
        applications = BAZADANIX.query.all()
        return render_template('index.html', applications=applications)
    except Exception as e:
        return f"Error retrieving applications: {e}", 500

@app.route('/search', methods=['GET', 'POST'])
def search_application():
    if request.method == 'POST':
        search_term = request.form.get('search_id')
        application = BAZADANIX.query.filter_by(num_zay=search_term).first()
        if application:
            return render_template('application_details.html', application=application)
        else:
            return "Заявка не найдена."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)