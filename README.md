# Bot de Recordatorios para Discord/Telegram

## Descripción

Este proyecto es un bot diseñado para **Discord o Telegram** que permite almacenar fechas importantes y envía recordatorios cuando se acercan o el mismo día del evento. Su propósito es ayudar a recordar cumpleaños, aniversarios y otros eventos clave.

## Características

- Agregar, editar y eliminar eventos.
- Notificaciones automáticas cuando se acerque la fecha.
- Recordatorio el mismo día del evento.
- Soporte para múltiples usuarios.
- Opcional: Configuración de tiempos de aviso (ej. 1 día antes, 1 semana antes).

## Tecnologías

- Lenguaje: Python / Node.js (según el bot elegido)
- Base de Datos: SQLite / Firebase / PostgreSQL
- API: Discord.js / discord.py / Telebot (para Telegram)
- Hosting: Heroku, Railway, VPS o local

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/tu-repositorio.git


2. Abre telegram y busca el bot "pixard" si no sale busca "FlashReminder_bot" y escribe /recordatorio



## PREGUNTAS


## Ciclo de vida del dato (5b):

**¿Cómo se gestionan los datos desde su generación hasta su eliminación en tu proyecto?**  
Se almacenan en memoria mientras el bot está en ejecución.  

**¿Qué estrategia sigues para garantizar la consistencia e integridad de los datos?**  
Se validan antes de ser guardados en la lista de recordatorios.  

**Si no trabajas con datos, ¿cómo podrías incluir una funcionalidad que los gestione de forma eficiente?**  
Usando una base de datos para que no se pierdan al reiniciar el bot.  



## Almacenamiento en la nube (5f):

**Si tu software utiliza almacenamiento en la nube, ¿cómo garantizas la seguridad y disponibilidad de los datos?**  
El bot está alojado en Railway, que mantiene el servicio activo.  

**¿Qué alternativas consideraste para almacenar datos y por qué elegiste tu solución actual?**  
Consideré VPS y Heroku, pero Railway ofrece una integración sencilla y gratuita.  

**Si no usas la nube, ¿cómo podrías integrarla en futuras versiones?**  
Agregando almacenamiento en la nube para persistencia de datos.  



## Seguridad y regulación (5i):

**¿Qué medidas de seguridad implementaste para proteger los datos o procesos en tu proyecto?**  
Uso variables de entorno para las credenciales del bot.  

**¿Qué normativas (e.g., GDPR) podrían afectar el uso de tu software y cómo las has tenido en cuenta?**  
Podría verse afectado por GDPR si almacena datos personales, pero actualmente no lo hace.  

**Si no implementaste medidas de seguridad, ¿qué riesgos potenciales identificas y cómo los abordarías en el futuro?**  
Riesgo de filtración de credenciales, mitigado con variables de entorno.  



## Implicación de las THD en negocio y planta (2e):

**¿Qué impacto tendría tu software en un entorno de negocio o en una planta industrial?**  
Automatizar recordatorios para mejorar la organización.  

**¿Cómo crees que tu solución podría mejorar procesos operativos o la toma de decisiones?**  
Facilita la gestión de fechas importantes y tareas repetitivas.  

**Si tu proyecto no aplica directamente a negocio o planta, ¿qué otros entornos podrían beneficiarse?**  
Grupos de estudio, eventos y planificación personal.  


## Mejoras en IT y OT (2f):

**¿Cómo puede tu software facilitar la integración entre entornos IT y OT?**  
Podría integrarse con sistemas de notificación en empresas.  

**¿Qué procesos específicos podrían beneficiarse de tu solución en términos de automatización o eficiencia?**  
Gestión de tareas y recordatorios en equipos de trabajo.  

**Si no aplica a IT u OT, ¿cómo podrías adaptarlo para mejorar procesos tecnológicos concretos?**  
Añadiendo integración con APIs empresariales.  



## Tecnologías Habilitadoras Digitales (2g):

**¿Qué tecnologías habilitadoras digitales (THD) has utilizado o podrías integrar en tu proyecto?**  
Telegram API, Railway y Python.  

**¿Cómo mejoran estas tecnologías la funcionalidad o el alcance de tu software?**  
Permiten comunicación en tiempo real y despliegue automático.  

**Si no has utilizado THD, ¿cómo podrías implementarlas para enriquecer tu solución?**  
Añadiendo una base de datos en la nube para mejorar la persistencia.  
