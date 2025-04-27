import asyncio
import threading
from bleak import BleakScanner, BleakClient

# --- À personnaliser ---
SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
DEVICE_NAME = "Nano33BLE"  # Adapter si nécessaire

class Pen:
    """Gère la connexion et la réception de données depuis le stylo connecté via BLE."""

    def __init__(self):
        self.client = None
        self.running = False
        self.data_callback = None  # Fonction appelée quand nouvelle donnée
        self.loop_thread = None

    async def _connect_ble(self):
        """Recherche et connexion BLE en interne (async)."""
        print("🔍 Recherche du stylo BLE...")
        devices = await BleakScanner.discover()
        arduino_address = None
        for device in devices:
            if device.name and DEVICE_NAME in device.name:
                arduino_address = device.address
                print(f"✅ Stylo trouvé : {device.name} ({device.address})")
                break

        if not arduino_address:
            raise Exception("❌ Stylo non trouvé !")

        self.client = BleakClient(arduino_address)
        await self.client.connect()
        print("🔗 Connecté au stylo BLE.")

    async def _listen_loop(self):
        """Boucle d'écoute BLE."""
        def handle_notification(sender, data):
            message = data.decode('utf-8').strip()
            print(f"📩 Reçu: {message}")
            if self.data_callback:
                self.data_callback(message)

        await self.client.start_notify(CHARACTERISTIC_UUID, handle_notification)
        print("👂 En écoute des notifications BLE...")

        while self.running:
            await asyncio.sleep(0.1)  # Laisse tourner la boucle
        await self.client.stop_notify(CHARACTERISTIC_UUID)

    def connect(self):
        """Connexion BLE, non-bloquante pour la GUI."""
        self.running = True
        self.loop_thread = threading.Thread(target=self._start_async_loop, daemon=True)
        self.loop_thread.start()

    def _start_async_loop(self):
        asyncio.run(self._async_main())

    async def _async_main(self):
        try:
            await self._connect_ble()
            await self._listen_loop()
        except Exception as e:
            print(f"❌ Erreur dans la connexion BLE: {e}")

    def stop_listening(self):
        """Stoppe l'écoute et déconnecte proprement."""
        self.running = False
        if self.client and self.client.is_connected:
            asyncio.run(self.client.disconnect())
        print("❎ Déconnecté du stylo.")

    def set_data_callback(self, callback_function):
        """Définit une fonction appelée à chaque réception de donnée."""
        self.data_callback = callback_function



if __name__ == "__main__":
    import time

    def handle_data(message):
        print(f"🎯 Message traité: {message}")

    pen = Pen()
    pen.set_data_callback(handle_data)
    pen.connect()

    try:
        print("⌛ Test du stylo en cours... Ctrl+C pour arrêter.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pen.stop_listening()





# import serial
# import threading

# class Pen:
#     """Gère la connexion et la réception de données depuis le stylo connecté via Arduino BLE."""

#     def __init__(self, port: str, baudrate: int = 9600):
#         """
#         Args:
#             port (str): Port série auquel l'arduino est connecté (ex: COM3, /dev/ttyUSB0).
#             baudrate (int): Vitesse de transmission série.
#         """
#         self.port = port
#         self.baudrate = baudrate
#         self.serial_connection = None
#         self.running = False
#         self.data_callback = None  # fonction à appeler quand nouvelle data reçue

#     def connect(self):
#         """Établit la connexion série."""
#         self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
#         print(f"Connecté à {self.port} à {self.baudrate} bauds.")

#     def start_listening(self):
#         """Démarre l'écoute des données dans un thread séparé."""
#         if not self.serial_connection:
#             raise Exception("Connexion non établie. Appelez connect() d'abord.")

#         self.running = True
#         self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
#         self.listener_thread.start()

#     def _listen_loop(self):
#         """Boucle de lecture des données série."""
#         while self.running:
#             if self.serial_connection.in_waiting > 0:
#                 line = self.serial_connection.readline().decode('utf-8').strip()
#                 if line:
#                     print(f"Reçu: {line}")
#                     if self.data_callback:
#                         self.data_callback(line)

#     def stop_listening(self):
#         """Arrête l'écoute et ferme la connexion."""
#         self.running = False
#         if self.serial_connection and self.serial_connection.is_open:
#             self.serial_connection.close()
#         print("Déconnexion du stylo.")

#     def set_data_callback(self, callback_function):
#         """Permet de définir une fonction appelée à chaque réception de donnée."""
#         self.data_callback = callback_function
