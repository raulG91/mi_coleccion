from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,DecimalField,SelectField,FileField,TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

platforms = [('Master System','Master system'),('Nintendo Nes','Nintendo Nes'),('Megadrive','Megadrive'),('Super Nintendo','Super Nintendo'),('Game boy','Game boy'),('Game boy advance','Game boy advance'),
                                               ('Game Gear','Game Gear'),('Sega Saturn','Sega Saturn'), ('Play Station 1','Play Station 1'),('Nintendo 64','Nintendo 64'),('Dreamcast','Dreamcast'),('Play Station 2','Play Station 2'),('Game Cube','Game Cube'),('Xbox','Xbox'),
                                               ('Play Station 3','Play Station 3'), ('Xbox 360','Xbox 360'),('Wii','Wii'),('Play Station 4','Play Station 4'),('Xbox one','Xbox one'),('Wii U', 'Wii U'),('Nintendo Switch','Nintendo Switch'),('Play Station 5','Play Station 5'),
                                               ('Xbox Series S/X','Xbox Series S/X'),('Nintendo DS','Nintendo DS'),
                                               ('PSP','PSP'),('PS Vita','PS Vita'),('Nintendo 3DS','Nintendo 3DS')]

genres = [('Accion','Accion'),('Aventuras','Aventuras'),('Arcade','Arcade'),('Lucha','Lucha'),('Beat \'Em Up','Beat \'Em Up'),('Hack and Slash','Hack and Slash'),('Plataformas','Plataformas'),('Disparos','Disparos'),('Estrategia','Estrategia'),
                                         ('Conduccion','Conduccion'),('Deportes','Deportes'),('Rol','Rol'),('Simulacion','Simulacion')]

regions = [('PAL','PAL'),('NTSC','NTSC'),('Other', 'Otra')]

platforms_filter = platforms.copy()
platforms_filter.insert(0,('',''))

genres_filter = genres.copy()
genres_filter.insert(0,('',''))

regions_filter = regions.copy()
regions_filter.insert(0,('',''))


status = [('Nuevo','Nuevo'),('Como nuevo','Como nuevo'),('Usado','Usado'),('Muy usado','Muy Usado')]

buyer = [('Game','Game'),('El corte ingles','El Corte Ingles'),('Media Markt','Media Markt'),
                                                      ('Xtralife','Xtralife'),('Cex','Cex'),('Fnac','Fnac'),('PC Componentes', 'PC Componentes'),('Worten','Worten'),
                                                      ('Carrefour','Carrefour'),('Ebay','Ebay'),('Wallapop','Wallapop'),('Vinted','Vinted'),('Eneba','Eneba'),('Otra','Otra')]

class NewGameForm(FlaskForm):
  name  = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
  description  = TextAreaField('Descripcion', validators=[DataRequired(),Length(max=255)])
  buy_date = DateField('Fecha compra')
  price = DecimalField('Precio (€)',places=2,rounding=None)
  platform = SelectField('Plataforma',choices=platforms)
  genre = SelectField('Genero', choices=genres)
  region = SelectField('Region',choices=regions)
  publisher = StringField('Publisher', validators=[Length(max=255)])
  status = SelectField('Estado',choices=status)
  buyer_platform = SelectField('Comprado en',choices=buyer)
  image = FileField('Imagen',name="upload-image",validators=[FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes')])
  submit = SubmitField('Guardar')

class GameDetailsForm(FlaskForm):
  name  = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
  description  = TextAreaField('Descripcion', validators=[DataRequired(),Length(max=255)])
  buy_date = DateField('Fecha compra')
  price = DecimalField('Precio (€)',places=2,rounding=None)
  platform = SelectField('Plataforma',choices=platforms)
  genre = SelectField('Genero', choices=genres)
  region = SelectField('Region',choices=regions)
  publisher = StringField('Publisher', validators=[Length(max=255)])
  status = SelectField('Estado',choices=status)
  buyer_platform = SelectField('Comprado en',choices=buyer)
  modify = SubmitField('Modificar', name = 'modify')
  delete = SubmitField("Borrar Producto", name = "delete")

class FIlterForm(FlaskForm):
  platform = SelectField('Plataforma',choices=platforms_filter)
  genre = SelectField('Genero', choices=genres_filter)
  region = SelectField('Region',choices=regions_filter)
  filter = SubmitField('Filtrar', name = 'filter_button')
  reset = SubmitField("Reset", name = "reset")