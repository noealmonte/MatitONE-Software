import asyncio
from bleak import BleakClient

# Adresse MAC ou UUID du périphérique (à adapter)
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # Remplace par l'adresse MAC de l'Arduino
CHARACTERISTIC_UUID = "abcdef01-1234-5678-1234-56789abcdef0"  # UUID de la caractéristique

async def notification_handler(sender, data):
    """Callback qui s'exécute quand on reçoit des données."""
    print(f"Données reçues de {sender}: {data.decode()}")

async def main():
    async with BleakClient(DEVICE_ADDRESS) as client:
        if not await client.is_connected():
            print("Impossible de se connecter à l'Arduino BLE")
            return
        
        print("Connecté à l'Arduino BLE !")
        
        # Activer les notifications
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        
        # Attendre la réception des données pendant 10 secondes
        await asyncio.sleep(10)

        # Désactiver les notifications
        await client.stop_notify(CHARACTERISTIC_UUID)

# Exécuter l'événement asyncio
asyncio.run(main())
