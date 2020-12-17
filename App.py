#Mensajes entre vistas funcion flash 
from flask import Flask,render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 

app = Flask(__name__)

#concetado a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('select * from contacts')
    data = cur.fetchall()
    return render_template('index.html',contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        #Datos desde el formulario
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        ##obtinene la conexion
        cur = mysql.connection.cursor()

        cur.execute( 'insert into contacts (fullname,phone,email) values (%s,%s,%s)',
        (fullname,phone,email))

        mysql.connection.commit()

        #Enviar Mensaje
        flash("Contact added successfully")
        #url direccionar
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts where id=%s",id)
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html',contact=data[0])

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""

            UPDATE contacts 
            SET fullname = %s,  
                email = %s,
                phone = %s 
            WHERE id = %s

        """,(fullname,email,phone,id))
        mysql.connection.commit()
        flash("Actualizado ok")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts where id={0}".format(id))
    mysql.connection.commit()
    flash("Contact Removed successfully")
    return redirect(url_for('Index'))    


if __name__ == "__main__":
    app.run(debug = True, port = 3000)
