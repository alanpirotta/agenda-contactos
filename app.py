from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os

# def cls():
#     os.system('cls')
# cls()


app=Flask(__name__)
app.secret_key='12345678'
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='agenda_contactos'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#Habilta el acceso a la carpeta para el HTML
@app.route('/uploads/<nomFoto>')
def uploads(nomFoto):
    return send_from_directory(app.config['CARPETA'], nomFoto)

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
    cursor.execute("SELECT foto FROM `agenda_contactos`.`contactos` WHERE ID=%s", id)
    fila= cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM `agenda_contactos`.`contactos` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
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
    _foto=request.files['addFoto']
    id=request.form['contactId']
    
    sql= "UPDATE `agenda_contactos`.`contactos` SET `nombre`=%s, `telefono`=%a, `email`=%s WHERE id=%s;"
    datos=(_nombre, _telefono, _email, id)
    
    conn= mysql.connect()
    cursor= conn.cursor()
    
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if _foto.filename != '':
        nombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nombreFoto)
        cursor.execute("SELECT foto FROM `agenda_contactos`.`contactos` WHERE ID=%s", id)
        fila= cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `agenda_contactos`.`contactos` SET foto=%s WHERE id=%s", (nombreFoto, id))
        conn.commit()
        
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
    if _nombre == '' or _telefono== '' or _email=='' or _foto=='':
        flash('Completa todos los campos')
        return redirect(url_for('create'))
    #Falta poner en el create que muestre el mensaje
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
    