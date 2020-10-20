from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    due = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Assignment %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        assignment_course = request.form['course']
        assignment_task = request.form['task']
        assignment_due = request.form['due']
        new_assignment = Todo(course=assignment_course, task=assignment_task, due = assignment_due)
		
        try:
            db.session.add(new_assignment)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your assignment'

    else:
        assignments = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', assignments=assignments)


@app.route('/delete/<int:id>')
def delete(id):
    assignment_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(assignment_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that assignment'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    assignment = Todo.query.get_or_404(id)

    if request.method == 'POST':
        assignment.course = request.form['course']
        assignment.task = request.form['task']
        assignment.due = request.form['due']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your assignment'

    else:
        return render_template('update.html', assignment=assignment)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
