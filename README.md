# NPBot - Discord Version

*Más información del creador del bot original en su  [wiki](https://github.com/tplesetz/chatgpt-turbo-discord-bot/wiki).*

El siguiente bot ha sido adaptado para su uso como PNJ para rol y larp. A continuación traduciré y ampliaré la información para utilizarlo paso a paso, por lo que no son necesarios conocimientos de programación.

Si eres desarrollador y encuentras algún fallo o posible mejora, estaré encantada de ampliar el proyecto. Yo tan solo estoy empezando con Python :)

Tienes más información sobre aplicaciones de IA para larp aquí: [minadivarius/LARP-AI-Design: Repositorio destinado a la publicación de recursos y casos prácticos de aplicación de inteligencia artificial al diseño de roles en vivo. (github.com)](https://github.com/minadivarius/LARP-AI-Design)

¡Vamos a ello!

## Crear el bot en Discord

Accede al [Portal de Desarrolladores de Discord](https://discord.com/developers/applications) con tu cuenta y crea una "Nueva Aplicación".

![](https://miro.medium.com/v2/resize:fit:1012/format:webp/1*fpWfKMZLU1eNWgj456pWpg.png)


Asigna un nombre a la aplicación, acepta los términos de servicio y pulsa en "Crear".

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BYHuVlINNzhHVBczOf2Lng.png)



Selecciona la pestaña "Bot" del menú de navegación y añade uno.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yGTAfqulVL9MPqDZ9OGIkw.png)


Después habilita la opción "Message Content Intent".

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*khZ71ASO2ZwjaoM41tIHfw.png)


Pincha en el botón para copiar el token del bot. Por razones de seguridad, esta será la única vez que puedas verlo sin tener que generar otro, así que cópialo en un sitio seguro.

Expande el área llamada "OAuth2" en el menú de navegación y pincha en el botón "URL Generator". Aquí podrás seleccionar los permisos del bot para añadirlo a tu servidor de Discord. En el área de "Scopes" tendrás que seleccionar "bot" y "applications.commands".

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*11cRb3HW96HhKRh_YYG9wA.png)

Los permisos requeridos son los siguientes:

**General Permissions**

* Read Messages/View Channels

**Text Permissions**

* Send Messages
* Send Messages in Threads
* Read Message History
* Mention Everyone
* Use Slash Commands


Tras seleccionar los permisos correctos, aparecerá una URL en la parte inferior de la página. Copia esa URL y pégala en una nueva pestaña del navegador para permitir que el Bot se una a tu servidor. Puedes compartir este link con tus amigos si quieren añadir tu bot a otro servidor.

Una vez que el bot se haya unido a tu servidor, dale permisos para cualquier canal que quieras usar para interactuar con él. También puedes impedir que acceda a otros canales o categorías.

## OpenAI API Keys

Accede a tu perfil para ver tus [OpenAI API Keys](https://platform.openai.com/account/api-keys). Tendrás que crear una cuenta gratuita si aún no la tienes.

Una vez allí, crea una nueva clave y cópiala en un lugar seguro, junto al anterior token del bot.


## Configurar el bot

El bot está configurado para interpretar a un personaje concreto de mi rol en vivo ***Project Dark.ia - La insurrección de los cautivos*** (coescrito junto a ChatGPT, por cierto), que podrás descargar del [repositorio](https://github.com/minadivarius/LARP-AI-Design) anterior.

Para adaptar usar el bot y adaptarlo a nuevos proyectos, descarga todos los archivos de este repositorio (puedes hacerlo fácilmente desde la pestaña "Code > Download Zip").

Lo más importante es editar el archivo **mycontext.py** con el bloc de notas o algún programa como Visual Studio Code. En este archivo se encuentra el prompt inicial que dotará de personalidad al bot. Borra el contenido actual y escribe tu prompt entre las comillas de la variable: `prompt1="""AQUÍ"""`. Ten en cuenta que si tu prompt es demasiado largo, el bot llegará antes a su límite de memoria (actualmente de unas 3.000 palabras, entre prompts + respuestas) y tendrás que reiniciarlo, por lo que perderá el contexto anterior.

También debes editar el archivo **npbot_discord.py**. Puedes editar los siguientes elementos:
-  `chat_history`, como un pequeño prompt inicial para ChatGPT (como el nombre del personaje).
- El estado del bot en Discord (`name="Dark.ia"`)
- El nombre del comando `chat` y su descripción (`@client.tree.command(name="chat", description="Hablar con El Ordenador")`).
- La palabra "Escribiendo..." por lo que quieras que aparezca mientras se generan las respuestas del bot (`await  interaction.response.send_message("Escribiendo...", ephemeral=True, delete_after=3)`
- La `await interaction.channel.send`, sustituyendo la palabra "ORDENADOR" por el nombre de tu personaje.

También puedes añadir o modificar **parámetros** de ChatGPT, como la temperatura (un número entre el 0 y el 2, que permite disminuir o aumentar la creatividad de las respuestas). Tienes más información al respecto aquí: [Chat completion - OpenAI API](https://platform.openai.com/docs/guides/chat)

### Comandos

Existe la posibilidad de **generar otros comandos** para el bot, lo que puede ser útil para establecer interacción con distintos personajes o personalidades del mismo, o para establecer otros "modos de juego". Solo tienes que hacer un copia y pega del comando existente, y así podrás cambiar como quieras prompt inicial (añadiendo uno nuevo a la variable `prompt2` al final del archivo **mycontext.py**), para que los jugadores puedan alternar entre uno u otro.

Ten en cuenta que para que los jugadores puedan interactuar con el bot, tendrán que hacerlo sí o sí a través del comando "/chat" (o como lo hayas llamado). Si escriben únicamente en la caja de texto de Discord, el bot no recibirá ningún mensaje. Esto es bastante incómodo, pero de momento no sé cómo hacer que funcione bien con los mensajes normales.



## Ejecutando el bot

Instala el programa **Docker Desktop** desde [aquí](https://www.docker.com/products/docker-desktop/) y ábrelo.

Ve a la carpeta donde tienes todos los archivos del bot y abre una terminal (si usas Windows, escribe "cmd" en la barra del explorador de archivos de dicha carpeta).

Allí tendrás que pegar el siguiente comando y después pulsar la tecla *enter* para generar la **imagen de tu bot**:

```shell
docker build -t npbot_discord .
```

En el mismo lugar, debes crear el **contenedor del bot** haciendo lo mismo con el siguiente código, en el que debes introducir el token del bot y la API key que habías apuntado antes:

```shell
docker run -d --name npbot_discord --env DISCORD_BOT_TOKEN="TU-TOKEN" --env OPENAI_API_KEY="TU-APIKEY" npbot_discord:latest
```

Si lo has hecho todo correctamente, tu bot debería estar funcionando y conectado a Discord. Puedes **validar** esto entrando en un canal de Discord en el que hayas dado permiso al bot para ver si está conectado.


![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*LYRC6AWOqEcF4p9A-Qf-jA.png)

En ese mismo canal, ya puedes utilizar el comando "/chat" para empezar a **interactuar** con tu personaje interpretado por ChatGPT.

![](https://miro.medium.com/v2/resize:fit:1400/1*_kbGjZB2vvQtfE3Ys5ACBg.gif)

### Otras aclaraciones
El bot solo funcionará mientras tengas **Docker abierto** y el contenedor se esté ejecutando. En caso contrario, tu bot aparecerá desconectado y no podrá recibir ni responder ningún mensaje.

Si el bot se conecta tras haber sido desconectado previamente, no podrá recordar las conversaciones anteriores. El cambio de un comando a otro también genera una **pérdida del contexto** (aunque siempre puedes hacerle un resumen de lo que estaba pasando...)

Si no has cambiado nada en el bot, en tu siguiente sesión puedes abrir Docker y darle simplemente al **play** del contenedor del bot (npbot-discord), sin tener que ejecutar de nuevo los comandos para crear la imagen y el contenedor del bot.


### Editar el bot

Si quieres editar cualquier archivo del bot (por ejemplo, para cambiar el prompt), tendrás que borrar el contenedor y la imagen que has creado en Docker, para después volver a generarlas siguiendo los pasos anteriores. En este caso, no es necesario refrescar Discord, ya que los cambios se aplicarán automáticamente (pero, al tener que desconectarse y conectarse, habrá unos segundos de inactividad, y perderá el contexto previo). Si quieres modificar los comandos de Discord, sí tendrás que **reiniciarlo** todo.
