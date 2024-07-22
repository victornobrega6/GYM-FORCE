# aqui vão ficar os comandos de compilação
# instalamos a biblioteca flash com o comando pip3 install flask

from flask import Flask, render_template, request, redirect, flash, session

from flask_sqlalchemy import SQLAlchemy

# abaixo é criada a variavel de aplicação!

app = Flask(__name__)

#a linha abaixo é a chave de segurança da aplicação
app.secret_key = "aprendendodoiniciocomdaniel"


app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = '127.0.0.1:3306',
        database = 'loja'
    )

db = SQLAlchemy(app)

class Produto(db.Model):
    id_produto = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_produto = db.Column(db.String(50), nullable = False)
    marca_produto = db.Column(db.String(30), nullable = False)
    preco_produto = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name
    

class Advanced_suplements(db.Model):
    id_adv = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_adv = db.Column(db.String(50), nullable = False)
    marca_adv = db.Column(db.String(30), nullable = False)
    preco_adv = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name


# a linha abaixo eu crio uma rota

###@app.route("/inicio")
#def ola():
    #return "<h2>Iniciando com Flask</h2>"

# a rota abaixo chama a lista de produtos
@app.route("/lista") # LISTA DE SUPLEMENTOS NORMAIS
def lista_produtos():

    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')
    
    prod_cadastros = Produto.query.order_by(Produto.id_produto)
    

    return render_template("lista.html",
                 todos_produtos = prod_cadastros)

@app.route("/advanced_suplements") # LISTA DE SUPLEMTOS AVANÇADOS
def advanced_suplements():

    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')
    
    prod_cadastros_adv = Advanced_suplements.query.order_by(Advanced_suplements.id_adv)
    

    return render_template("advanced_suplements.html",
                            todos_produtos_adv = prod_cadastros_adv)


@app.route("/cadastrar") # LISTA DE SUPLEMTOS NORMAIS
def cadastrar_produto():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')

    return render_template("cad_produto.html")


@app.route("/cadastrar_adv") # LISTA DE SUPLEMTOS AVANÇADOS
def cadastrar_produto_adv():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')

    return render_template("cad_produto_adv.html")

#a rota a baixo é responsavel por adicionar o produto na lista
@app.route("/adicionar", methods=["POST",])
def adicionar_produto():

    #as linhas a baixo fazem a capitação dos dados dos formularios
    nome_recebido = request.form["txtNome"]
    marca_recebido = request.form["txtMarca"]

    preco_recebido = request.form["txtPreco"].replace(',', '.')

    preco_recebido = float(preco_recebido)


    #linha a baixo é a variavel q prepara os dados para enviar para o banco de dados
    add_produto = Produto(nome_produto = nome_recebido, marca_produto = marca_recebido, preco_produto = preco_recebido)
    
    #a linha abaixo adiciona a varivael para ser inserida na tabela
    db.session.add(add_produto)

    #a linha abaixo envia as informaçoes para o banco de dados 
    db.session.commit()

    #A LINHA ABAIXO ENVIA A MENSAGEM PARA APRESENTAR PARA O USER
    flash("Produto cadastrado com sucesso!!!")

    return redirect('/lista')

#a rota a baixo é responsavel por adicionar o produto na lista
@app.route("/adicionar_adv", methods=["POST",]) # ADICIONA PRODUTO A LISTA ADV
def adicionar_produto_adv():

    #as linhas a baixo fazem a capitação dos dados dos formularios
    nome_recebido_adv = request.form["txtNome"]
    marca_recebido_adv = request.form["txtMarca"]

    preco_recebido_adv = request.form["txtPreco"].replace(',', '.')

    preco_recebido_adv = float(preco_recebido_adv)


    #linha a baixo é a variavel q prepara os dados para enviar para o banco de dados
    add_produto_adv = Advanced_suplements(nome_adv = nome_recebido_adv, marca_adv = marca_recebido_adv, preco_adv = preco_recebido_adv)
    
    #a linha abaixo adiciona a varivael para ser inserida na tabela
    db.session.add(add_produto_adv)

    #a linha abaixo envia as informaçoes para o banco de dados 
    db.session.commit()

    #A LINHA ABAIXO ENVIA A MENSAGEM PARA APRESENTAR PARA O USER
    flash("Produto cadastrado com sucesso!!!")

    return redirect('/advanced_suplements')



@app.route("/edit/<int:id>") #entre <> define o tipo primeiro (int,str etc) LISTA DE SUPLEMTOS NORMAIS
def editar_produto(id):

    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')


    # a variavel abaixo é o produto buscado no banco 
    
    produto_selecionado = Produto.query.filter_by(id_produto = id).first() #filter by é mais especifico, assim que ele acha o que voce procura ele para o filter normal busca todos

    return render_template("edit.html", produto = produto_selecionado)

@app.route("/edit_adv/<int:id>") #entre <> define o tipo primeiro (int,str etc) LISTA DE SUPLEMTOS AVANÇADOS
def editar_produto_adv(id):

    if 'usuario_logado' not in session or session['usuario_logado'] == None: return redirect('/login')

    # a variavel abaixo é o produto buscado no banco 
    
    produto_selecionado_adv = Advanced_suplements.query.filter_by(id_adv = id).first() #filter by é mais especifico, assim que ele acha o que voce procura ele para o filter normal busca todos

    return render_template("edit_adv.html", advanced_suplements = produto_selecionado_adv)



@app.route('/upgrade', methods = ['POST',])
def up():
    produto_selecionado = Produto.query.filter_by(id_produto = request.form['txtId']).first()

    #AS LINHAS ABAIXO ATUALIZAM CADA CAMPO NA TABELA DO BANCO COM BASE NAS INFORMAÇOES PASSADAS
    #PELO USUARIO
    produto_selecionado.nome_produto = request.form['txtNome']
    produto_selecionado.marca_produto = request.form['txtMarca']
    produto_selecionado.preco_produto = request.form['txtPreco']

    #A LINHA ABAIXO ADICIONA AS INFORMAÇOES NA CAMADA PARA ENVIAR PRO BANCO DE DADOS
    db.session.add(produto_selecionado)

    #A LINHA ABAIXO MANDA AS INFORMAÇOES PARA O BANCO DE DADOS
    db.session.commit()

    return redirect('/lista')


@app.route('/upgrade1', methods = ['POST',])
def up_adv():
    produto_selecionado_adv = Advanced_suplements.query.filter_by(id_adv = request.form['txtId']).first()

    #AS LINHAS ABAIXO ATUALIZAM CADA CAMPO NA TABELA DO BANCO COM BASE NAS INFORMAÇOES PASSADAS
    #PELO USUARIO
    produto_selecionado_adv.nome_adv = request.form['txtNome']
    produto_selecionado_adv.marca_adv = request.form['txtMarca']
    produto_selecionado_adv.preco_adv = request.form['txtPreco']

    #A LINHA ABAIXO ADICIONA AS INFORMAÇOES NA CAMADA PARA ENVIAR PRO BANCO DE DADOS
    db.session.add(produto_selecionado_adv)

    #A LINHA ABAIXO MANDA AS INFORMAÇOES PARA O BANCO DE DADOS
    db.session.commit()

    return redirect('/advanced_suplements')


# ***** A ROTA ABAIXO SE TRATA DE EXCLUIR O PRODUTO
@app.route('/excluir/<int:id>') # LISTA DE SUPLEMENTOS NORMAIS
def excluir_produto(id):
    #A LINHA ABAIXO EXCLUI O REGISTRO DO BD
    Produto.query.filter_by(id_produto = id).delete()

    #A LINHA ABAIXO COMMITA AS INFORMAÇOES PARA A BASE DE DADOS
    db.session.commit()

    flash("Produto excluido com sucesso!!!")
    return redirect('/lista')


@app.route('/excluir_adv/<int:id>') # LISTA DE SUPLEMENTOS AVANÇADOS
def excluir_produto_adv(id):
    #A LINHA ABAIXO EXCLUI O REGISTRO DO BD
    Advanced_suplements.query.filter_by(id_adv = id).delete()

    #A LINHA ABAIXO COMMITA AS INFORMAÇOES PARA A BASE DE DADOS
    db.session.commit()

    flash("Produto excluido com sucesso!!!")
    return redirect('/advanced_suplements')

@app.route('/login')
def login():
    return render_template('login.html')

#essa é a rota mais sensivel da aplicação
@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    #a linha abaixo verifica se a senha e login sao "admin"
    login = request.form['txtLogin']
    senha = request.form['txtSenha']

    if login == 'admin' and senha == 'senha':
        #session -> é necessario importar 
        # *** IMPORTANTE: para utilizar o session deve se por obrigação
        # *** ter referenciado o comando Secret_Key
        # para que tenha uma sessao onde nao seja apenas o login CRIPTOGRAFADO
        session['usuario_logado'] = request.form['txtLogin']

        return redirect('/lista')
    else:
        #a linhha abaixo retorna para a tela de login caso o usuario
        #erre o login ou senha
        return redirect('/login')

#Rota de Inicio da tela
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

#Rota para sair
@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect('/lista')

#Rota de continuação
@app.route('/caridade')
def caridade():
    return render_template('caridade.html')
    

app.run()
