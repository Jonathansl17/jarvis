# Jarvis — resumen para la exposición

Tres partes, una por persona: **Jonathan** (notebooks), **Leno** (API), **Jennifer** (frontend: pingüino y emociones).

---

## Parte 1 — Notebooks (Jonathan)

**Qué es:** 10 modelos de machine learning, cada uno en su propio notebook (`notebooks/<modelo>/`), hechos de principio a fin con CRISP-DM.

**Las 6 fases de CRISP-DM en cada notebook:**

1. **Entender el problema:** qué se quiere predecir y por qué importa.
2. **Entender los datos:** el dataset se descarga con `kagglehub`, así que el notebook corre igual en Colab y en local.
3. **Preparar los datos:** valores faltantes, codificar las columnas de texto y separar train/test estratificado.
4. **Modelar:** se entrena la técnica asignada y se comparan variantes.
5. **Evaluar:** matriz de confusión, ROC, precisión/recall o error, según el tipo de modelo.
6. **Desplegar:** se guarda el modelo en `models/<nombre>.joblib`, que es el archivo que la API carga después.

**Los 10 modelos:**

| Técnica | Modelo |
|---|---|
| ARIMA (serie de tiempo) | precio de Bitcoin |
| Regresión lineal múltiple | precio de autos usados, % de grasa corporal |
| Red neuronal (MLP) | churn de telecom |
| KNN | calidad del vino |
| Árbol de decisión | retraso de vuelos |
| Regresión logística | riesgo de derrame cerebral |
| SVM | etapa de cirrosis |
| Random forest | precio del aguacate |
| Naive Bayes | tipo de hepatitis |

**Ejemplo para contar (stroke):** solo el 4.9 % de los casos son derrames, así que un modelo "normal" aprende a ignorarlos. Por eso se usó una regresión logística con **pesos balanceados**, donde cada caso de derrame cuenta como unos 20 sanos. Así el modelo detecta mucho más los casos que importan.

---

## Parte 2 — API (Leno)

**Qué es:** un servicio REST hecho con **FastAPI** (`api/`) que expone los 10 modelos.

**Endpoints:**

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | indica si el servicio está vivo |
| GET | `/models` | lista los modelos cargados |
| GET | `/models/{name}/schema` | muestra qué campos pide ese modelo |
| POST | `/predict/{name}` | recibe un JSON y devuelve la predicción |

**Cómo funciona por dentro:**

- **Registry:** al arrancar carga todos los `.joblib` **una sola vez**. En cada petición no se entrena nada.
- **Schemas (Pydantic):** validan el JSON de entrada. Si falta un dato o viene mal, responden con un error claro.
- **Adapters:** uno por modelo. Traducen el JSON "humano" al formato que espera el modelo y luego traducen la predicción de vuelta.
- **Respuestas:**
  - Los clasificadores devuelven `label`, `probability` y `threshold`.
  - Las regresiones devuelven el valor en sus unidades, más **warnings** si un dato está fuera del rango con el que se entrenó.
  - Bitcoin devuelve una lista de fechas con precio e intervalo.
- **Campos opcionales:** si vienen vacíos, se rellenan con el mismo valor que usó el notebook para los datos faltantes.

**Demo fácil:** abrir `http://localhost:8000/docs` y probar un modelo desde el navegador.

---

## Parte 3 — Frontend: pingüino y emociones (Jennifer)

**Qué es:** la app de escritorio JarvisTEC (`app/`), hecha con CustomTkinter. Habla español.

**El flujo de una pregunta:**

1. El usuario habla (Ctrl+Space) o escribe.
2. **Whisper** convierte la voz en texto.
3. Un parser decide qué modelo usar y qué datos extraer. Usa Gemini si hay API key y, si no, reglas por palabras clave. Si falta un dato, la app lo pregunta.
4. La app llama a la API.
5. Arma la respuesta y la dice en voz alta con **Piper**.

**Emociones:**

- La webcam busca la cara con **Haar cascade** (OpenCV).
- Una **CNN en ONNX** clasifica la cara, recortada a 48×48 px, en 7 emociones: feliz, triste, enojo, miedo, sorpresa, asco y neutral.
- Toma una muestra cada **2 segundos** para no cargar la máquina.
- **La emoción cambia el tono de la respuesta.** Ejemplos:
  - Feliz: "¡Genial! … Me alegra verte contento."
  - Miedo: "No te preocupes, … Estoy aquí para ayudarte."
  - Enojo: "Tranquilo, …" y la respuesta se recorta a una sola frase, calmada y corta.

**El pingüino:**

- **Estados:** reposo, escuchando, pensando y hablando.
- **Emociones:** tiene una pose y una animación en bucle para cada emoción. Refleja la emoción del usuario y hace una transición cuando esa emoción cambia.
- **Detalles de vida:** parpadea, saluda con la aleta y da un saltito después de cada respuesta.

**Cierre sugerido:** una prueba end-to-end (`python -m app.e2e`) maneja la ventana real con voz sintetizada, una frase por modelo, y confirma que todo responde sin congelarse.
