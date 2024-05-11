from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Usuario(BaseUserManager):
    def create_temp_user(self, email, nombre, apellidos, fecha_nacimiento, genero, pais, ciudad, organizacion, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        usuario = self.model(
            email = self.normalize_email(email),
            nombre = nombre, 
            apellidos = apellidos,
            fecha_nacimiento = fecha_nacimiento,
            genero = genero,
            pais = pais,
            ciudad = ciudad,
            organizacion = organizacion
        )

        usuario.set_password(password)
        return usuario
    
    def create_user(self, email, nombre, apellidos, fecha_nacimiento, genero, pais, ciudad, organizacion, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        usuario = self.model(
            email = self.normalize_email(email),
            nombre = nombre, 
            apellidos = apellidos,
            fecha_nacimiento = fecha_nacimiento,
            genero = genero,
            pais = pais,
            ciudad = ciudad,
            organizacion = organizacion
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, email, nombre, apellidos, fecha_nacimiento, genero, pais, ciudad, organizacion,  password):
        usuario = self.create_user(
            email, 
            nombre = nombre, 
            apellidos = apellidos,
            fecha_nacimiento = fecha_nacimiento,
            genero = genero,
            pais = pais,
            ciudad = ciudad,
            organizacion = organizacion,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario

class Profesor(AbstractBaseUser):
    GENDER_CHOICES = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('O', 'Otro')
    )

    COUNTRY_CHOICES = (
        ("AF", "Afghanistan"),
        ("AX", "Åland Islands"),
        ("AL", "Albania"),
        ("DZ", "Algeria"),
        ("AS", "American Samoa"),
        ("AD", "Andorra"),
        ("AO", "Angola"),
        ("AI", "Anguilla"),
        ("AQ", "Antarctica"),
        ("AG", "Antigua and Barbuda"),
        ("AR", "Argentina"),
        ("AM", "Armenia"),
        ("AW", "Aruba"),
        ("AU", "Australia"),
        ("AT", "Austria"),
        ("AZ", "Azerbaijan"),
        ("BS", "Bahamas"),
        ("BH", "Bahrain"),
        ("BD", "Bangladesh"),
        ("BB", "Barbados"),
        ("BY", "Belarus"),
        ("BE", "Belgium"),
        ("BZ", "Belize"),
        ("BJ", "Benin"),
        ("BM", "Bermuda"),
        ("BT", "Bhutan"),
        ("BO", "Bolivia (Plurinational State of)"),
        ("BQ", "Bonaire, Sint Eustatius and Saba"),
        ("BA", "Bosnia and Herzegovina"),
        ("BW", "Botswana"),
        ("BV", "Bouvet Island"),
        ("BR", "Brazil"),
        ("IO", "British Indian Ocean Territory"),
        ("BN", "Brunei Darussalam"),
        ("BG", "Bulgaria"),
        ("BF", "Burkina Faso"),
        ("BI", "Burundi"),
        ("CV", "Cabo Verde"),
        ("KH", "Cambodia"),
        ("CM", "Cameroon"),
        ("CA", "Canada"),
        ("KY", "Cayman Islands"),
        ("CF", "Central African Republic"),
        ("TD", "Chad"),
        ("CL", "Chile"),
        ("CN", "China"),
        ("CX", "Christmas Island"),
        ("CC", "Cocos (Keeling) Islands"),
        ("CO", "Colombia"),
        ("KM", "Comoros"),
        ("CG", "Congo"),
        ("CD", "Congo (the Democratic Republic of the)"),
        ("CK", "Cook Islands"),
        ("CR", "Costa Rica"),
        ("CI", "Côte d'Ivoire"),
        ("HR", "Croatia"),
        ("CU", "Cuba"),
        ("CW", "Curaçao"),
        ("CY", "Cyprus"),
        ("CZ", "Czechia"),
        ("DK", "Denmark"),
        ("DJ", "Djibouti"),
        ("DM", "Dominica"),
        ("DO", "Dominican Republic"),
        ("EC", "Ecuador"),
        ("EG", "Egypt"),
        ("SV", "El Salvador"),
        ("GQ", "Equatorial Guinea"),
        ("ER", "Eritrea"),
        ("EE", "Estonia"),
        ("SZ", "Eswatini"),
        ("ET", "Ethiopia"),
        ("FK", "Falkland Islands (Malvinas)"),
        ("FO", "Faroe Islands"),
        ("FJ", "Fiji"),
        ("FI", "Finland"),
        ("FR", "France"),
        ("GF", "French Guiana"),
        ("PF", "French Polynesia"),
        ("TF", "French Southern Territories"),
        ("GA", "Gabon"),
        ("GM", "Gambia"),
        ("GE", "Georgia"),
        ("DE", "Germany"),
        ("GH", "Ghana"),
        ("GI", "Gibraltar"),
        ("GR", "Greece"),
        ("GL", "Greenland"),
        ("GD", "Grenada"),
        ("GP", "Guadeloupe"),
        ("GU", "Guam"),
        ("GT", "Guatemala"),
        ("GG", "Guernsey"),
        ("GN", "Guinea"),
        ("GW", "Guinea-Bissau"),
        ("GY", "Guyana"),
        ("HT", "Haiti"),
        ("HM", "Heard Island and McDonald Islands"),
        ("VA", "Holy See"),
        ("HN", "Honduras"),
        ("HK", "Hong Kong"),
        ("HU", "Hungary"),
        ("IS", "Iceland"),
        ("IN", "India"),
        ("ID", "Indonesia"),
        ("IR", "Iran (Islamic Republic of)"),
        ("IQ", "Iraq"),
        ("IE", "Ireland"),
        ("IM", "Isle of Man"),
        ("IL", "Israel"),
        ("IT", "Italy"),
        ("JM", "Jamaica"),
        ("JP", "Japan"),
        ("JE", "Jersey"),
        ("JO", "Jordan"),
        ("KZ", "Kazakhstan"),
        ("KE", "Kenya"),
        ("KI", "Kiribati"),
        ("KP", "Korea (the Democratic People's Republic of)"),
        ("KR", "Korea (the Republic of)"),
        ("KW", "Kuwait"),
        ("KG", "Kyrgyzstan"),
        ("LA", "Lao People's Democratic Republic"),
        ("LV", "Latvia"),
        ("LB", "Lebanon"),
        ("LS", "Lesotho"),
        ("LR", "Liberia"),
        ("LY", "Libya"),
        ("LI", "Liechtenstein"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("MO", "Macao"),
        ("MG", "Madagascar"),
        ("MW", "Malawi"),
        ("MY", "Malaysia"),
        ("MV", "Maldives"),
        ("ML", "Mali"),
        ("MT", "Malta"),
        ("MH", "Marshall Islands"),
        ("MQ", "Martinique"),
        ("MR", "Mauritania"),
        ("MU", "Mauritius"),
        ("YT", "Mayotte"),
        ("MX", "Mexico"),
        ("FM", "Micronesia (Federated States of)"),
        ("MD", "Moldova (the Republic of)"),
        ("MC", "Monaco"),
        ("MN", "Mongolia"),
        ("ME", "Montenegro"),
        ("MS", "Montserrat"),
        ("MA", "Morocco"),
        ("MZ", "Mozambique"),
        ("MM", "Myanmar"),
        ("NA", "Namibia"),
        ("NR", "Nauru"),
        ("NP", "Nepal"),
        ("NL", "Netherlands"),
        ("NC", "New Caledonia"),
        ("NZ", "New Zealand"),
        ("NI", "Nicaragua"),
        ("NE", "Niger"),
        ("NG", "Nigeria"),
        ("NU", "Niue"),
        ("NF", "Norfolk Island"),
        ("MK", "North Macedonia"),
        ("MP", "Northern Mariana Islands"),
        ("NO", "Norway"),
        ("OM", "Oman"),
        ("PK", "Pakistan"),
        ("PW", "Palau"),
        ("PS", "Palestine, State of"),
        ("PA", "Panama"),
        ("PG", "Papua New Guinea"),
        ("PY", "Paraguay"),
        ("PE", "Peru"),
        ("PH", "Philippines"),
        ("PN", "Pitcairn"),
        ("PL", "Poland"),
        ("PT", "Portugal"),
        ("PR", "Puerto Rico"),
        ("QA", "Qatar"),
        ("RE", "Réunion"),
        ("RO", "Romania"),
        ("RU", "Russian Federation"),
        ("RW", "Rwanda"),
        ("BL", "Saint Barthélemy"),
        ("SH", "Saint Helena, Ascension and Tristan da Cunha"),
        ("KN", "Saint Kitts and Nevis"),
        ("LC", "Saint Lucia"),
        ("MF", "Saint Martin (French part)"),
        ("PM", "Saint Pierre and Miquelon"),
        ("VC", "Saint Vincent and the Grenadines"),
        ("WS", "Samoa"),
        ("SM", "San Marino"),
        ("ST", "Sao Tome and Principe"),
        ("SA", "Saudi Arabia"),
        ("SN", "Senegal"),
        ("RS", "Serbia"),
        ("SC", "Seychelles"),
        ("SL", "Sierra Leone"),
        ("SG", "Singapore"),
        ("SX", "Sint Maarten (Dutch part)"),
        ("SK", "Slovakia"),
        ("SI", "Slovenia"),
        ("SB", "Solomon Islands"),
        ("SO", "Somalia"),
        ("ZA", "South Africa"),
        ("GS", "South Georgia and the South Sandwich Islands"),
        ("SS", "South Sudan"),
        ("ES", "Spain"),
        ("LK", "Sri Lanka"),
        ("SD", "Sudan"),
        ("SR", "Suriname"),
        ("SJ", "Svalbard and Jan Mayen"),
        ("SE", "Sweden"),
        ("CH", "Switzerland"),
        ("SY", "Syrian Arab Republic"),
        ("TW", "Taiwan (Province of China)"),
        ("TJ", "Tajikistan"),
        ("TZ", "Tanzania, the United Republic of"),
        ("TH", "Thailand"),
        ("TL", "Timor-Leste"),
        ("TG", "Togo"),
        ("TK", "Tokelau"),
        ("TO", "Tonga"),
        ("TT", "Trinidad and Tobago"),
        ("TN", "Tunisia"),
        ("TR", "Türkiye"),
        ("TM", "Turkmenistan"),
        ("TC", "Turks and Caicos Islands"),
        ("TV", "Tuvalu"),
        ("UG", "Uganda"),
        ("UA", "Ukraine"),
        ("AE", "United Arab Emirates"),
        ("GB", "United Kingdom of Great Britain and Northern Ireland"),
        ("UM", "United States Minor Outlying Islands"),
        ("US", "United States of America"),
        ("UY", "Uruguay"),
        ("UZ", "Uzbekistan"),
        ("VU", "Vanuatu"),
        ("VE", "Venezuela (Bolivarian Republic of)"),
        ("VN", "Viet Nam"),
        ("VG", "Virgin Islands (British)"),
        ("VI", "Virgin Islands (U.S.)"),
        ("WF", "Wallis and Futuna"),
        ("EH", "Western Sahara"),
        ("YE", "Yemen"),
        ("ZM", "Zambia"),
        ("ZW", "Zimbabwe"),
    )

    email = models.EmailField("Correo Electrónico", unique = True, max_length=254, primary_key=True)
    nombre = models.CharField("Nombre" ,max_length=200, null=True, blank=False)
    apellidos = models.CharField("Apellidos", max_length=200, null=True, blank=False)
    imagen = models.ImageField("Imagen de Perfil", default="usuario.png", upload_to='', null=True, blank=True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default=False)
    usuario_verificado = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=False)
    genero = models.CharField("Género", max_length=1 , choices=GENDER_CHOICES, default='H', null=True)
    pais = models.CharField("País", max_length=2 , choices=COUNTRY_CHOICES, null=True)
    ciudad = models.CharField("Ciudad", max_length=200, null=True, blank=True)
    organizacion = models.CharField("Organizacion", max_length=200, null=True, blank=False)
    objects = Usuario()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'fecha_nacimiento', 'genero', 'pais', 'ciudad', 'organizacion']

    def __str__(self):
        return f'{self.nombre},{self.apellidos}'
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
class Gincana(models.Model):
    titulo = models.CharField('Nombre de la gincana', max_length=100)
    descripcion = models.TextField('Descirpción de la gincana', blank=True)
    fecha = models.DateTimeField('Fecha de creación', auto_now_add=True)
    edicion = models.DateTimeField('Edición de la gincana', null=True, blank=True)
    duracion = models.TimeField('Duración', null=True, blank=True)
    visibilidad = models.BooleanField('Visibilidad de la gincana: ', default=False)
    activa = models.BooleanField('Actividad de la gincana', default=False)
    imagen = models.ImageField("Imagen de la gincana", default="mapa.png", upload_to='', null=True, blank=True)
    imagen_oscura = models.ImageField("Imagen oscura de la gincana", default="mapa_oscuro.png", upload_to='', null=True, blank=True)
    email_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - ' + self.email_profesor.email
    
class GincanaJugada(models.Model):
    duracion = models.TimeField('Duración', null=True, blank=True)
    total_puntos = models.IntegerField('Puntuación', null=True, blank=True)
    edición = models.DateTimeField('Edición', auto_now_add=True, primary_key=True)
    gincana = models.ForeignKey(Gincana, on_delete=models.CASCADE)

    def __str__(self):
        return self.gincana.titulo + ' - ' + self.edición

class Verificacion(models.Model):
    code = models.IntegerField('Código', null=True, blank=True)
    email = models.EmailField("Correo Electrónico", unique = True, max_length=254, primary_key=True)

    def __str__(self):
        return self.code + ' - ' + self.email_profesor.email
    
class Parada(models.Model):
    orden = models.IntegerField('Orden', default=1)
    latitud = models.FloatField('Latitud')
    longitud = models.FloatField('Longitud')
    gincana = models.ForeignKey(Gincana, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.latitud) + ' - ' + str(self.longitud) + ' - ' + self.gincana.titulo
    
class Pregunta(models.Model):
    NUM = (
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    )

    enunciado = models.TextField('Enunciado')
    num_respuestas = models.IntegerField('Numero de Respuestas',choices=NUM, default=2)
    parada = models.ForeignKey(Parada, on_delete=models.CASCADE)

    def __str__(self):
        return self.enunciado + ' - ' + self.parada.gincana.titulo
    
class Respuesta(models.Model):
    respuesta = models.CharField('Respuesta',max_length=254)
    puntos = models.IntegerField('Puntos')
    es_correcta = models.BooleanField('Es Correcta/Fallo', default=False)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def __str__(self):
        return self.respuesta + ' - ' + self.pregunta.parada.gincana.titulo
