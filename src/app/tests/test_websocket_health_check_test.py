from django.conf import settings
from django.test import LiveServerTestCase
from websocket import create_connection
from channels.testing import ChannelsLiveServerTestCase

class WebSocketHealthCheckTest(ChannelsLiveServerTestCase):
    def test_websocket_health_check(self):
        ws_protocol = 'wss' if settings.REDIS_SSL else 'ws'
        # Adjust the port and potentially the host, as needed
        ws_url = f"{ws_protocol}://{self.live_server_url.replace('http://', '')}/health"

        # No need to change the settings.APP_URL to self.live_server_url
        # as ChannelsLiveServerTestCase takes care of providing the correct server URL

        ws = create_connection(ws_url)

        try:
            result = ws.recv()
            self.assertEqual(result, "200")
        finally:
            ws.close()