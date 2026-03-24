# Biblioteca de funciones generales

Biblioteca de funciones generales para los proyectos en Python de La Casa Del Carpintero.

Esta biblioteca cuenta con varios módulos para diversas finalidades. Por favor lee su respectiva documentación para poder acondicionar tu espacio de trabajo antes de usarlos.

## Índice

**USO**
- [Instalación](#instalación)

**MÓDULOS**
- [Conexión con Hojas de Cálculo de Google `spreadsheet`](#hojas-de-cálculo-spreadsheet)
    - [`write` Guardar en Hojas de Cálculo](#write-guardar-en-hojas-de-cálculo)
    - [`read` Cargar desde Hojas de Cálculo](#read-cargar-desde-hojas-de-cálculo)

**CONFIGURACIÓN**
- [Variables de entorno](#variables-de-entorno)

----

## Instalación

Instala esta librería por medio de **pip** con el siguiente comando:
```bash
pip install git+https://github.com/onnymm/ccc_utils.git
```

Instala las dependencias para usar la librería
```bash
pip install -r .\requirements.txt
```

Con eso estarás listo para comenzar a usar esta librería:
```py
from ccc_utils import spreadsheet
```

----

## Hojas de Cálculo `spreadsheet`

Este módulo está diseñado para obtener datos desde una hoja de cálculo de Google Sheets en formato Pandas DataFrame o para exportar un Pandas DataFrame a una hoja de cálculo.

```py
from ccc_utils import spreadsheet
```

### Funciones

#### `read` Cargar desde Hojas de Cálculo

Esta función carga un DataFrame a partir de los datos en una hoja de un archivo de Hojas de Cálculo.

> NOTA: Para leer un archivo de Hojas de Cálculo es necesario [conceder el permiso a la cuenta de servicio](#compartir-la-hoja-de-cálculo-con-la-cuenta-de-servicio) en éste.

Parámetros:
- `spreadsheet_name`: `str` Nombre del archivo de Hojas de Cálculo.
- `sheet_name`: `str` Nombre de la hoja del archivo de Hojas de Cálculo.

#### `write` Guardar en Hojas de Cálculo

Esta función escribe los datos del Pandas DataFrame provisto en una hoja de hoja de cálculo especificada.

Si el nombre de la hoja proporcionado apunta a una hoja que no existe, ésta se creará.

Para asegurar el formato de los datos en la hoja destino, es necesario tomar en cuenta que este método convierte fechas y horas en la codificación usada por Microsoft Excel y Google Sheets, en valores numéricos con decimales.

El parseo de los datos se determina por el `dtype` de la columna, así que es necesario convertir los tipos de dato necesarios antes de realizar la escritura.

Los `dtypes` a parsear son:

- `datetime64[as]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[D]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[fs]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[h]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[M]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[m]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[ms]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[ns]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[ps]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[s]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[us]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[W]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[Y]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `datetime64[μs]`: Numérico entero con fracción para valor de fecha con o sin hora.
- `timedelta64[as]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[D]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[fs]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[h]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[M]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[m]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[ms]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[ns]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[ps]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[s]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[us]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[W]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[Y]`: Numérico con fracción para valor de tiempo o duración.
- `timedelta64[μs]`: Numérico con fracción para valor de tiempo o duración.
- `category`: Texto.
- `str`: Texto.
- `string`: Texto.
- `string[pyarrow]`: Texto.
- `string[python]`: Texto.
- `object`: Texto.
- `O`: Texto.

> NOTA: Para escribir en un archivo de Hojas de Cálculo es necesario [conceder el permiso a la cuenta de servicio](#compartir-la-hoja-de-cálculo-con-la-cuenta-de-servicio) en éste.

Parámetros:
- `data`: `DataFrame` Datos a escribir en el archivo de hojas de Cálculo.
- `spreadsheet_name`: `str` Nombre del archivo de Hojas de Cálculo.
- `sheet_name`: `str` Nombre de la hoja del archivo de Hojas de Cálculo.
- `columns_start_position`: `str | None`: Posición inicial para comenzar a colocar las columnas.
- `data_start_position`: `str | None`: Posición inicial para comenzar a colocar los datos sin incluir las columnas.

### Configuración

Antes de usar este módulo se requieren una serie de configuraciones previas descritas a continuación:
- Contar con un [proyecto](#creación-de-un-proyecto-en-google-cloud) en Google Cloud.
- Tener habilitadas las [APIs](#activación-de-la-api-de-google-sheets-y-google-drive) de Google Sheets y Google Drive.
- Tener [credenciales](#creación-de-credenciales-de-una-cuenta-de-servicio) de cuenta de servicio.
- Contar con el [archivo JSON de credenciales](#obtención-de-credenciales-de-cuenta-de-servicio-en-formato-json).

Carga el archivo de credenciales en la carpeta raíz del proyecto.
El archivo deberá llamarse `spreadsheets_service_credentials.json`. En caso de requerir un nombre distinto, lo puedes especificar en las [variables de entorno](#variables-de-entorno) con el nombre de variable `CCC_SPREADSHEETS_SERVICE_JSON_CREDENTIALS` y el valor del nombre sin la extensión `.json`.

#### Creación de un proyecto en Google Cloud

Un proyecto en Google Cloud funciona como el contenedor administrativo donde se agrupan todos los recursos relacionados con la integración. En este proyecto se habilitan las APIs necesarias, se gestionan credenciales y se aplican las políticas de acceso y seguridad. Sin un proyecto, Google no permite el uso de servicios como Sheets o Drive desde aplicaciones externas.

1. Dirígete a [Google Cloud](https://cloud.google.com/).
2. Dirígete a `Consola`.
3. Selecciona `Selecciona un proyecto`:
    1. Una ventana se abrirá.
    2. Selecciona `Proyecto nuevo`
    3. Serás dirigido a un formulario para configurar tu proyecto.
4. Asígnale un nombre significativo a tu proyecto.
5. Selecciona nuevamente `Selecciona un proyecto`
6. Selecciona el proyecto que acabas de crear

#### Activación de la API de Google Sheets y Google Drive

La activación de Google Sheets API y Google Drive API permite que una aplicación externa pueda interactuar con hojas de cálculo almacenadas en Google Drive. Sheets API define las operaciones que pueden realizarse sobre las hojas (leer, escribir, actualizar), mientras que Drive API gestiona el acceso a los archivos. Ambas son necesarias para trabajar con Google Sheets de forma programática.

1. Activa la API de Google Sheets:
    1. Dentro de tu proyecto de [Google Cloud](https://cloud.google.com/) busca `APIs y servicios` y selecciónalo.
    2. Dirígete a `Biblioteca`.
    3. Busca `Google Sheets`.
    4. Entra y da clic en `Habilitar`.

2. Activa la API de Google Drive
    1. Dentro de tu proyecto de [Google Cloud](https://cloud.google.com/) busca `APIs y servicios` y selecciónalo.
    2. Dirígete a `Biblioteca`.
    3. Busca `Google Drive`.
    4. Entra y da clic en `Habilitar`.

#### Creación de credenciales de una cuenta de servicio

Una cuenta de servicio es una identidad técnica que representa a la aplicación que accederá a Google Sheets. A diferencia de una cuenta personal, no requiere inicio de sesión interactivo y está diseñada para procesos automatizados. Esta cuenta es la que Google reconoce y autoriza cuando el script intenta acceder a los servicios habilitados.

1. Dentro de tu proyecto de [Google Cloud](https://cloud.google.com/)  busca `APIs y servicios` y selecciónalo.
2. Dirígete a `Credenciales`.
3. Haz clic en `Crear credenciales`.
    1. Selecciona `Cuenta de servicio`.
    2. Llena los campos:
        - Nombre.
        - ID (Opcional, se autogenera por defecto).
    3. Haz clic en `Crear y continuar`.
    4. Otorga el rol de `Editor` a la cuenta.
    5. Haz clic en `Continuar`.
    6. Haz clic en `Listo`.

#### Obtención de credenciales de cuenta de servicio en formato JSON

El archivo de credenciales contiene la información de autenticación de la cuenta de servicio, incluyendo las claves necesarias para que el script pueda identificarse ante Google. Este archivo permite que la aplicación se autentique de forma segura y es indispensable para establecer la conexión con las APIs. Debe manejarse con cuidado, ya que concede acceso a los recursos autorizados.

1. Dentro de tu proyecto de [Google Cloud](https://cloud.google.com/)  busca `APIs y servicios` y selecciónalo.
2. Dirígete a `Credenciales`.
3. Busca tu cuenta la de servicio deseada.
4. Haz clic sobre ella.
5. Busca la sección `Claves` y selecciónala.
6. Haz clic en `Agregar clave` y `Crear clave nueva`.
7. Una ventana se abrirá.
8. Seleccióna `JSON`.
9. Se descargará un archivo JSON.

> ⚠️ Importante
>
> Guarda estas credenciales en un lugar seguro. Por ninguna razón las alojes en un repositorio público o una carpeta pública.

#### Compartir la hoja de cálculo con la cuenta de servicio

Compartir la hoja con la cuenta de servicio otorga permisos explícitos para que la aplicación pueda acceder al archivo específico. Aunque la cuenta de servicio tenga credenciales válidas, no puede interactuar con ningún documento si no se le concede acceso directo. Este paso garantiza un control preciso sobre qué archivos puede leer o modificar el script.

1. Dentro de tu proyecto de [Google Cloud](https://cloud.google.com/)  busca `APIs y servicios` y selecciónalo.
2. Dirígete a `Credenciales`.
3. Busca tu cuenta la de servicio deseada.
4. Copia el correo de la cuenta de servicio
5. Abre tu hoja de cálculo.
6. Haz clic en `Compartir`.
7. Pega la cuenta de correo.
8. Asígnale permisos de `Editor`.
9. Haz clic en `Guardar`.

----

## Variables de entorno

Esta librería permite personalizar su comportamiento mediante variables de entorno, las cuales se utilizan para definir configuraciones como nombres personalizados de archivos requeridos u otros valores que necesiten diferir de la configuración predeterminada. Este mecanismo proporciona mayor flexibilidad, facilita la adaptación a distintos entornos y ayuda a evitar conflictos con otros proyectos, archivos o dependencias.

Las variables de entorno pueden definirse en el archivo .env. En caso de que alguna no sea especificada, la librería utilizará automáticamente su valor prestablecido.

A continuación se listan las variables de entorno disponibles, junto con su descripción y el valor predeterminado que se aplicará si no se proporciona una configuración explícita:

| Nombre de la variable                       | Descripción                                                                                                                               | Valor prestablecido                  |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| `CCC_SPREADSHEETS_SERVICE_JSON_CREDENTIALS` | Nombre de archivo de credenciales de cuenta de servicio en Google Cloud para el módulo [Hojas de Cálculo](#hojas-de-cálculo-spreadsheet). | `"spreadsheets_service_credentials"` |



