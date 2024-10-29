
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee Model for Database
class EmployeeDB(db.Model):
    emp_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.String(10), nullable=False)
    no = db.Column(db.String(100), nullable=False)

# Route to load data from Excel to SQLite
@app.route('/import_excel')
def import_excel():
    # Read Excel file using pandas
    excel_file = '/mnt/data/employees.xlsx'  # Modify as necessary to match the uploaded file path
    df = pd.read_excel(excel_file)

    # Iterate over the rows and insert them into the database
    for _, row in df.iterrows():
        employee = EmployeeDB(
            emp_id=row['emp_id'],
            name=row['name'],
            position=row['position'],
            hire_date=row['hire_date'],
            no=row['no']
        )
        db.session.add(employee)

    db.session.commit()
    return 'Data imported from Excel successfully!'

# Route to display all employees in a table
@app.route('/')
def index():
    employees = EmployeeDB.query.all()
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
