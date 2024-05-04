# Plan de acción

El usuario objetivo seleccionado para este proyecto es el área de ventas de una empresa de servicios financieros que ofrece productos de crédito a sus clientes. El objetivo principal es maximizar las ganancias de la empresa mediante la identificación de patrones en los datos que puedan ayudar a predecir el riesgo de default de los clientes y optimizar las estrategias de venta de productos de crédito. 

## Preguntas de negocio:

Para orientar el análisis al área de ventas y maximizar las ganancias, podemos plantear las siguientes preguntas de negocio:

1. ¿Cuáles son las características demográficas más relevantes que afectan el riesgo de default?

2. ¿Cómo podemos utilizar el historial de pagos de los clientes en meses anteriores y su nivel de deuda para predecir qué clientes tienen mayor probabilidad de hacer default?

## Acciones propuestas:

### Visualizaciones de datos:

1. **Demografía y Default:**
  
  - Visualización: Diagramas de barras o gráficos de dispersión que muestren la relación entre características demográficas como género, nivel educativo, estado civil y la tasa de default.
  - Acción: Identificar patrones en los datos demográficos que indiquen una mayor propensión al default. Por ejemplo, si ciertos grupos demográficos tienen una tasa de default significativamente más alta, se pueden ajustar las estrategias de marketing y las políticas de concesión de crédito para mitigar este riesgo.

2. **Historial de pagos y Deuda:**

  - Visualización: Gráficos de líneas o diagramas de dispersión que ilustren la relación entre el historial de pagos en meses anteriores, el nivel de deuda y la probabilidad de default.
  - Acción: Identificar patrones en el historial de pagos y el nivel de endeudamiento que estén asociados con un mayor riesgo de default. Por ejemplo, si los clientes con un historial de pagos irregular tienen una mayor probabilidad de default, se pueden implementar estrategias proactivas para gestionar su deuda y reducir el riesgo de incumplimiento.

### Modelos predictivos:

Para maximizar las ganancias, se propone un modelo de clasificación basado en redes neuronales que identifique qué clientes tienen mayor probabilidad de hacer default. Este modelo puede entrenarse utilizando características demográficas, historial de pagos en meses anteriores y nivel de deuda como variables predictoras. A continuación, se podrían tomar decisiones basadas en las predicciones del modelo, como limitar el crédito a clientes con alta probabilidad de default o ofrecer productos financieros alternativos.

La selección del modelo óptimo se puede condicionar a la optimización de una función de ganancias que considere el costo de los falsos positivos y falsos negativos. Por ejemplo, si el costo de un falso positivo (conceder crédito a un cliente que luego hace default) es mayor que el costo de un falso negativo (rechazar crédito a un cliente solvente), se puede ajustar el umbral de decisión del modelo para minimizar este riesgo. De este modo, se maximizarían las ganancias de la empresa al reducir el número de clientes que hacen default sin sacrificar la rentabilidad de los clientes solventes.

### Métricas de evaluación:

Para el modelo de clasificación:
- Precisión
- Recall
- F1-Score
- Matriz de confusión

Para el modelo de maximización de ganancias:
- Total de ganancias obtenidas considerando el porcentaje de ganancia por dolar prestado definido (_p_).

## Conclusiones:

Con este enfoque, el área de ventas puede utilizar la información proporcionada por el análisis descriptivo y el modelo predictivo para mejorar la segmentación de clientes, personalizar las estrategias de marketing y gestionar de manera más efectiva el riesgo de default, lo que en última instancia puede contribuir a maximizar las ganancias de la empresa.
