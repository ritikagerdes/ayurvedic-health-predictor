import type { MealItem, Exercise, PredictionData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIClient {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  private async fetch(endpoint: string, options: RequestInit = {}) {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Request failed with status ${response.status}`);
    }

    return response.json();
  }

  async generatePrediction(
    mealItems: MealItem[],
    exercise: Exercise,
    lifestyleFactors: string,
    dosha: string,
    token: string
  ): Promise<PredictionData> {
    this.setToken(token);
    
    const requestBody = {
      mealItems,
      exercise,
      lifestyleFactors,
      dosha,
    };

    return this.fetch('/api/predict', {
      method: 'POST',
      body: JSON.stringify(requestBody),
    });
  }

  async addGlucoseReading(
    token: string,
    reading: { value: number; timestamp: string; notes?: string }
  ) {
    this.setToken(token);
    
    return this.fetch('/api/glucose-reading', {
      method: 'POST',
      body: JSON.stringify(reading),
    });
  }

  async getGlucoseHistory(token: string, days: number = 30) {
    this.setToken(token);
    
    return this.fetch(`/api/glucose-history?days=${days}`);
  }

  async getProfile(token: string) {
    this.setToken(token);
    
    return this.fetch('/api/profile');
  }

  async updateProfile(token: string, profileData: any) {
    this.setToken(token);
    
    return this.fetch('/api/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  async getMealHistory(token: string, days: number = 7) {
    this.setToken(token);
    
    return this.fetch(`/api/meal-history?days=${days}`);
  }

  async getFoodSuggestions(token: string, condition: string = 'general') {
    this.setToken(token);
    
    return this.fetch(`/api/food-suggestions?condition=${condition}`);
  }
}

export const apiClient = new APIClient();