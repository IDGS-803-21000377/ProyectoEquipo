from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Receta, Ingrediente, RecetaIngrediente
from forms import RecetaForm, IngredienteForm

recetas_bp = Blueprint('recetas', __name__, url_prefix='/recetas')


@recetas_bp.route('/', methods=['GET'])
def lista():
    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/crear', methods=['GET', 'POST'])
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


@recetas_bp.route('/ingredientes', methods=['POST'])
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


@recetas_bp.route('/editar/<int:id>', methods=['POST'])
def editar_receta(id):
    receta = Receta.query.get_or_404(id)
    nuevo_nombre = request.form.get('nuevo_nombre')
    nueva_descripcion = request.form.get('nueva_descripcion')

    if nuevo_nombre:
        receta.nombre = nuevo_nombre
    if nueva_descripcion:
        receta.descripcion = nueva_descripcion

    db.session.commit()
    flash("Receta actualizada correctamente", "success")
    return redirect(url_for('recetas.crear_receta'))


@recetas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    
    # Primero eliminar las relaciones con ingredientes
    RecetaIngrediente.query.filter_by(receta_id=id).delete()
    
    # Luego eliminar la receta
    db.session.delete(receta)
    db.session.commit()
    
    flash("Receta eliminada correctamente", "success")
    return redirect(url_for('recetas.crear_receta'))
