from django.core.management import call_command
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateSuperuserCommandTest(TestCase):

    def test_create_superuser(self):
        """Test that a superuser is created with the given environment variables."""
        with override_settings(DJANGO_SUPERUSER_USERNAME='admin',
                               DJANGO_SUPERUSER_EMAIL='admin@admin.com',
                               DJANGO_SUPERUSER_PASSWORD='password'):
            # Ensure no users exist initially
            self.assertEqual(User.objects.count(), 0)
            
            # Call the management command
            call_command('create_superuser')
            
            # Verify a superuser has been created
            self.assertEqual(User.objects.count(), 1)
            self.assertTrue(User.objects.filter(username='admin', is_superuser=True).exists())

    def test_no_superuser_created_if_exists(self):
        """Test that no new superuser is created if one already exists."""
        User.objects.create_superuser('existing_admin', 'admin2@admin.com', 'password')
        
        with override_settings(DJANGO_SUPERUSER_USERNAME='newadmin',
                               DJANGO_SUPERUSER_EMAIL='newadmin@admin.com',
                               DJANGO_SUPERUSER_PASSWORD='newpassword'):
            call_command('create_superuser')
            
            self.assertEqual(User.objects.count(), 1)
            self.assertTrue(User.objects.filter(username='existing_admin', is_superuser=True).exists())
            self.assertFalse(User.objects.filter(username='newadmin').exists())