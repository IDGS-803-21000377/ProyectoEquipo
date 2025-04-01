from flask import Blueprint, render_template, redirect, url_for
from models import Producto, db
from forms import MaterialForm

inventarioMaterbp = Blueprint('materiales', __name__, url_prefix='/materiales')

@inventarioMaterbp.route('/', methods=['GET', 'POST'])
def index():
    form = MaterialForm()  

    if form.validate_on_submit():  
        nuevo_material = Producto(
            nombreProducto=form.nombreProducto.data,
            cantidad=form.cantidad.data,
            fechaCaducidad=form.fechaCaducidad.data
        )
        db.session.add(nuevo_material)  
        db.session.commit()  
        return redirect(url_for('materiales.index')) 
    materiales = Producto.query.all()  
    return render_template('materiales.html', form=form, materiales=materiales)

@inventarioMaterbp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    material = Producto.query.get_or_404(id) 
    form = MaterialForm(obj=material) 

    if form.validate_on_submit(): 
        material.nombreProducto = form.nombreProducto.data
        material.cantidad = form.cantidad.data
        material.fechaCaducidad = form.fechaCaducidad.data
        db.session.commit()  
        return redirect(url_for('materiales.index'))

    return render_template('editar_material.html', form=form, material=material)

@inventarioMaterbp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_material(id):
    material = Producto.query.get_or_404(id)  
    db.session.delete(material)  
    db.session.commit() 
    return redirect(url_for('materiales.index'))  
