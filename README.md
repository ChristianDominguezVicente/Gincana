MANUAL DE INSTALACIÓN:
1. Crear un entorno virtual: python -m venv /ruta_del_proyecto/venv
2. Instalar todas las dependencias: pip install -r requirements.txt
3. Instalar en el equipo Redis para el funcionamiento de celery:
   - Windows: https://github.com/tporadowski/redis/releases
     - Verificar funcionamiento: Ir a la carpeta de Program Files donde esta instalado redis, ejecutar redis-cli.exe y escribir en la terminal que aparecerá PING, debe contestar PONG.
   - Linux:
     - Instación: sudo apt install redis-server
     - Iniciar servicio: sudo systemctl start redis-server
     - Habilitar servicio: sudo systemctl enable redis-server
     - Verificar funcionamiento: redis-cli ping
4. Instalar en el equipo wkhtmltopdf para poder generar PDFs:
   - Windows: https://wkhtmltopdf.org/downloads.html
     - Después de instalarlo: añadir wkhtmltopdf al PATH del sistema
     - Verificar instalación: wkhtmltopdf --version
   - Linux: sudo apt installa wkhtmltopdf

MANUAL DE ARRANQUE:
1. .\venv\Scripts\activate
2. python manage.py runserver
3. celery -A gincana.celery worker --pool=solo -l info
4. celery -A gincana beat -l INFO

NOTAS:
En la aplicación web se puede crear Usuarios, iniciar y cerrar sesión. Crear Gincanas, eliminarlas e actualizarlas.

Se ha seguido el siguiente tutorial para la estructura de la aplicación web:
https://www.youtube.com/watch?v=e6PkGDH4wWA

Por otra parte, se han seguido para modificar los usuario por defecto de django los siguientes videos:
https://www.youtube.com/watch?v=lNxQkW1kjto
https://www.youtube.com/watch?v=HTIr44gLvxY
https://www.youtube.com/watch?v=UTJ_Dr5I5sQ
https://www.youtube.com/watch?v=Owg7ZzSRvUw

Sidebar con bootstrap:
https://www.youtube.com/watch?v=i7uJAOFEd4g
https://getbootstrap.com/docs/5.0/examples/sidebars/#
https://dev.to/codeply/bootstrap-5-sidebar-examples-38pb
https://getbootstrap.com/docs/5.0/customize/color/
https://www.youtube.com/watch?v=fiv1_J-TmEI

Desabilitar Caché:
https://stackoverflow.com/questions/11474345/force-browser-to-refresh-css-javascript-etc

Modal añadir paradas:
https://www.youtube.com/watch?v=BJ5M9RYpdt4

Localizaciones:
https://www.youtube.com/watch?v=ZLuXPwug490&list=PLxooeC3-xaNfmKrHLU6IFpEYa3RVbh-Y6&index=4

Reloj:
https://github.com/monim67/django-bootstrap-datepicker-plus

Se usa Celery para comprobaciones periodicas en el servidor:
https://www.youtube.com/playlist?list=PLLz6Bi1mIXhHKA1Szy2aj9Jbs6nw9fhNY

Enlace Imagen Docker: https://drive.google.com/file/d/1O39jeDr7VpnAvs_acjeiKVo0pKZ2WTrW/view?usp=drive_link

Crear la imagen de Docker: docker build -t gincana .

Iniciar Docker Container con la aplicación: docker run -d --name gincanaContainer -p 8000:8000 gincana

Detener Docker Container: docker stop gincana 

Borrar Docker Container: docker rm gincanaContainer

Exportar Imagen Docker: docker save -o gincana.zip gincana

QR: https://www.youtube.com/watch?v=xk8K3MNu81I
