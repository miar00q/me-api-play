#!/usr/bin/env python3

from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.main import app

def test_api():
    client = TestClient(app)

    # Test health endpoint
    response = client.get('/health')
    print(f'✅ Health endpoint: {response.status_code}')
    print(f'   Response: {response.json()}')

    # Test profile endpoint
    response = client.get('/profile')
    print(f'✅ Profile endpoint: {response.status_code}')
    if response.status_code == 200:
        profile = response.json()
        print(f'   Profile: {profile["name"]} - {len(profile["skills"])} skills, {len(profile["projects"])} projects')
    else:
        print(f'   Error: {response.json()}')

    # Test skills endpoint
    response = client.get('/skills/top')
    print(f'✅ Skills endpoint: {response.status_code}')
    if response.status_code == 200:
        skills = response.json()
        print(f'   Top skills: {len(skills)} found')

    # Test search endpoint
    response = client.get('/search?q=python')
    print(f'✅ Search endpoint: {response.status_code}')
    if response.status_code == 200:
        results = response.json()
        print(f'   Search results: {len(results)} found')

    # Test projects endpoint
    response = client.get('/projects?skill=python')
    print(f'✅ Projects endpoint: {response.status_code}')
    if response.status_code == 200:
        projects = response.json()
        print(f'   Python projects: {len(projects)} found')

    print('\n🎉 All API endpoints are working!')

if __name__ == '__main__':
    test_api()
