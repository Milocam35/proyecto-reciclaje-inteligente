## 💡 Sistema IoT + IA para Clasificación Inteligente de Residuos: Eco Vision

Eco Vision es un **sistema completo que combina IoT, Visión Artificial, Inteligencia Artificial, AWS Serverless y un frontend web moderno** para identificar y clasificar residuos como:

* ♻️ **Reciclable**
* 🗑️ **No reciclable**
* 🌱 **Orgánico**

El objetivo es automatizar la **recolección inteligente de residuos** en entornos domésticos, institucionales o urbanos, optimizando el manejo de desechos mediante IA.

---

## 🚀 Características Principales

| Característica | Descripción |
| :--- | :--- |
| **Clasificación de Imágenes** | Con **TensorFlow Lite ARM64** para procesamiento rápido y eficiente. |
| **Procesamiento Serverless** | Implementado con **AWS Lambda** y **S3 Trigger**. |
| **Persistencia** | Base de datos **RDS MySQL**. |
| **API Serverless** | Gestionada con **API Gateway + Lambda** (REST). |
| **Sincronización IoT** | Mediante **polling inteligente** desde el dispositivo. |
| **Módulo de Notificaciones** | En desarrollo (**SNS**). |
| **Panel Web** | Desarrollado en **React + TailwindCSS**. |
| **Gestión de Seguridad** | Autenticación y gestión de administradores con **Cognito User Pool**. |
| **Infraestructura como Código** | Gestión automática de la infraestructura con **Terraform (IaC)**. |
| **Arquitectura** | Modular, escalable y de bajo costo. |

---

## 🏗️ Arquitectura del Sistema

El sistema se divide en tres módulos principales y se gestiona completamente en AWS, utilizando Terraform para la orquestación.

### 1️⃣ Módulo: Firmware – ESP32-CAM (C)

Este módulo representa el dispositivo IoT en el borde.

* **Captura de Imágenes:** El dispositivo toma la foto del residuo.
* **Carga a S3:** Sube la imagen directamente al bucket **S3** utilizando una **URL prefirmada (presigned URL)** vía HTTPS PUT.
* **Solicitud de Clasificación:** Realiza un *polling* a la API 10 segundos después de la subida para obtener el resultado.
* **Actuación:** Muestra el resultado de la clasificación o activa componentes externos (e.g., motores de clasificación).

### 2️⃣ Módulo: Backend Serverless – AWS (Terraform + Lambdas)

El *core* de procesamiento y gestión de datos.

* **S3 Bucket:** Almacenamiento de imágenes RAW.
* **Lambda Classifier:** Procesa imágenes con **TensorFlow Lite** para la clasificación.
* **Lambda Eventos:** Gestiona la lógica de negocio; guarda y consulta detalles de los eventos en **MySQL**.
* **API Gateway REST:** Expone los *endpoints* para la comunicación (IoT, Web, Admin):
    * `/events`
    * `/stats`
    * `/notifications` (en desarrollo)
* **RDS MySQL:** Capa de persistencia centralizada.
* **VPC Privada:** Entorno seguro de ejecución para las Lambdas y RDS.
* **Cognito User Pool:** Provee autenticación y seguridad para usuarios del frontend web.

### 3️⃣ Módulo: Frontend Web – React + TailwindCSS

Interfaz de usuario para la visualización y administración.

* **Dashboard:** Visualización en tiempo real del flujo de eventos.
* **Estadísticas:** Gráficas y métricas de clasificación de residuos.
* **Panel Administrativo:** Gestión de usuarios, corrección de clasificaciones (`tipoReal`).
* **Despliegue:** Alojado en **S3** y distribuido por **CloudFront**.
* **Dominio Personalizado:** Gestionado con **Route53**.

---

## 🔄 Flujo de Clasificación (Principal)

El siguiente diagrama ilustra el flujo de datos principal para la clasificación de un residuo.

1.  **📸 Captura:** El **ESP32-CAM** captura la imagen del residuo.
2.  **☁️ Carga:** La imagen se envía directamente al **S3 bucket** mediante **presigned URL (PUT)**.
3.  **🟢 Trigger:** El evento de creación de objeto en **S3 (ObjectCreated:*)** dispara la **Lambda Classifier**.
4.  **🧠 Clasificación (Lambda):**
    * Descarga la imagen.
    * La preprocesa ($224 \times 224$ RGB).
    * La clasifica con **TensorFlow Lite FP16**.
    * Obtiene el `tipoClasificado` y `confianza`.
5.  **🗄️ Registro (API):** La Lambda envía los datos de la clasificación al endpoint `/events`.
6.  **📝 Persistencia:** El backend (`Lambda Eventos`) guarda el evento en **RDS MySQL**.
7.  **⏱️ Sincronización (IoT):** Después de 10s, el ESP32 realiza un *polling* a: `GET /events/last`.
8.  **📬 Actuación:** El ESP32 recibe la clasificación y activa los componentes necesarios.
9.  **🖥️ Visualización (Web):** El *frontend* consulta la API (`/events`, `/stats`) para visualizar historial y estadísticas.

---

## 🗂️ Estructura del Proyecto

```
.
├── docs
├── firmware
├── frontend
│   ├── public
│   └── src
│       ├── assets
│       ├── components
│       │   ├── layout
│       │   └── ui
│       │       └── charts
│       ├── context
│       ├── hooks
│       ├── pages
│       │   ├── admin
│       │   └── home
│       │       └── components
│       ├── routes
│       ├── services
│       ├── styles
│       └── utils
└── terraform
    ├── environments
    │   ├── dev
    │   └── prod
    ├── image_classifier
    │   ├── model
    │   └── utils
    ├── lambdas
    │   ├── consult_db
    │   ├── events
    │   │   ├── dto
    │   │   ├── models
    │   │   ├── repositories
    │   │   └── services
    │   ├── generate_presigned_url
    │   ├── lambda_db_init
    │   ├── notifications
    │   │   ├── dto
    │   │   ├── models
    │   │   ├── repositories
    │   │   └── services
    │   ├── stats
    │   │   ├── dto
    │   │   ├── models
    │   │   ├── services
    │   └── test_db
    ├── modules
    │   ├── api_gateway
    │   ├── cloudwatch
    │   ├── cognito
    │   ├── ecr
    │   ├── lambda
    │   │   └── lambda_builds
    │   ├── rds
    │   ├── s3
    │   ├── sns
    │   └── vpc
    └── scripts
        └── probar_subir_img
```

---

## 🧠 Modelo de IA

* **Entrenamiento:** Basado en **TensorFlow**.
* **Formato de Ejecución:** Convertido a **TensorFlow Lite FP16** para optimizar el rendimiento y la memoria en **AWS Lambda**.
* **Entrada (Input):** Imagen de **$224 \times 224$ RGB**.
* **Salida (Output):** Clasificación en una de las tres categorías:
    * `["reciclable", "noReciclable", "organico"]`

---

## 🗄️ Modelo de Datos – Evento

Un evento registra el ciclo completo de clasificación y sincronización.

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INT | Identificador único del evento. |
| `horaClasificado` | DATETIME | Momento en que la IA finalizó la clasificación. |
| `horaSincronizado` | DATETIME | Fecha en que S3 subió la imagen (se obtiene del S3 Event). |
| `duracion` | FLOAT | Tiempo total de procesamiento (`horaClasificado - horaSincronizado`). |
| `rutaImagen` | VARCHAR | Clave del objeto en el bucket S3. |
| `tipoClasificado` | VARCHAR | Resultado de la IA (`reciclable`, `noReciclable`, `organico`). |
| `tipoReal` | VARCHAR | Corrección manual del administrador (Defecto: **"NO\_REVISADO"**). |
| `admin_id` | INT | ID del administrador que realizó la corrección, si aplica. |
| `confianza` | FLOAT | Nivel de confianza del modelo de IA (0 a 1). |

### 4. 📊 Tabla `Estadistica`

Almacena métricas de desempeño del modelo de IA calculadas periódicamente (por ejemplo, mediante una Lambda programada que procesa la tabla `Evento`).

| Campo | Tipo | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO\_INCREMENT | Identificador único. |
| `fn` | FLOAT | NULL | Falsos Negativos (FN). |
| `fp` | FLOAT | NULL | Falsos Positivos (FP). |
| `vn` | FLOAT | NULL | Verdaderos Negativos (VN). |
| `vp` | FLOAT | NULL | Verdaderos Positivos (VP). |
| `precision_global` | FLOAT | NULL, CHECK ($0 \le x \le 1$) | Métrica de precisión global. |
| `recall` | FLOAT | NULL, CHECK ($0 \le x \le 1$) | Métrica de Recall (Sensibilidad). |
| `f1_score` | FLOAT | NULL, CHECK ($0 \le x \le 1$) | Métrica de F1 Score (Equilibrio entre Precisión y Recall). |
| `auc` | FLOAT | NULL, CHECK ($0 \le x \le 1$) | Área bajo la curva (AUC). |
| `fecha_creacion` | DATETIME | DEFAULT CURRENT\_TIMESTAMP | Momento del cálculo de la estadística. |

### 3. 🔔 Tabla `Notificaciones`

Registra alertas generadas por el sistema (por ejemplo, errores de hardware o éxito en la clasificación).

| Campo | Tipo | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO\_INCREMENT | Identificador único. |
| `tipo` | ENUM | NOT NULL | Tipo de alerta (`success`, `error`). |
| `mensaje` | VARCHAR(255) | NOT NULL | Contenido del mensaje. |
| `origen` | VARCHAR(100) | | Módulo que generó la notificación (e.g., 'ESP32', 'LambdaClassifier'). |
| `evento_id` | INT | FOREIGN KEY, NULL | Referencia al `Evento` que causó la notificación. |
| `fecha` | TIMESTAMP | DEFAULT CURRENT\_TIMESTAMP | Momento de la creación de la notificación. |


## 🛠️ Infraestructura como Código (Terraform)

Terraform es la herramienta utilizada para provisionar y gestionar toda la infraestructura **AWS** de forma automática y reproducible.

**Componentes creados automáticamente:**

* **S3 Buckets** y sus *triggers* de eventos.
* **AWS Lambdas** y sus **roles IAM** asociados.
* **ECR** (Elastic Container Registry) para alojar la imagen Docker del clasificador.
* **RDS MySQL** en subredes privadas.
* **VPC** completa (Subnets, Route Tables, NAT Gateway, Security Groups).
* **API Gateway REST**.
* **CloudFront** y **S3** para el *hosting* del *frontend*.
* **Cognito User Pool** para la gestión de usuarios web.
