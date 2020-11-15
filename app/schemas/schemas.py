from app.schemas.game_schema import *
from app.schemas.lobby_schema import *
from app.schemas.user_schema import *

'''
Las clases estan divididas según los siguientes criterios (priorizados):
1. Endpoint en los que participan
2. Si es parte de una request o una respuesta
3. Intentar ocultar información que no debería poder accederse
       (i.e.: en vez de reutilizar una clase que comparte más información,
       creamos una distinta más pequeña)
=> Quiźas se puede utilizar el tipo Optional para poder reutilizar clases

Ejemplo de uso:

Estamos jugando, se acaba de resolver que vamos a ser el ministro,
 y ahora nuestro cliente debería mostrarnos las cartas de proclamación
 de las cuales podemos elejir.

El front end manda una GET request a

localhost:8080/<game_id>/minister

internamente (con jwt) se verifica que realmente seamos nosotros
 (el ministro) los que pedimos la información, y responde devolviendo
 una instancia de MinisterProc
'''