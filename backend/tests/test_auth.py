import pytest
from fastapi.testclient import TestClient

import sys
sys.path.append("..")

from app.main import app

import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)


class TestAuth:
    
    def test_register_new_user(self):
        """Регистрация нового пользователя"""
        import time
        unique_id = int(time.time())

        response = client.post(
            "/auth/register",
             json={
            "username": f"testuser_{unique_id}",
            "email": f"test_{unique_id}@example.com",
            "password": "test123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == f"testuser_{unique_id}"
        assert data["email"] == f"test_{unique_id}@example.com"
    
    def test_register_duplicate_email(self):
        """Регистрация с уже существующим email"""
        # Первый запрос
        client.post(
            "/auth/register",
            json={
                "username": "user1",
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        
        # Второй запрос с тем же email
        response = client.post(
            "/auth/register",
            json={
                "username": "user2",
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.text.lower()
    
    def test_login_with_valid_credentials(self):
        """Вход с правильными данными"""
        # Сначала регистрируем пользователя
        client.post(
            "/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "mypassword"
            }
        )
        
        # Пытаемся войти
        response = client.post(
            "/auth/login",
            data={
                "username": "loginuser",
                "password": "mypassword"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_with_invalid_password(self):
        """Вход с неправильным паролем"""
        # Сначала регистрируем пользователя
        client.post(
            "/auth/register",
            json={
                "username": "wrongpass",
                "email": "wrong@example.com",
                "password": "correctpass"
            }
        )
        
        # Пытаемся войти с неправильным паролем
        response = client.post(
            "/auth/login",
            data={
                "username": "wrongpass",
                "password": "wrongpass"
            }
        )
        
        assert response.status_code == 401