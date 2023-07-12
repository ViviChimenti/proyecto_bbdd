
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from flask_migrate import Migrate
import os

virtual_env = os.getenv('VIRTUAL_ENV')
if virtual_env:
    print("Entorno virtual:", os.path.basename(virtual_env))
else:
    print("No se ha activado ningún entorno virtual.")


app=Flask(__name__) #Crea el objeto app de la clase Flask
CORS(app) #permite acceder desde el front al back

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/proyecto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow
#migrate = Migrate(app, db)

# ---------fin configuracion-----------

#definimos la tabla
class Producto(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    pcategoria=db.Column(db.String(100))
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,precio,stock,pcategoria,imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.pcategoria = pcategoria
        self.imagen = imagen

    #Si hay mas tablas para crear las definimos aca

with app.app_context():
    db.create_all() #Crea las tablas

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','pcategoria','imagen')
    
producto_schema=ProductoSchema() #El objeto para traer un producto
productos_schema=ProductoSchema(many=True) #Trae muchos registro de producto
# ------------------------------------
#definimos tabla categoria

class Categoria(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    categoria=db.Column(db.String(100))
    detalle=db.Column(db.String(100))
    def __init__(self,categoria,detalle):
        self.categoria = categoria
        self.detalle = detalle

with app.app_context():
    db.create_all() #Crea las tablas

class CategoriaSchema(ma.Schema):
    class Meta:
        fields=('id','categoria','detalle')
    
categoria_schema=CategoriaSchema() #El objeto para traer un categoria
categorias_schema=CategoriaSchema(many=True) #Trae muchos registro de categoria

#-------------------------------------
#Creamos los endpoint
#GET
#POST
#Delete
#Put

#Get endpoint del get
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos = Producto.query.all() #heredamos del db.model
    result= productos_schema.dump(all_productos) #lo heredamos de ma.schema
                                                #Trae todos los registros de la tabla y los retornamos en un JSON
    return jsonify(result)


@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro

@app.route('/productos/<nombre>', methods=['GET'])
def get_producto_por_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first()
    if producto:
        return producto_schema.jsonify(producto)
    else:
        return jsonify({"message": "Producto no encontrado"})




@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado


@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    print(request.json)
    nombre=request.json.get('nombre')
    precio=request.json.get('precio')
    stock=request.json.get('stock')
    pcategoria=request.json.get('pcategoria')
    imagen=request.json.get('imagen')

    if not nombre or not precio or not stock or not pcategoria or not imagen:
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    new_producto = Producto(nombre=nombre, precio=precio, stock=stock, pcategoria=pcategoria, imagen=imagen)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto),201


@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
 
    producto.nombre=request.json['nombre']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.pcategoria=request.json['pcategoria']
    producto.imagen=request.json['imagen']


    db.session.commit()
    return producto_schema.jsonify(producto)


#------------------------------------------
#Get endpoint del get categoria
@app.route('/categorias',methods=['GET'])
def get_Categorias():
    all_categorias = Categoria.query.all() #heredamos del db.model
    result= categorias_schema.dump(all_categorias) #lo heredamos de ma.schema
                                                #Trae todos los registros de la tabla y los retornamos en un JSON
    return jsonify(result)


@app.route('/categorias/<id>',methods=['GET'])
def get_categoria(id):
    categoria=Categoria.query.get(id)
    return categoria_schema.jsonify(categoria)   # retorna el JSON de un producto recibido como parametro

@app.route('/categorias/<categoria>', methods=['GET'])
def get_categoria_por_nombre(categoria):
    categoria = Categoria.query.filter_by(categoria=categoria).first()
    if categoria:
        return categoria_schema.jsonify(categoria)
    else:
        return jsonify({"message": "Categoria no encontrada"})




@app.route('/categorias/<id>',methods=['DELETE'])
def delete_categoria(id):
    categoria=Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return categoria_schema.jsonify(categoria)   # me devuelve un json con el registro eliminado


@app.route('/categorias', methods=['POST']) # crea ruta o endpoint
def create_categoria():
    #print(request.json)  # request.json contiene el json que envio el cliente
    categoria=request.json['categoria']
    detalle=request.json['detalle']
    new_categoria=Categoria(categoria,detalle)
    db.session.add(new_categoria)
    db.session.commit()
    return categoria_schema.jsonify(new_categoria)


@app.route('/categorias/<id>' ,methods=['PUT'])
def update_categoria(id):
    categoria=Categoria.query.get(id)
 
    categoria.categoria=request.json['categoria']
    categoria.detalle=request.json['detalle']
   
    db.session.commit()
    return categoria_schema.jsonify(categoria)
#-------------------------------------------------------

#Programa Principal
if __name__ == '__main__':
    app.run(debug=True, port=5000)
