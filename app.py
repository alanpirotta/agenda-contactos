from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

# def cls():
#     os.system('cls')
# cls()


app=Flask(__name__)
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='agenda_contactos'
mysql.init_app(app)

@app.route('/')
def index():
    sql= "SELECT * FROM `agenda_contactos`.`contactos`;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)
    contactos=cursor.fetchall()
    print(f'La cantidad de contactos es: {len(contactos)}')
    for contacto in contactos:
        print(contacto)
    conn.commit()
    return render_template('contactos/index.html', contactos=contactos)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM `agenda_contactos`.`contactos` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def method_name(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `agenda_contactos`.`contactos` WHERE id=%s ", (id))
    contactos=cursor.fetchall()
    conn.commit()
    return render_template('contactos/EDIT.html', contactos=contactos)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['addNombre']
    _telefono=request.form['addTelefono']
    _email=request.form['addEmail']
    id=request.form['contactId']
    _foto=request.files['addFoto']
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if _foto.filename != '':
        nombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nombreFoto)
    
    sql= "UPDATE `agenda_contactos`.`contactos` SET `nombre`=%s, `telefono`=%a, `email`=%s WHERE id=%s;"
    datos=(_nombre, _telefono, _email, id)
    
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

@app.route('/create')
def create():
    return render_template('contactos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['addNombre']
    _telefono=request.form['addTelefono']
    _email=request.form['addEmail']
    _foto=request.files['addFoto']
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if _foto.filename != '':
        nombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nombreFoto)
    
    sql= "INSERT INTO `contactos` (`id`, `nombre`, `telefono`, `email`, `foto`) VALUES (NULL, %s, %s, %s,%s);"
    datos=(_nombre,_telefono,_email,nombreFoto)
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
    