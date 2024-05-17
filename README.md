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
