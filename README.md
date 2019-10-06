# 3 Way CRUD

# Requerimientos
- Python 3.7+. Verificar quie se este usando esta `python --version`. En algunos casos puede ser necesario usar la direccion completa del ejecutable.

# Preparación
1. Crear el ambiente virtual de Python `python3.7 -m venv pyenv`. No es requerido, pero es recomendado, si no se va a usar saltar al paso 2.
1. Abrir el ambiente virtual de Python `.\pyenv\Scripts\Activate.ps1` (Powershell). En caso de CMD utilizar `.\pyenv\Scripts\activate.bat` y va a comenzar la terminal en el ambiente virtual. Esto se puede verificar con el indicador `(pyenv)` que deberia aparecer a inicio de la ultima linea en la terminal.
2. Instalar los requerimientos utilizando `pip install -r requirements.txt`.
3. Copiar `config.samle.py` a `config.py` e ingresar credenciales para bases de datos maestro.
3. Crear las tablas vacias con ` env FLASK_APP=app_api flask apps create-tables`.

# Manual de uso
1. Abrir el ambiente virtual de Python `.\pyenv\Scripts\Activate.ps1` (Powershell). En caso de CMD utilizar `.\pyenv\Scripts\activate.bat` y va a comenzar la terminal en el ambiente virtual. Esto se puede verificar con el indicador `(pyenv)` que deberia aparecer a inicio de la ultima linea en la terminal.
2. Para correr el programa escribir `env FLASK_APP=main.py flask run`.

