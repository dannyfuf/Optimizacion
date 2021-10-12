# Requerimientos:
    - Python ~ 3.8.6
    - OR-Tools https://developers.google.com/optimization


# Ejecución
en el archivo mezcla.py se debe llamar a la función "mezcla" especificando los parametros solicitados. A través de la misma sea realiza todo el proceso de generación de los datos y de resolución del problema. Lo que realiza cada parámetro está especificado en el código.

## Return
La función retorna un diccionario que contiene:
- El status de la resolución, indicando si es factible o no
- El valor de la optimización
- Una lista con los valores de las variables de decisión

De manera opcional:
- El tiempo utilizado en la resolución
- Las matrices con los datos generados: de utilidades, disponibilidades y la matriz de tecnología/