"""User-facing UI text: card/window titles, sender labels, status words.

Kept out of widget modules so no user-facing string is inlined at a call
site, mirroring `dialogue/strings.py`'s role for the dialogue layer. The
whole app is Spanish-facing; this module is the one place that changes if
that ever needs to.
"""

WINDOW_TITLE = "JarvisTEC"

CARD_TITLE_AVATAR = "Avatar"
CARD_TITLE_CAMERA = "Cámara"
CARD_TITLE_CONVERSATION = "Conversación"

SENDER_USER = "Tú"
SENDER_ASSISTANT = "JarvisTEC"

ENTRY_PLACEHOLDER = "Escribe o pulsa el micrófono…"

STATUS_MIC_IDLE = "en reposo"
STATUS_MIC_RECORDING = "grabando"
STATUS_MIC_OFF = "apagado"

STATUS_API_CONNECTED = "conectada"
STATUS_API_ERROR = "error"
STATUS_API_BUSY = "ocupada"

STATUS_IA_RULES = "reglas"

CAMERA_DISABLED_LABEL = "apagada"
CAMERA_TOGGLE_ON = "ON"
CAMERA_TOGGLE_OFF = "OFF"

MIC_BUTTON_IDLE = "MIC"
MIC_BUTTON_RECORDING = "REC"
MIC_BUTTON_PROCESSING = "···"
SEND_BUTTON = "→"
