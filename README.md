# Git Manager

### Descripción
Este programa ha sido desarrollado para realizar de forma más cómoda los git pull y git push en tus proyectos, sobre todo si empleas varios repositorios.
De momento este programa solo cuenta con soporte para Linux, aunque igual lo amplío a otros sistemas operativos en el futuro.

### Modo de uso
#### Archivo de Python
1. Descarga el archivo .py
2. Si no tienes Python instalado en tu PC, descárgalo desde [su web oficial](https://www.python.org/)).
3. Guarda el archivo .py en un directorio en el que tengas un entorno virtual de Python (si no lo tienes créalo ejecutando 'python3 -m venv venv' en el directorio donde guardes el .py, y a continuación ejecuta 'source venv/bin/activate' para ponerlo en marcha.
4. Añade el archivo .py los repositorios que quieras usar. Recuerda que el token, el nombre de usuario y el nombre del repositorio tienen que estar en la misma posición en las listas.
5. El modo de uso de este script es 'python3 gitmanager.py push/pull', pero es más cómodo si le asignas un alias en la terminal, para así poder llamarlo desde cualquier parte de tu PC.
6. Para añadir un alias, ve al archivo fuente de tu shell (bashrc, zshrc...) y añade 'alias push/pull=python3 camino/hasta/tu/gitmanager.py push/pull' (recuerda que los alias para push y para pull se definen por separado).
7. A partir de ahora ya puedes llamar a este script desde cualquier directorio de tu PC.

### Consideraciones
* Este es un programa para manejar desde la terminal
* Para salir del programa interrumpiendo la ejecución tienes que emplear el comando CTRL + C
