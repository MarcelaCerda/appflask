from flask import Flask ,jsonify,request
from flask_cors import CORS
 
from flask_sqlalchemy import SQLAlchemy      # ORM manejador de Base de datos
from flask_marshmallow import Marshmallow    # manejo JSON
 
app=Flask(__name__)
CORS(app)
 
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10507594:fcmUfEw4se@sql10.freemysqlhosting.net/sql10507594'
#                                                     user:clave@URL_BaseDatos/nombreBaseDatos
'''
Host: sql10.freesqldatabase.com
Database name: sql10507594
Database user: sql10507594
Database password: fcmUfEw4se
Port number: 3306
'''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)
 
# defino las tablas*******************************
class Producto(db.Model):   # la clase Producto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
     
    def __init__(self,nombre,precio,stock):   #crea el  constructor de la clase
        self.nombre=nombre   # no  el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.stock=stock

class Usuario(db.Model):   # la clase Producto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    email=db.Column(db.String(100))
    prioridad=db.Column(db.Integer)
    
    def __init__(self,nombre,email,prioridad):   #crea el  constructor de la clase
        self.nombre=nombre   # no  el id porque lo crea sola mysql por ser auto_incremento
        self.email=email
        self.prioridad=prioridad


db.create_all()  # crea las tablas
#  ************************************************************
class ProductoSchema(ma.Schema):
    class Meta:   # matchea los campos con los valores para generarel JSON
        fields=('id','nombre','precio','stock')

producto_schema=ProductoSchema()            # para crear un producto
productos_schema=ProductoSchema(many=True)  # multiples registros
 
# programo los mapeos, o las rutas, los endpoint, la URL
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()
    result=productos_schema.dump(all_productos)
    return jsonify(result)  # returna un JSON con todos los producto
 
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/producto/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route('/productos', methods=['POST']) #  endpoint para insertar un producto
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    new_producto=Producto(nombre,precio,stock)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)
 
 
@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
   
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
 
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    db.session.commit()
    return producto_schema.jsonify(producto)

# Usuario*****************

class UsuarioSchema(ma.Schema):
    class Meta:   # matchea los campos con los valores para generarel JSON
        fields=('id','nombre','email','prioridad')

usuario_schema=UsuarioSchema()            # para crear un usuario
usuarios_schema=UsuarioSchema(many=True)  # multiples registros
  
# programo los mapeos, o las rutas, los endpoint, la URL
@app.route('/',methods=['GET'])
def index():
    return "CRUD Python"
 
@app.route('/usuarios',methods=['GET'])
def get_Usuarios():
    all_usuarios=Usuario.query.all()
    result=usuarios_schema.dump(all_usuarios)
    return jsonify(result)  # returna un JSON con todos los usuario
 
@app.route('/usuarios/<id>',methods=['GET'])
def get_usuario(id):
    usuario=Usuario.query.get(id)
    return usuario_schema.jsonify(usuario)

@app.route('/usuario/<id>',methods=['DELETE'])
def delete_usuario(id):
    usuario=Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)

@app.route('/usuarios', methods=['POST']) #  endpoint para insertar un usuario
def create_usuario():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    email=request.json['email']
    prioridad=request.json['prioridad']
    new_usuario=Usuario(nombre,email,prioridad)
    db.session.add(new_usuario)
    db.session.commit()
    return usuario_schema.jsonify(new_usuario)
 
 
@app.route('/usuarios/<id>' ,methods=['PUT'])
def update_usuario(id):
    usuario=Usuario.query.get(id)
   
    nombre=request.json['nombre']
    precio=request.json['precio']
    prioridad=request.json['prioridad']
 
    usuario.nombre=nombre
    usuario.precio=precio
    usuario.prioridad=prioridad
    db.session.commit()
    return usuario_schema.jsonify(usuario)


# programa principal ****************************************
if __name__=='__main__':  
    app.run(  )

#debug=True, port=5000