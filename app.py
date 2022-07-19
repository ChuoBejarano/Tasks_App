from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db'
db = SQLAlchemy(app)


class Tarea(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	contenido = db.Column(db.String(200))
	hecho = db.Column(db.Boolean)

@app.route('/')
def home():
	tareas = Tarea.query.all()
	return render_template('index.html', tareas= tareas)

@app.route('/crear-tareas', methods=['POST'])
def create():
	tarea = Tarea(contenido= request.form['contenido'], hecho=False)
	db.session.add(tarea)
	db.session.commit()
	return redirect(url_for('home'))

@app.route('/hecho/<id>')
def done(id):
	tarea = Tarea.query.filter_by(id=int(id)).first()
	tarea.hecho = not(tarea.hecho)
	db.session.commit()
	return redirect(url_for('home'))

@app.route('/eliminar/<id>')
def delete(id):
	tarea = Tarea.query.filter_by(id=int(id)).delete()
	db.session.commit()
	return redirect(url_for('home'))




if __name__ == '__main__':
	app.run(debug=True)
