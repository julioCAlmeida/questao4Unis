from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'imc_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Função para obter a lista de usuários
def get_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nome, altura, peso, (peso * 100 / POW(altura, 2) * 100) AS imc, CASE \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 17 THEN 'Muito abaixo do peso' \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 18.5 THEN 'Abaixo do peso' \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 25 THEN 'Peso normal' \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 30 THEN 'Acima do peso' \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 35 THEN 'Obesidade I' \
                WHEN (peso * 100 / POW(altura, 2) * 100) < 40 THEN 'Obesidade II (severa)' \
                ELSE 'Obesidade III (mórbida)' END AS situacao FROM usuarios ORDER BY nome")
    usuarios = cur.fetchall()
    cur.close()
    return usuarios

@app.route('/')
def index():
    return render_template('index.html', result_text="")

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    patient_name = request.form['patient_name']
    full_address = request.form['full_address']

    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
    except ValueError:
        return render_template('index.html',
                               result_text="Por favor, insira valores numéricos válidos para Peso e Altura.")

    bmi = ((weight * 100) / (height ** 2)) * 100

    if bmi < 17:
        situation = "Muito abaixo do peso"
    elif 17 <= bmi < 18.5:
        situation = "Abaixo do peso"
    elif 18.5 <= bmi < 25:
        situation = "Peso normal "
    elif 25 <= bmi < 30:
        situation = "Acima do peso"
    elif 30 <= bmi < 35:
        situation = "Obesidade I "
    elif 35 <= bmi < 40:
        situation = "Obesidade II (severa)"
    else:
        situation = "Obesidade III (mórbida)"

    result_text = f"{patient_name.upper()}\nIMC: {bmi:.2f}\nSituação: {situation}"

    # Inserir dados no banco de dados
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nome, altura, peso) VALUES (%s, %s, %s)",
                (patient_name, height, weight))
    mysql.connection.commit()
    cur.close()

    return render_template('index.html', result_text=result_text)

@app.route('/usuarios_cadastrados')
def usuarios_cadastrados():
    usuarios = get_usuarios()
    return render_template('usuarios_cadastrados.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
