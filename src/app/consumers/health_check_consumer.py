from channels.generic.websocket import AsyncWebsocketConsumer

class HealthCheckConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data="200")

    async def disconnect(self, close_code):
        pass