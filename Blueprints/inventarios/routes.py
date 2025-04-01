from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

from forms import GalletaForm
from models import Galleta,db
inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/', methods=['GET', 'POST'])
def index():
    form = GalletaForm()
    if form.validate_on_submit():
        nueva_galleta = Galleta(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            existencias=form.existencias.data,
            precio=form.precio.data,
            gramaje=form.gramaje.data,
            vidaAnaquel=form.vidaAnaquel.data
        )
        db.session.add(nueva_galleta)
        db.session.commit()
        return redirect(url_for('inventario.index'))

    galletas = Galleta.query.all()
    return render_template('inventario.html', form=form, galletas=galletas)

@inventario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_galleta(id):
    galleta = Galleta.query.get_or_404(id)
    form = GalletaForm(obj=galleta)
    if form.validate_on_submit():
        galleta.nombre = form.nombre.data
        galleta.descripcion = form.descripcion.data
        galleta.existencias = form.existencias.data
        galleta.precio = form.precio.data
        galleta.gramaje = form.gramaje.data
        galleta.vidaAnaquel = form.vidaAnaquel.data
        db.session.commit()
        return redirect(url_for('inventario.index'))

    return render_template('editar_galleta.html', form=form, galleta=galleta)

@inventario_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_galleta(id):
    galleta = Galleta.query.get_or_404(id)
    db.session.delete(galleta)
    db.session.commit()
    return redirect(url_for('inventario.index'))
