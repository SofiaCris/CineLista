import os 
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir, "filmes.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Filme(db.Model):
    nome = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    descricao = db.Column(db.Text, nullable=True)
    duracao = db.Column(db.String(50), nullable=True)
    genero = db.Column(db.String(50), nullable=True)
    faixa_etaria = db.Column(db.String(10), nullable=True)
    diretor = db.Column(db.String(80), nullable=True)

    def __repr__ (self):
        return '<nome: {}>'.format(self.nome)
    
with app.app_context():
    db.create_all()

@app.route('/', methods= ["GET", "POst"]) 
def index():
    filmes = None
    if request.form:
        try:
            filme = Filme(nome = request.form.get("nome"))
            db.session.add(filme)
            db.session.commit()
        except Exception as e:
            print("Falha em adicionar o filme")
            print(e)
    filmes = Filme.query.all()
    return render_template('index.html', filmes=filmes) 

@app.route('/atualizar', methods=['POST'])
def atualizar():
    try:
        nome_novo = request.form.get("nome_novo")
        nome_antigo = request.form.get("nome_antigo")
        filme = Filme.query.filter_by(nome = nome_antigo).first()
        filme.nome = nome_novo
        db.session.commit()
    except Exception as e:
        print("Não foi possível atualizar o nome do filme")
        print (e)
    return redirect('/')

@app.route('/apagar', methods=['POST']) 
def apagar():
    nome = request.form.get("nome")
    filme = Filme.query.filter_by(nome = nome).first()
    db.session.delete(filme)
    db.session.commit()

    return redirect("/")

@app.route('/informacoes/<string:nome>', methods=['GET'])
def informacoes(nome):
    filme = Filme.query.filter_by(nome=nome).first()
    return render_template('informacoes.html', filme=filme)

@app.route('/adicionar_informacoes/<string:nome>', methods=['GET', 'POST'])
def adicionar_informacoes(nome):
    if request.method == 'POST':
        duracao = request.form.get("duracao")
        genero = request.form.get("genero")
        faixa_etaria = request.form.get("faixa_etaria")
        descricao = request.form.get("descricao")
        diretor = request.form.get("diretor")
        
        filme = Filme.query.filter_by(nome=nome).first()
        filme.duracao = duracao
        filme.genero = genero
        filme.faixa_etaria = faixa_etaria
        filme.descricao = descricao
        filme.diretor = diretor
        
        db.session.commit()
        return redirect('/')
    
    return render_template('descricao.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)