from typing import List, Dict, Any, Optional
from models.schemas import PredictionResponse, DietarySuggestion, Exercise
from groq import Groq
import os


class AyurvedaService:
    def __init__(self, vector_service, supabase_service):
        self.vector_service = vector_service
        self.supabase_service = supabase_service
        
        # Initialize Groq (Free and Unlimited!)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
    
    async def generate_prediction(
        self,
        meal_items: List[str],
        exercise: Optional[Exercise],
        lifestyle_factors: str,
        dosha: str,
        user_id: str
    ) -> PredictionResponse:
        """Generate comprehensive Ayurvedic analysis and glucose prediction"""
        
        # Get relevant Ayurvedic knowledge from vector DB
        meal_context = self._get_meal_context(meal_items, dosha)
        
        # Get user's historical data
        user_stats = await self.supabase_service.get_user_statistics(user_id)
        
        # Build comprehensive prompt
        prompt = self._build_analysis_prompt(
            meal_items=meal_items,
            exercise=exercise,
            lifestyle_factors=lifestyle_factors,
            dosha=dosha,
            context=meal_context,
            user_stats=user_stats
        )
        
        # Generate with Groq (Free, Fast, Unlimited!)
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Excellent quality, large context window
            messages=[
                {"role": "system", "content": "You are an expert Ayurvedic practitioner specializing in metabolic health, digestive wellness, and blood glucose management. Provide detailed, actionable advice based on Ayurvedic principles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse response
        return self._parse_groq_response(response.choices[0].message.content)
    
    def _get_meal_context(self, meal_items: List[str], dosha: str) -> str:
        """Retrieve relevant Ayurvedic context from vector database"""
        contexts = []
        
        # Search for each meal item
        for item in meal_items[:3]:  # Limit to first 3 items
            results = self.vector_service.get_food_properties(item)
            if results:
                contexts.append(results[0])
        
        # Search for dosha-specific guidance
        dosha_results = self.vector_service.search(
            f"{dosha} dietary guidelines foods to favor avoid",
            n_results=3
        )
        contexts.extend([r['document'] for r in dosha_results])
        
        # Search for glucose management
        glucose_results = self.vector_service.search(
            "blood glucose management diabetes prevention ayurveda",
            n_results=2
        )
        contexts.extend([r['document'] for r in glucose_results])
        
        return "\n\n".join(contexts)
    
    def _build_analysis_prompt(
        self,
        meal_items: List[str],
        exercise: Optional[Exercise],
        lifestyle_factors: str,
        dosha: str,
        context: str,
        user_stats: Dict[str, Any]
    ) -> str:
        """Build comprehensive prompt for Gemini"""
        
        meal_str = ", ".join(meal_items)
        exercise_str = f"{exercise.type} for {exercise.duration}" if exercise and exercise.type else "No exercise logged"
        
        prompt = f"""You are an expert Ayurvedic practitioner specializing in metabolic health, digestive wellness, and blood glucose management.

AYURVEDIC KNOWLEDGE BASE:
{context}

USER INFORMATION:
- Primary Dosha: {dosha}
- Recent Average Glucose (7 days): {user_stats.get('avg_glucose_7days', 'Not available')} mg/dL
- Meal Logs (7 days): {user_stats.get('meal_logs_7days', 0)}

CURRENT MEAL LOG:
- Foods consumed: {meal_str}
- Exercise: {exercise_str}
- Other factors: {lifestyle_factors if lifestyle_factors else "None"}

TASK:
Analyze this meal using Ayurvedic principles and provide:

1. BLOOD GLUCOSE PREDICTION: Estimate the likely blood glucose response (e.g., "Moderate rise to 120-140 mg/dL", "Stable around 90-110 mg/dL", "Significant spike above 160 mg/dL"). Consider:
   - Glycemic nature of foods consumed
   - Food combinations and order of consumption
   - Impact of exercise on glucose metabolism
   - Dosha-specific metabolic tendencies

2. AYURVEDIC EXPLANATION: Explain using concepts like:
   - Agni (digestive fire) state
   - Food combinations (compatible/incompatible)
   - Impact on doshas
   - Effects on dhatus (tissues), especially rasa (plasma) and rakta (blood)
   - Influence on liver (yakrit) and pancreas function

3. PERSONALIZED RECOMMENDATIONS: Provide 4-6 specific, actionable recommendations for:
   - Optimizing digestive health (Agni)
   - Supporting liver and pancreas function
   - Managing blood glucose naturally
   - Balancing the {dosha} dosha
   - Improving metabolism
   - Include specific herbs, spices, or practices

4. MEAL-SPECIFIC DIETARY SUGGESTIONS: For each meal (Breakfast, Lunch, Dinner, Snacks), provide:
   - Foods to favor (3-4 specific items with quantities)
   - Foods to avoid (2-3 specific items)
   - Preparation and timing notes

Focus on addressing:
- High cholesterol management
- Blood glucose regulation
- Slow metabolism improvement
- Liver health (yakrit)
- Pancreas function
- Digestive system optimization

Format your response as JSON with this structure:
{{
  "predictedGlucose": "string describing glucose prediction",
  "explanation": "detailed Ayurvedic explanation",
  "recommendations": ["recommendation 1", "recommendation 2", ...],
  "dietarySuggestions": [
    {{
      "meal": "Breakfast",
      "foodsToFavor": "specific foods with quantities",
      "foodsToAvoid": "specific foods",
      "notes": "preparation and timing guidance"
    }},
    ...
  ]
}}

Be specific with food names, quantities, and preparation methods. Ground all recommendations in Ayurvedic principles."""

        return prompt
    
    def _parse_groq_response(self, response_text: str) -> PredictionResponse:
        """Parse Gemini's response into structured format"""
        import json
        import re
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                
                # Parse dietary suggestions if present
                dietary_suggestions = None
                if 'dietarySuggestions' in data and data['dietarySuggestions']:
                    dietary_suggestions = [
                        DietarySuggestion(**sug) for sug in data['dietarySuggestions']
                    ]
                
                return PredictionResponse(
                    predictedGlucose=data.get('predictedGlucose', 'Unable to predict'),
                    explanation=data.get('explanation', ''),
                    recommendations=data.get('recommendations', []),
                    dietarySuggestions=dietary_suggestions
                )
            except json.JSONDecodeError:
                pass
        
        # Fallback parsing if JSON extraction fails
        lines = response_text.split('\n')
        return PredictionResponse(
            predictedGlucose="Moderate glucose response expected",
            explanation=response_text[:500],
            recommendations=["Consult with an Ayurvedic practitioner for personalized guidance"],
            dietarySuggestions=None
        )
    
    async def get_food_recommendations(
        self,
        condition: str,
        dosha: str
    ) -> List[Dict[str, Any]]:
        """Get food recommendations for specific health conditions"""
        
        # Map conditions to Ayurvedic queries
        condition_map = {
            "cholesterol": "high cholesterol management foods herbs",
            "glucose": "blood sugar glucose diabetes management",
            "metabolism": "slow metabolism agni digestive fire",
            "liver": "liver health yakrit detoxification",
            "pancreas": "pancreas function insulin production",
            "digestion": "digestive health gut wellness",
            "general": "balanced diet health wellness"
        }
        
        query = condition_map.get(condition.lower(), condition)
        query += f" {dosha} dosha"
        
        # Search vector database
        results = self.vector_service.search(query, n_results=10)
        
        # Process and structure results
        recommendations = []
        for result in results:
            recommendations.append({
                "context": result['document'],
                "relevance": 1 - (result['distance'] if result['distance'] else 0)
            })
        
        return recommendations