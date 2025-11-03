from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
import jwt
from jwt import PyJWKClient
import httpx
from datetime import datetime

from services.supabase_service import SupabaseService
from services.vector_service import VectorService
from services.ayurveda_service import AyurvedaService
from models.schemas import (
    PredictionRequest,
    PredictionResponse,
    GlucoseReading,
    UserProfile,
    FoodLog,
    DietarySuggestion
)

load_dotenv()

app = FastAPI(title="Ayurvedic Health Predictor API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
AUTH0_ALGORITHMS = ["RS256"]

security = HTTPBearer()

# Initialize Services
supabase_service = SupabaseService()
vector_service = VectorService()
ayurveda_service = AyurvedaService(vector_service, supabase_service)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token from Auth0"""
    token = credentials.credentials
    
    try:
        # Get Auth0 public key
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Decode and verify token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=AUTH0_ALGORITHMS,
            audience=AUTH0_API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


@app.get("/")
async def root():
    return {"message": "Ayurvedic Health Predictor API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_glucose(
    request: PredictionRequest,
    user: dict = Depends(verify_token)
):
    """Generate glucose prediction and Ayurvedic recommendations"""
    user_id = user.get("sub")
    
    try:
        # Log the food intake
        await supabase_service.log_meal(
            user_id=user_id,
            meal_items=[item.value for item in request.mealItems],
            exercise=request.exercise.dict() if request.exercise else None,
            lifestyle_factors=request.lifestyleFactors,
            dosha=request.dosha
        )
        
        # Generate prediction using Ayurvedic principles
        prediction = await ayurveda_service.generate_prediction(
            meal_items=[item.value for item in request.mealItems],
            exercise=request.exercise,
            lifestyle_factors=request.lifestyleFactors,
            dosha=request.dosha,
            user_id=user_id
        )
        
        return prediction
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating prediction: {str(e)}"
        )


@app.post("/api/glucose-reading")
async def add_glucose_reading(
    reading: GlucoseReading,
    user: dict = Depends(verify_token)
):
    """Log actual glucose monitor reading"""
    user_id = user.get("sub")
    
    try:
        result = await supabase_service.add_glucose_reading(
            user_id=user_id,
            glucose_value=reading.value,
            timestamp=reading.timestamp,
            notes=reading.notes
        )
        return {"message": "Glucose reading logged successfully", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error logging glucose reading: {str(e)}"
        )


@app.get("/api/glucose-history")
async def get_glucose_history(
    days: int = 30,
    user: dict = Depends(verify_token)
):
    """Get user's glucose reading history"""
    user_id = user.get("sub")
    
    try:
        history = await supabase_service.get_glucose_history(user_id, days)
        return {"data": history}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching glucose history: {str(e)}"
        )


@app.get("/api/profile", response_model=UserProfile)
async def get_profile(user: dict = Depends(verify_token)):
    """Get user profile"""
    user_id = user.get("sub")
    
    try:
        profile = await supabase_service.get_user_profile(user_id)
        if not profile:
            # Create default profile
            profile = await supabase_service.create_user_profile(
                user_id=user_id,
                email=user.get("email"),
                name=user.get("name")
            )
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile: {str(e)}"
        )


@app.put("/api/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfile,
    user: dict = Depends(verify_token)
):
    """Update user profile"""
    user_id = user.get("sub")
    
    try:
        updated_profile = await supabase_service.update_user_profile(
            user_id=user_id,
            profile_data=profile_data.dict(exclude_unset=True)
        )
        return updated_profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )


@app.get("/api/food-suggestions")
async def get_food_suggestions(
    condition: str = "general",
    user: dict = Depends(verify_token)
):
    """Get food suggestions for specific health conditions"""
    user_id = user.get("sub")
    
    try:
        # Get user profile for personalization
        profile = await supabase_service.get_user_profile(user_id)
        dosha = profile.get("dosha", "Vata-Pitta") if profile else "Vata-Pitta"
        
        suggestions = await ayurveda_service.get_food_recommendations(
            condition=condition,
            dosha=dosha
        )
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching food suggestions: {str(e)}"
        )


@app.get("/api/meal-history")
async def get_meal_history(
    days: int = 7,
    user: dict = Depends(verify_token)
):
    """Get user's meal history"""
    user_id = user.get("sub")
    
    try:
        history = await supabase_service.get_meal_history(user_id, days)
        return {"data": history}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching meal history: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)