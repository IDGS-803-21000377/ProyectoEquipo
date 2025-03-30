from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Receta, Ingrediente, RecetaIngrediente
from forms import RecetaForm, IngredienteForm

recetas_bp = Blueprint('recetas', __name__, url_prefix='/recetas')

@recetas_bp.route('/', methods=['GET', 'POST'])
def lista():
    form = RecetaForm()

    # Rellenar las opciones del select dinámicamente
    ingredientes = Ingrediente.query.all()
    for ingr_form in form.ingredientes:
        ingr_form.ingrediente_id.choices = [(i.id, i.nombre) for i in ingredientes]

    if form.validate_on_submit():
        nueva_receta = Receta(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data
        )
        db.session.add(nueva_receta)
        db.session.flush()

        for ingr_form in form.ingredientes:
            ri = RecetaIngrediente(
                receta_id=nueva_receta.id,
                ingrediente_id=ingr_form.ingrediente_id.data,
                cantidad=ingr_form.cantidad.data
            )
            db.session.add(ri)

        db.session.commit()
        flash("Receta creada exitosamente", "success")
        return redirect(url_for('recetas.lista'))

    recetas = Receta.query.all()
    return render_template('recetas.html', form=form, recetas=recetas)

@recetas_bp.route('/ingredientes', methods=['GET', 'POST'])
def gestionar_ingredientes():
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            flash("El nombre del ingrediente es obligatorio.", "error")
        else:
            # Verificar si ya existe
            existente = Ingrediente.query.filter_by(nombre=nombre).first()
            if existente:
                flash("Este ingrediente ya existe.", "warning")
            else:
                nuevo = Ingrediente(nombre=nombre)
                db.session.add(nuevo)
                db.session.commit()
                flash("Ingrediente agregado exitosamente.", "success")

        return redirect(url_for('gestionar_ingredientes'))

    ingredientes = Ingrediente.query.all()
    return render_template("ingredientes.html", ingredientes=ingredientes)
