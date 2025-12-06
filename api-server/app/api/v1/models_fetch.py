from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep, UserDep
from app.repositories import secrets_repo
from app.core.security import fernet_decrypt_data
import requests
import cohere
import os

router = APIRouter()

# Simple in-memory cache: { "provider_name": { "timestamp": float, "models": [...] } }
# In a production app, use Redis or similar.
MODEL_CACHE = {}
CACHE_DURATION_SECONDS = 3600 * 24  # Cache for 24 hours

@router.get("/{provider_name}")
def get_provider_models(
    provider_name: str,
    db: SessionDep,
    user: UserDep,
):
    """
    Fetch models from a specific provider using the user's stored secret key.
    """
    # 1. Find the secret for this provider belonging to the user
    # We need to search through the user's secrets to find one that matches the provider name.
    # This assumes the 'name' in secrets table corresponds to the provider name (e.g. "OpenAI", "Anthropic")
    
    # Note: In a real scenario, you might want to pass the secret_id directly to be precise,
    # but searching by name is a reasonable UX shortcut if names are consistent.
    user_secrets = secrets_repo.get_secrets_by_user_id(db, user_id=user.id, skip=0, limit=100)
    
    target_secret = None
    for secret in user_secrets:
        if secret.name.lower() == provider_name.lower():
            target_secret = secret
            break
            
    if not target_secret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No secret found for provider '{provider_name}'. Please add a key first."
        )

    # Decrypt the key
    api_key = fernet_decrypt_data(target_secret.key)

    # 2. Check Cache (Optional: could key by provider only, or provider+user if keys have different access)
    # For simplicity, we'll just fetch fresh for now or implement a simple cache later if needed.
    
    try:
        if provider_name.lower() == "openai":
            return fetch_openai_models(api_key)
        elif provider_name.lower() == "anthropic":
            return fetch_anthropic_models(api_key)
        elif provider_name.lower() == "cohere":
            return fetch_cohere_models(api_key)
        elif provider_name.lower() == "groq":
            return fetch_groq_models(api_key)
        elif provider_name.lower() == "google":
             return fetch_google_models(api_key)
        else:
             raise HTTPException(status_code=400, detail=f"Provider '{provider_name}' not supported for auto-fetch.")
             
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_openai_models(api_key: str):
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Extract just the IDs
    return [model["id"] for model in data["data"]]

def fetch_anthropic_models(api_key: str):
    url = "https://api.anthropic.com/v1/models"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01" 
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return [model["id"] for model in data["data"]]

def fetch_cohere_models(api_key: str):
    # Using the SDK as per example, or raw request. SDK is safer if installed.
    # If cohere is not installed, we can use requests.
    # "Bearer authentication of the form Bearer <token>"
    url = "https://api.cohere.com/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return [model["name"] for model in data["models"]]

def fetch_groq_models(api_key: str):
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return [model["id"] for model in data["data"]]

def fetch_google_models(api_key: str):
    # Google uses query param ?key=API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Google returns "models/gemini-pro", we usually just want "gemini-pro" or the full string?
    # The user's example showed "models/gemini-1.5-flash". 
    # Let's return the 'name' field which usually includes 'models/' prefix, 
    # but often users just want the ID. Let's strip 'models/' if present for cleaner UI, 
    # or keep it if the provider expects it. 
    # Usually for LiteLLM/etc you might need just the ID.
    models = []
    for m in data.get("models", []):
        name = m["name"]
        if name.startswith("models/"):
            name = name.replace("models/", "")
        models.append(name)
    return models
