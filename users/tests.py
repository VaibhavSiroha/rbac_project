from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class RBACTests(TestCase):
    def setUp(self):
        # Create test users
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='Admin'
        )
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123',
            role='Manager'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123',
            role='User'
        )
        
        self.client = APIClient()
        
    def get_tokens(self, username, password):
        response = self.client.post(reverse('login'), {
            'username': username,
            'password': password
        })
        return response.data['access']
        
    def test_manager_cannot_delete_user(self):
        """Test that a manager cannot delete a user"""
        token = self.get_tokens('manager', 'managerpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.delete(reverse('user-delete', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_user_can_only_see_own_profile(self):
        """Test that a regular user can only see their own profile"""
        token = self.get_tokens('user', 'userpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see their own profile
        self.assertEqual(response.data[0]['username'], 'user')
        
    def test_admin_can_manage_roles(self):
        """Test that an admin can change user roles"""
        token = self.get_tokens('admin', 'adminpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(
            reverse('user-role', kwargs={'pk': self.user.id}),
            {'role': 'Manager'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the role was changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'Manager') 