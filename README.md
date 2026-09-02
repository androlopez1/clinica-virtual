# Clínica Virtual — Asistente Conversacional de Salud

> Este README es la fuente de verdad del proyecto entre sesiones de Claude Code.
> Debe actualizarse cada vez que haya un avance real en el código o una decisión de arquitectura.
> Última actualización: 2026-09-02

---

## 🎯 Visión del producto

Asistente conversacional que actúa como primer punto de contacto para pacientes de salud. Capaz de:

- Responder preguntas generales de salud
- Orientar al usuario según sus síntomas (sin diagnóstico definitivo)
- Indicar cuándo buscar atención médica real
- A futuro: integrarse con WhatsApp, gestionar múltiples pacientes, mantener historial, conectarse a servicios médicos reales

### Consideraciones de dominio (salud) — desde el inicio, aunque no implementadas aún

- No debe presentarse como sustituto de un médico
- Evitar diagnósticos categóricos
- Incluir advertencias cuando sea necesario
- Ser conservador en las respuestas
- La arquitectura debe poder evolucionar hacia cumplimiento regulatorio

### Nota importante sobre el estado actual

El proyecto **se desvió del asistente genérico de salud** hacia una implementación de producción específica: un asistente de WhatsApp para el consultorio de la **Dra. Vanessa López Guerrero (médica geriatra, Bogotá, Colombia)**, con tarifas, flujo de agendamiento y protocolos propios de ese consultorio. Ver [app/prompts.py](app/prompts.py).

Esto significa que el proyecto saltó de **Fase 1 (MVP genérico)** directo a piezas de **Fase 2 (WhatsApp + memoria por sesión)**, sin pasar por la versión mínima. Es una decisión de producto válida, pero debe ser explícita y consciente en cada sesión.

---

## 🧠 Contexto técnico

- VM remota en Google Cloud (**e2-micro**, recursos limitados: minimizar CPU/RAM/dependencias)
- Conexión vía VS Code por SSH
- Linux (Ubuntu)
- Claude Code CLI ya configurado con API key
- **Twilio ya configurado** para el canal de WhatsApp (pendiente de conectar el webhook real)
- Lenguaje: Python (Node solo si hay razón fuerte)
- Sin sobreingeniería; código simple, pero preparado para escalar sin reescribir todo

---

## 🚀 Fases del proyecto (plan original)

### Fase 1 (MVP)
Recibe texto → lo envía a Claude → retorna respuesta. Sin DB, sin auth, sin memoria conversacional. Probado con curl.

### Fase 2
Endpoint público, integración con WhatsApp (webhooks), manejo básico de sesiones.

### Fase 3 (futuro)
Memoria conversacional persistente, DB, observabilidad (logs/métricas), múltiples usuarios, seguridad, validaciones médicas más estrictas.

---

## 🏗️ Arquitectura actual

```
Usuario (WhatsApp / curl)
        │
        ▼
   Flask (app/main.py)
   ├── GET  /health     → healthcheck
   ├── POST /chat       → prueba directa (sin historial persistente)
   └── POST /whatsapp   → webhook estilo Twilio (TwiML), historial en memoria por número
        │
        ▼
  app/claude.py → Anthropic API (Claude)
        │
        ▼
  app/prompts.py → SYSTEM_PROMPT (reglas del consultorio de la Dra. Vanessa)
```

**Framework actual: Flask** (el plan original sugería FastAPI "preferiblemente" — decisión pendiente de confirmar si se mantiene Flask o se migra).

---

## 📁 Estructura del proyecto

```
clinica-virtual/
├── app/
│   ├── __init__.py        (vacío)
│   ├── main.py             # rutas Flask: /health, /chat, /whatsapp
│   ├── claude.py           # wrapper cliente Anthropic
│   └── prompts.py          # SYSTEM_PROMPT del consultorio
├── requirements.txt        # flask, anthropic, python-dotenv
├── test_chat.sh             # script curl interactivo para /chat
├── .env / .env.example      # ANTHROPIC_API_KEY
└── README.md                 # este archivo
```

---

## 📋 Tabla de pasos (plan original de 7 pasos)

| # | Paso | Estado | Notas |
|---|------|--------|-------|
| 1 | Proponer arquitectura mínima | ✅ Hecho | Chat → Claude → respuesta |
| 2 | Definir estructura del proyecto | ✅ Hecho | `app/main.py`, `app/claude.py`, `app/prompts.py` |
| 3 | Configurar entorno | ✅ Hecho | `.venv`, `requirements.txt`, `.env` |
| 4 | Crear API mínima | ⚠️ Hecho con desviación | Se usó **Flask**, no FastAPI como sugería el plan |
| 5 | Integrar API de Claude | ⚠️ Hecho, con pendiente | Revisar `model="claude-sonnet-4-6"` en [app/claude.py](app/claude.py) — no es un ID de modelo confirmado |
| 6 | Probar el sistema (curl/navegador) | ⚠️ Parcial | `/chat` probado con `test_chat.sh`; `/whatsapp` aún sin prueba real vía Twilio |
| 7 | Sugerir mejoras futuras | ❌ Pendiente | No se ha documentado formalmente |

---

## 🔍 Hallazgos y pendientes técnicos

1. **Modelo de Claude a confirmar**: `app/claude.py` usa `claude-sonnet-4-6`. Verificar el ID correcto disponible antes de producción.
2. **Inconsistencia de puerto**: `test_chat.sh` apunta a `localhost:8000`; Flask por defecto corre en `5000`. Confirmar puerto real de ejecución.
3. **Memoria conversacional volátil**: el diccionario `conversations` en [app/main.py](app/main.py) vive en RAM del proceso — se pierde al reiniciar. Aceptable para pruebas, no para producción (ver Fase 3).
4. **Integración real con Twilio pendiente**: el endpoint `/whatsapp` existe y responde en formato TwiML, pero falta conectar el número/sandbox de Twilio para que llegue tráfico real.
5. **Framework**: decidir si se mantiene Flask o se migra a FastAPI (el plan original lo prefería).
6. **Prompt específico vs. genérico**: el `SYSTEM_PROMPT` actual es 100% específico al consultorio de la Dra. Vanessa. Si la visión es una "clínica virtual" multi-doctor/genérica, esto debe replantearse en algún punto.

---

## ▶️ Cómo correr y probar

```bash
# Activar entorno
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env   # y completar ANTHROPIC_API_KEY

# Correr servidor (confirmar puerto real)
flask --app app.main run --port 8000

# Probar /chat
./test_chat.sh

# Probar /health
curl http://localhost:8000/health
```

---

## 🗒️ Historial de avances

- **2026-09-02**: Revisión inicial del código existente. Se detecta que el proyecto ya está más allá de Fase 1 (tiene WhatsApp + memoria por número). Se crea este README para mantener contexto entre sesiones. Usuario confirma que Twilio ya está configurado.
