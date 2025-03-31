from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required,LoginManager
from models import db, Receta, Ingrediente, RecetaIngrediente
from forms import RecetaForm, IngredienteForm

recetas_bp = Blueprint('recetas', __name__, url_prefix='/recetas')

@recetas_bp.route('/', methods=['GET'])
@login_required
def lista():
    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/crear', methods=['GET', 'POST'])
@login_required 
def crear_receta():
    receta_form = RecetaForm()
    ingrediente_form = IngredienteForm()

    # Consulta los ingredientes disponibles en la base de datos
    ingredientes = Ingrediente.query.all()
    recetas = Receta.query.all()

    # Asigna las opciones del Select dinámicamente a cada subformulario de ingredientes
    for ingr_form in receta_form.ingredientes:
        ingr_form.ingrediente_id.choices = [(i.id, i.nombre) for i in ingredientes]

    if receta_form.validate_on_submit():
        nueva_receta = Receta(
            nombre=receta_form.nombre.data,
            descripcion=receta_form.descripcion.data
        )
        db.session.add(nueva_receta)
        db.session.flush()  # Obtener el ID antes de agregar ingredientes

        for ingr_form in receta_form.ingredientes:
            ri = RecetaIngrediente(
                receta_id=nueva_receta.id,
                ingrediente_id=ingr_form.ingrediente_id.data,
                cantidad=ingr_form.cantidad.data
            )
            db.session.add(ri)

        db.session.commit()
        flash("Receta creada con éxito", "success")
        return redirect(url_for('recetas.crear_receta'))

    return render_template(
        "recetas.html",
        receta_form=receta_form,
        ingrediente_form=ingrediente_form,
        ingredientes=ingredientes,
        recetas=recetas
    )

@recetas_bp.route('/editar/<int:id>', methods=['POST'])
@login_required 
def editar_receta(id):
    receta = Receta.query.get_or_404(id)
    nuevo_nombre = request.form.get('nuevo_nombre')
    nueva_descripcion = request.form.get('nueva_descripcion')

    if not nuevo_nombre or not nueva_descripcion:
        flash("Todos los campos son obligatorios para editar la receta.", "error")
    else:
        receta.nombre = nuevo_nombre
        receta.descripcion = nueva_descripcion
        db.session.commit()
        flash("Receta actualizada correctamente.", "success")

    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required 
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)

    # También eliminamos los ingredientes relacionados
    RecetaIngrediente.query.filter_by(receta_id=receta.id).delete()

    db.session.delete(receta)
    db.session.commit()
    flash("Receta eliminada correctamente.", "success")

    return redirect(url_for('recetas.crear_receta'))



@recetas_bp.route('/ingredientes', methods=['POST'])
@login_required 
def gestionar_ingredientes():
    ingrediente_form = IngredienteForm()
    if ingrediente_form.validate_on_submit():
        nombre = ingrediente_form.nombre.data.strip()
        existente = Ingrediente.query.filter_by(nombre=nombre).first()

        if existente:
            flash("Este ingrediente ya existe.", "warning")
        else:
            nuevo = Ingrediente(nombre=nombre)
            db.session.add(nuevo)
            db.session.commit()
            flash("Ingrediente agregado exitosamente.", "success")

    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/ingredientes/editar/<int:id>', methods=['POST'])
@login_required 
def editar_ingrediente(id):
    nombre = request.form.get('nuevo_nombre')
    ingrediente = Ingrediente.query.get_or_404(id)

    if not nombre:
        flash("El nombre es obligatorio.", "error")
    else:
        ingrediente.nombre = nombre
        db.session.commit()
        flash("Ingrediente actualizado correctamente.", "success")

    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/ingredientes/eliminar/<int:id>', methods=['POST'])
@login_required 
def eliminar_ingrediente(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    db.session.delete(ingrediente)
    db.session.commit()
    flash("Ingrediente eliminado correctamente.", "success")
    return redirect(url_for('recetas.crear_receta'))
