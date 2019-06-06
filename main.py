import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash

@app.route('/articles', methods=['GET'])
def articles():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM articulos")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/articles/<cod>', methods=['GET'])
def article(cod):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM articulos WHERE codigo=%s", cod)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/articles/<cod>', methods=['DELETE'])
def eliminar(cod):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM articulos WHERE codigo=%s", (cod,))
		conn.commit()
		resp = jsonify('Artículo eliminado')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/articles', methods=['PUT'])
def modificar():
	try:
		_codigo = request.json['codigo']
		_descripcion = request.json['descripcion']
		_precio = request.json['precio']

		if _codigo and _descripcion and _precio and request.method == 'PUT':
			sql = "update articulos set descripcion=%s, precio=%s where codigo=%s"
			data=(_descripcion, _precio, _codigo)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Articulo modificado')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@app.route('/articles', methods=['POST'])
def anadir():
	try:
		'''
		_codigo = request.args.get('codigo')
		_descripcion = request.args.get('descripcion')
		_precio = request.args.get('precio')
		'''
		_codigo = request.json['codigo']
		_descripcion = request.json['descripcion']
		_precio = request.json['precio']
		
		# validate the received values
		if _codigo and _descripcion and _precio and request.method == 'POST':
			#do not save password as a plain text
		#	_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO articulos(codigo,descripcion,precio) VALUES(%s, %s, %s)"
			data = (_codigo,_descripcion,_precio,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp





if __name__ == "__main__":
    app.run()