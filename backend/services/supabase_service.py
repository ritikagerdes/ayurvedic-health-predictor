import os
from supabase import create_client, Client
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any


class SupabaseService:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
    
    async def create_user_profile(
        self,
        user_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new user profile"""
        data = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "dosha": "Vata-Pitta",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = self.client.table("user_profiles").insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by user_id"""
        result = self.client.table("user_profiles").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None
    
    async def update_user_profile(
        self,
        user_id: str,
        profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user profile"""
        profile_data["updated_at"] = datetime.utcnow().isoformat()
        
        result = self.client.table("user_profiles").update(profile_data).eq("user_id", user_id).execute()
        return result.data[0] if result.data else None
    
    async def log_meal(
        self,
        user_id: str,
        meal_items: List[str],
        exercise: Optional[Dict[str, str]] = None,
        lifestyle_factors: Optional[str] = None,
        dosha: str = "Vata-Pitta"
    ) -> Dict[str, Any]:
        """Log a meal with associated data"""
        data = {
            "user_id": user_id,
            "meal_items": meal_items,
            "exercise": exercise,
            "lifestyle_factors": lifestyle_factors,
            "dosha": dosha,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = self.client.table("meal_logs").insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_meal_history(
        self,
        user_id: str,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get user's meal history for the last N days"""
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        result = self.client.table("meal_logs").select("*").eq("user_id", user_id).gte("timestamp", cutoff_date).order("timestamp", desc=True).execute()
        
        return result.data if result.data else []
    
    async def add_glucose_reading(
        self,
        user_id: str,
        glucose_value: float,
        timestamp: datetime,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a glucose monitor reading"""
        data = {
            "user_id": user_id,
            "glucose_value": glucose_value,
            "timestamp": timestamp.isoformat(),
            "notes": notes
        }
        
        result = self.client.table("glucose_readings").insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_glucose_history(
        self,
        user_id: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get glucose reading history"""
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        result = self.client.table("glucose_readings").select("*").eq("user_id", user_id).gte("timestamp", cutoff_date).order("timestamp", desc=True).execute()
        
        return result.data if result.data else []
    
    async def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get user's health statistics"""
        # Get recent glucose readings
        recent_glucose = await self.get_glucose_history(user_id, days=7)
        
        # Calculate averages
        if recent_glucose:
            avg_glucose = sum(r["glucose_value"] for r in recent_glucose) / len(recent_glucose)
            max_glucose = max(r["glucose_value"] for r in recent_glucose)
            min_glucose = min(r["glucose_value"] for r in recent_glucose)
        else:
            avg_glucose = max_glucose = min_glucose = None
        
        # Get meal count
        recent_meals = await self.get_meal_history(user_id, days=7)
        
        return {
            "avg_glucose_7days": avg_glucose,
            "max_glucose_7days": max_glucose,
            "min_glucose_7days": min_glucose,
            "meal_logs_7days": len(recent_meals),
            "glucose_readings_7days": len(recent_glucose)
        }