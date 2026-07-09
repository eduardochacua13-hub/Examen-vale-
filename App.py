from flask import Flask, jsonify, request
from database import Database  

app = Flask(__name__)

# ==========================================
# 1. LISTAR PRODUCTOS (GET)
# ==========================================
@app.route("/productos", methods=["GET"])
def listar_productos():
    db = Database() 
    data = db.execute(
        """
        SELECT p.id, p.nombre, p.precio, p.activo, p.categoria_id, c.nombre as categoria_nombre
        FROM public.productos p
        LEFT JOIN public.categorias c ON p.categoria_id = c.id
        ORDER BY p.id ASC
        """
    )
    db.close() 

    productos_formateados = []
    if data:
        for prod in data:

            productos_formateados.append({
                "id": prod[0],
                "nombre": prod[1],
                "precio": float(prod[2]),   
                "activo": prod[3],
                "categoria_id": prod[4],
                "categoria_nombre": prod[5] if prod[5] else "Sin Categoría" 
            })

    return jsonify(productos_formateados) 


# ==========================================
# 2. CREAR PRODUCTO (POST)
# ==========================================
@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json  

    db = Database()

    db.execute(
        """
        INSERT INTO public.productos(nombre, precio, activo, categoria_id)
        VALUES (%s, %s, %s, %s)
        """,
        (
            data["nombre"],
            data["precio"],
            data["activo"],
            data["categoria_id"] 
        )
    )
    db.close()

    return jsonify({"mensaje": "Producto creado exitosamente"}), 201


# ==========================================
# 3. ACTUALIZAR PRODUCTO (PUT)
# ==========================================
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.json    

    db = Database()
    db.execute(
        """
        UPDATE public.productos
        SET nombre=%s,
            precio=%s,
            activo=%s,
            categoria_id=%s
        WHERE id=%s
        """,
        (
            data["nombre"],
            data["precio"],
            data["activo"],
            data["categoria_id"],
            id  
        )
    )
    db.close()

    return jsonify({"mensaje": "Producto actualizado exitosamente"})


# ==========================================
# 4. ELIMINAR PRODUCTO (DELETE)
# ==========================================
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    db = Database()
    db.execute("DELETE FROM public.productos WHERE id=%s", (id,))
    db.close()

    return jsonify({"mensaje": "Producto eliminado físicamente"})


# ==========================================
# APERTURA DEL SERVIDOR
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
