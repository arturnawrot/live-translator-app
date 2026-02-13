from channels.layers import get_channel_layer
from django.test import TestCase
from asgiref.sync import async_to_sync

class TestRedisChannelLayer(TestCase):
    def test_channel_layer_send_receive(self):
        channel_layer = get_channel_layer()
        self.assertIsNotNone(channel_layer, "Channel layer is not configured")

        group_name = "test_group"
        message = {"type": "test.message", "text": "Hello, Channels!"}

        async_to_sync(channel_layer.group_add)(group_name, "test_channel")
        async_to_sync(channel_layer.group_send)(group_name, message)
        received_message = async_to_sync(channel_layer.receive)("test_channel")

        self.assertEqual(received_message, message)

        async_to_sync(channel_layer.group_discard)(group_name, "test_channel")