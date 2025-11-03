from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MealItem(BaseModel):
    id: int
    value: str


class Exercise(BaseModel):
    type: str = ""
    duration: str = ""


class PredictionRequest(BaseModel):
    mealItems: List[MealItem]
    exercise: Optional[Exercise] = None
    lifestyleFactors: str = ""
    dosha: str = "Vata-Pitta"


class DietarySuggestion(BaseModel):
    meal: str
    foodsToFavor: str
    foodsToAvoid: str
    notes: str


class PredictionResponse(BaseModel):
    predictedGlucose: str
    explanation: str
    recommendations: List[str]
    dietarySuggestions: Optional[List[DietarySuggestion]] = None


class GlucoseReading(BaseModel):
    value: float = Field(..., description="Glucose level in mg/dL")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


class UserProfile(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    dosha: str = "Vata-Pitta"
    age: Optional[int] = None
    height: Optional[float] = None  # in cm
    weight: Optional[float] = None  # in kg
    health_goals: Optional[List[str]] = None
    health_conditions: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class FoodLog(BaseModel):
    id: Optional[int] = None
    user_id: str
    meal_items: List[str]
    exercise: Optional[dict] = None
    lifestyle_factors: Optional[str] = None
    dosha: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FoodRecommendation(BaseModel):
    name: str
    benefits: List[str]
    doshas: List[str]
    preparation_tips: Optional[str] = None
    quantity_suggestion: Optional[str] = None
    timing: Optional[str] = None