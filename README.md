### ----- 1. Crear un entorno virtual y activarlo -----
### Para ejecutarlo debes crear un entorno virtual ya que esto lo requiere python
### - Windows: python -m venv venv
### - Mac/Linux: python3 -m venv venv
### Una vez creado el entorno virtual debemos activarlo:
### - Windows: venv\Scripts\activate
### - Mac/Linux: source venv/bin/activate

### Cuando se activa el entorno deberias ver al inicio de la linea de codigo (venv)
### Ejemplo:
### (venv) C:\Users\PC\Documents\python\todo-api>

### ----- 2. Instalar Librerias necesarias -----
### pip install fastapi uvicorn

### ----- 3. Instalar Dependencias necesarias -----
### pip install "sqlalchemy[asyncio]" aiosqlite
### -sqlalchemy[asyncio]: el ORM nos permite interactuar con la base de datos usando objetos python
### -aiosqlite: el Driver que permite a SQLAlchemy hablar con SQLite de forma asincrona (esencial ya que estamos usando FastAPI)

### ----- 4. Ejecutar servidor -----
### Para ejecutar el servidor en tu terminal raiz del proyecto debes ejecutar este codigo:
### uvicorn main:app --reload

### Felicidades ya puedes usar la API
