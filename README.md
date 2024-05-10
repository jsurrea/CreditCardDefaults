# Credit Card Defaults

Credit Card Defaults es un sistema de análisis de datos diseñado específicamente para la industria financiera. Proporciona visualizaciones interactivas y modelos de machine learning para ayudar en la toma de decisiones respecto al riesgo de no-pago por parte de clientes de tarjetas de crédito. Su diseño apoya al área de ventas de un banco, interesada en maximizar los ingresos obtenidos por concepto de intereses, pero buscando al mismo tiempo minimizar los clientes morosos.

## Instalación

1. Clona este repositorio en una instancia EC2 de AWS.
2. Ejecuta `DevOps/setup.sh`.
3. (Opcional) Configura `cron` siguiendo los pasos en `DevOps/crono_pull.sh`.

## Estructura de Directorios

- Business Analysis: Documentos relacionados con el análisis de negocio.
- Business Context: Información contextual sobre el negocio y la industria.
- Dashboard: Código fuente para el panel de visualización.
- Data Analysis: Archivos y scripts relacionados con el análisis de datos.
- Data Engineering: Scripts para la ingeniería y limpieza de datos.
- Data Science: Modelos de machine learning y análisis predictivo.
- Despliegue: Archivos finales usados en el despliegue de la aplicación.
- DevOps: Configuración y scripts de despliegue.
- Results: Resultados y conclusiones obtenidas del análisis.

### Entregables

- Reporte de trabajo en equipo: Disponible en el archivo `Results/teamwork.md`.
- Tarea 1: Las preguntas de negocio y el plan de acción se encuentran en `Business Analysis/action_plan.md`.
- Tarea 2/Soporte 1: La limpieza de datos, el alistamiento de los mismos y los datos finales se encuentran en `Data Engineering/`. 
- Tarea 3/Soporte 2: La exploración de datos se encuentra en los cuadernos Jupyter disponibles en `Data Analysis/`.
- Tarea 4/Soporte 3: Los modelos de predicción explorados se encuentran en los cuadernos Jupyter disponibles en `Data Science/`.
- Tarea 5/Soporte 4: Los archivos fuentes del tablero y sus *assets* respectivos se encuentran disponibles en `Dashboard/`.
- Tarea 6/Soporte 5: Snapshots de las máquinas lanzadas y archivos de configuración se encuentran disponibles en `DevOps/`.
- Archivos de Despliegue/Soporte 5: Modelos serializados, archivos *environment* y versión final del tablero se encuentran en `Despliegue/`.
- Repositorio Git/Soporte 6: Disponible en la dirección URL: [https://github.com/jsurrea/CreditCardDefaults](https://github.com/jsurrea/CreditCardDefaults).
- Tablero desplegado: Disponible en la dirección URL: [http://50.19.105.14:8050/](http://50.19.105.14:8050/).

## Uso

1. Ejecuta el servidor del panel de visualización con `screen -S dashboard_session -d -m python app.py`.
2. Abre un navegador web y navega a `http://50.19.105.14:8050/` para acceder al panel de Credit Card Defaults.

## Funcionalidades

- Visualizar mediante *drill-down* la probabilidad de *default* según características demográficas a través de un *treemap*.
- Visualizar por medio de KPIs los ingresos, pérdidas y ganancias esperadas asumiendo un margen de ganancia del 5% y una recuperación de cartera del 30%.
- Visualizar la evolución del estado de pago en los 6 meses anteriores de un subconjunto de 500 clientes por medio de un *Parallel Coordinates Graph*.
- Predecir la probabilidad de *default* de un nuevo cliente dadas sus características demográficas y su historial de pagos.

## Autores

- Daniela Arenas - k.arenas@uniandes.edu.co
- Haider Fonseca - h.fonseca@uniandes.edu.co
- Sebastian Urrea - js.urrea@uniandes.edu.co

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
