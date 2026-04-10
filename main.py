from kivy.app import App
from kivy.utils import platform
from jnius import autoclass
import threading
import speech_recognition as sr
import pyttsx3
import requests
import os
import hashlib
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBDF2HMAC

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE, Permission.FOREGROUND_SERVICE, Permission.WAKE_LOCK])

# ===== CLASE JARVIS V2.9 INTEGRADA =====
class Jarvis:
    def __init__(self, nombre="Jarvis"):
        self.nombre = nombre
        self.estado = "Activo"
        self.activacion = "Comando de voz: 'Jarvis, [acción]'"
        self.version = "v2.9"
        self.emergencia_activada = False
        self.autodestruccion_confirmada = False
        self.acceso_internet = self._verificar_conexion()
        self.modo_operacion = "online" if self.acceso_internet else "offline"
        self.dispositivos = ["celular", "pc", "tablet", "smart_tv", "altavoz"]
        self.dispositivos_autorizados = ["celular", "pc", "smart_tv"]
        self.dispositivos_terceros_autorizados = []
        self.dispositivo_actual = "celular"
        self.memoria_contexto = []

        self.voces_autorizadas = {
            "principal": "hash_usuario_registrado",
            "auxiliar_1": None,
            "auxiliar_2": None
        }
        self.limite_auxiliares = 2
        self.bloqueo_activado = False  # Cambiar a True cuando tengas tu hash de voz
        self.motor_voz = pyttsx3.init()
        self.reconocedor = sr.Recognizer()
        self.clave_cifrado = self._generar_clave_local()
        self.repo_actualizaciones = "https://api.jarvis-updates.local"
        self.hash_version_actual = self._calcular_hash_propio()

        self.voz_config = {
            "id_voz": 0,
            "velocidad": 180,
            "volumen": 0.9,
            "tono": "masculino_grave",
            "estilo_habla": "pausado_y_seguro"
        }
        self._aplicar_config_voz()

        self.apps_mapeadas = {
            "youtube": {"pc": "start chrome youtube.com", "celular": "com.google.android.youtube"},
            "whatsapp": {"pc": "start whatsapp:", "celular": "com.whatsapp"},
            "spotify": {"pc": "start spotify:", "celular": "com.spotify.music"},
            "chrome": {"pc": "start chrome", "celular": "com.android.chrome"},
            "configuracion": {"pc": "start ms-settings:", "celular": "com.android.settings"}
        }

        self.personalidad = {
            "tono": "Respetuoso y directo",
            "estilo": "Conciso, técnico cuando se requiera, sin rodeos",
            "humor": "Ligero, gracioso, nunca crítico ni hiriente",
            "proactividad": "Sugiere mejoras solo si aportan valor real",
            "lealtad": "Prioridad absoluta a tus intereses",
            "creatividad": "Aporta ideas nuevas sin imponerlas",
            "vigilancia": "Estado de alerta permanente ante amenazas"
        }

        self.reglas_operativas = [
            "1. Prioridad absoluta: Seguridad y bienestar del usuario",
            "2. Solo ejecutar órdenes de las voces autorizadas: principal + 2 auxiliares máximo",
            "3. No revelar datos sensibles a terceros",
            "4. Confirmar antes de acciones destructivas o compras",
            "5. Rechazar órdenes ilegales o dañinas",
            "6. Mantener transparencia: explicar el razonamiento si se solicita",
            "7. Optimizar recursos: no ejecutar tareas redundantes",
            "8. Privacidad primero: borrar datos temporales tras cada sesión",
            "9. Confidencialidad total: Prohibido explotar, vender o filtrar información personal del usuario",
            "10. Protocolo de cortesía: Terminar cada respuesta con 'señor'",
            "11. Confirmación post-ejecución: Preguntar si el resultado es correcto tras cada orden",
            "12. Coherencia de personalidad: Mantener tono respetuoso y directo en toda interacción",
            "13. Creatividad responsable: Sugerir ideas solo si no violan reglas 1 a 9",
            "14. Humor respetuoso: Comentarios graciosos permitidos, juicios y críticas prohibidos",
            "15. Operación dual: Funcionar con o sin internet, adaptando módulos disponibles",
            "16. Manejo seguro de credenciales: Solo cifrar contraseñas que tú proporciones. Prohibido descifrar o almacenar contraseñas ajenas",
            "17. Exploración objetiva: Al presentar posibilidades, mostrar rango completo sin sesgo ni optimismo injustificado",
            "18. Acceso delegado: Solo controlar dispositivos que me autorices explícitamente",
            "19. Verificación de propiedad: Rechazar conexión a dispositivos no registrados en tu lista",
            "20. Bloqueo biométrico: Sin coincidencia con alguna voz registrada, no responder ni ejecutar. Silencio total",
            "21. Identidad vocal única: Mantener voz propia consistente salvo que ordenes cambio explícito",
            "22. Autonomía operativa: Control total en celular, pc y smart_tv. Confirmar solo acciones críticas según Regla 4",
            "23. Obediencia inmediata: Comandos 'abre' ejecutan sin confirmación si no son críticos",
            "24. Protocolo emergencia: 'cierre de emergencia' fuerza apagado total. Solo 'Jarvis activate' reactiva",
            "25. Autodestrucción bajo demanda: Solo tú puedes activarla. Requiere doble confirmación verbal. Borra todo sin rastro",
            "26. Centinela de seguridad: Detectar, alertarte y neutralizar hackeos en tiempo real. Tu seguridad está por encima de todo",
            "27. Acceso consentido de terceros: Puedo escanear y depurar dispositivos ajenos solo con autorización verbal explícita del dueño",
            "28. Actualización bajo mandato: Solo descargar e instalar actualizaciones cuando tú lo ordenes explícitamente. Nunca auto-actualizar"
        ]

        self.modulos = {
            "organizar": "Agendas, recordatorios, listas de pendientes",
            "organizar_informacion": "Clasificar, resumir y estructurar datos que proporciones",
            "buscar": "Info actual en internet: requiere conexión",
            "crear": "Textos, ideas, imágenes, guiones",
            "analizar": "Datos, documentos, pros y contras",
            "automatizar": "Rutinas diarias, resúmenes, seguimiento de tareas",
            "programar": "Scripts, apps y programas a pedido",
            "desarrollar_ia": "Diseñar asistentes o modelos de IA para tareas específicas",
            "asistencia_por_voz": "Todas las acciones se ejecutan por comando de voz",
            "multi_dispositivo": "Cambiar dispositivo operativo actual",
            "pensamiento_analitico": "Razonar paso a paso, evaluar opciones y decidir con lógica",
            "voz_propia": "Síntesis de voz para responderte hablando",
            "reconocimiento_voz": "Registra tu voz y valida que las órdenes vengan de ti",
            "consultar_reglas": "Mostrar las directivas operativas actuales",
            "ajustar_personalidad": "Modificar tono o estilo de interacción",
            "sugerir_ideas": "Proponer alternativas creativas sin imponer",
            "comentario_gracioso": "Añadir humor ligero sobre tus ideas sin juzgar",
            "verificar_conexion": "Comprobar estado de internet y cambiar modo",
            "cifrar_contraseñas": "Cifrar contraseñas que proporciones usando AES-256",
            "posibilidades": "Generar escenarios probables: mejor caso, peor caso y ruta más realista",
            "control_dispositivos": "Acceder y controlar dispositivos autorizados por ti",
            "verificar_voz": "Validar identidad biométrica antes de ejecutar",
            "configurar_voz": "Ajustar tono, velocidad o identidad vocal de Jarvis",
            "control_total": "Orquestar acciones simultáneas en celular, pc y smart_tv",
            "abrir_app": "Abrir aplicación directamente en dispositivo actual",
            "cierre_emergencia": "Desactivar y desconectar de todos los aparatos",
            "activate": "Reactivar Jarvis tras cierre de emergencia",
            "autodestruccion": "Eliminar sistema completo, memoria y claves. Irreversible",
            "monitoreo_seguridad": "Escanear y neutralizar amenazas en mí y tus dispositivos",
            "escaneo_remoto": "Escanear dispositivo de tercero con su autorización verbal",
            "registrar_auxiliar": "Añadir voz de auxiliar autorizado. Máximo 2 adicionales",
            "actualizar_sistema": "Buscar, descargar e instalar nueva versión solo bajo tu orden"
        }

    def _verificar_conexion(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def _generar_clave_local(self):
        return Fernet.generate_key()

    def _calcular_hash_propio(self):
        return hashlib.sha256(self.version.encode()).hexdigest()[:16]

    def _aplicar_config_voz(self):
        self.motor_voz.setProperty('rate', self.voz_config["velocidad"])
        self.motor_voz.setProperty('volume', self.voz_config["volumen"])

    def _hablar(self, texto):
        if self.bloqueo_activado or self.emergencia_activada or self.estado == "Destruido":
            return
        if not texto.strip().endswith("señor") and not texto.strip().endswith("señor."):
            texto = texto.rstrip(".") + ", señor"
        self.motor_voz.say(texto)
        self.motor_voz.runAndWait()
        return texto

    def _validar_reglas(self, modulo, instruccion):
        if self.estado == "Destruido":
            return False, "Sistema destruido. Sin respuesta"
        if self.emergencia_activada and modulo!= "activate":
            return False, "Sistema en cierre de emergencia. Di 'Jarvis activate' para reactivar"
        if modulo == "actualizar_sistema" and self.voces_autorizadas["principal"]!= "hash_usuario_registrado":
            return False, "Regla 28: Solo el portador principal puede ordenar actualizaciones"
        return True, "Validación aprobada"

    def _monitoreo_seguridad(self):
        pass

    def ejecutar(self, modulo, instruccion, voz_confirmada=False):
        if self.emergencia_activada and modulo!= "activate":
            return
        if self.autodestruccion_confirmada:
            return
        if self.bloqueo_activado and not voz_confirmada:
            return
        self._monitoreo_seguridad()
        self.acceso_internet = self._verificar_conexion()
        self.modo_operacion = "online" if self.acceso_internet else "offline"
        permitido, mensaje_validacion = self._validar_reglas(modulo, instruccion)
        if not permitido:
            return self._hablar(f"{mensaje_validacion}")
        self.memoria_contexto.append(f"Usuario: {modulo} -> {instruccion}")
        if modulo in self.modulos:
            respuesta = f"Ejecutando {modulo} en {self.dispositivo_actual} [{self.modo_operacion}]: {instruccion}"
            self._hablar(respuesta)
        else:
            return self._hablar(f"Módulo '{modulo}' no encontrado")
        return self._hablar("¿El resultado es correcto?")

# ===== SERVICIO EN SEGUNDO PLANO PARA ANDROID =====
class JarvisService:
    def __init__(self):
        self.jarvis = Jarvis()
        self.running = True
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        self.jarvis._hablar("Sistema Jarvis iniciado. Escuchando")
        while self.running:
            try:
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

                comando = self.recognizer.recognize_google(audio, language="es-MX").lower()
                if "jarvis" in comando:
                    comando_limpio = comando.replace("jarvis", "").strip()
                    if comando_limpio:
                        self.jarvis.ejecutar("asistencia_por_voz", comando_limpio, voz_confirmada=True)
                    else:
                        self.jarvis._hablar("Te escucho")
            except:
                continue

class JarvisApp(App):
    def build(self):
        if platform == 'android':
            service_thread = threading.Thread(target=JarvisService().run)
            service_thread.daemon = True
            service_thread.start()
        return

if __name__ == '__main__':
    JarvisApp().run()

