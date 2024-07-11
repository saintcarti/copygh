
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito
    
 
    def agregar(self, producto):
        if producto.stock > -1:
            if str(producto.productoId) not in self.carrito.keys():
                self.carrito[str(producto.productoId)] = {
                    "productoId": producto.productoId,
                    "nombre": producto.nombre,
                    "imagen": producto.imagen.url,
                    "precio": str(producto.precio),
                    "cantidad": 1,
                    "total": str(producto.precio)
                }
                producto.stock -= 1
                producto.save()
            else:
                for key, value in self.carrito.items():
                    if key == str(producto.productoId):
                        if producto.stock > 0:
                            value["cantidad"] = value["cantidad"] + 1
                            value["total"] = float(value["precio"]) * value["cantidad"]
                            producto.stock -= 1
                        break
                producto.save()
            self.guardar_carrito()




    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.productoId)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()
    
    def restar(self, producto):
        producto_id = str(producto.productoId)
        if producto_id in self.carrito:
            self.carrito[producto_id]["cantidad"] -= 1
            self.carrito[producto_id]["total"] -= producto.precio
            if self.carrito[producto_id]["cantidad"] < 1:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
