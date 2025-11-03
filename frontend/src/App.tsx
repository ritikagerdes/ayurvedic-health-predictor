import React, { useState, useCallback, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Header } from './components/Header';
import { MealLogger } from './components/MealLogger';
import { ExerciseLogger } from './components/ExerciseLogger';
import { LifestyleLogger } from './components/LifestyleLogger';
import { DoshaSelector } from './components/DoshaSelector';
import { PredictionResult } from './components/PredictionResult';
import { GlucoseMonitor } from './components/GlucoseMonitor';
import { LoginButton, LogoutButton } from './components/Auth';
import { apiClient } from './services/apiClient';
import type { PredictionData, MealItem, Exercise } from './types';

const App: React.FC = () => {
  const { isAuthenticated, isLoading: authLoading, getAccessTokenSilently } = useAuth0();
  
  const [mealItems, setMealItems] = useState<MealItem[]>([{ id: Date.now(), value: '' }]);
  const [exercise, setExercise] = useState<Exercise>({ type: '', duration: '' });
  const [lifestyleFactors, setLifestyleFactors] = useState<string>('');
  const [dosha, setDosha] = useState<string>('Vata-Pitta');
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated) {
      // Initialize API client with auth token
      getAccessTokenSilently().then(token => {
        apiClient.setToken(token);
      });
    }
  }, [isAuthenticated, getAccessTokenSilently]);

  const handlePredict = useCallback(async () => {
    const validMealItems = mealItems.filter(item => item.value.trim() !== '');
    if (validMealItems.length === 0) {
      setError("Please add at least one food item to your meal.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const token = await getAccessTokenSilently();
      const result = await apiClient.generatePrediction(
        validMealItems,
        exercise,
        lifestyleFactors,
        dosha,
        token
      );
      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [mealItems, exercise, lifestyleFactors, dosha, getAccessTokenSilently]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Header />
        <main className="container mx-auto p-4 max-w-2xl">
          <div className="bg-white rounded-lg shadow-md p-8 mt-8 text-center">
            <h2 className="text-2xl font-bold text-slate-800 mb-4">
              Welcome to Ayurvedic Health Predictor
            </h2>
            <p className="text-slate-600 mb-6">
              Track your meals, exercise, and lifestyle with personalized Ayurvedic insights.
              Get blood glucose predictions and recommendations based on ancient wisdom.
            </p>
            <LoginButton />
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">
      <Header />
      <div className="container mx-auto p-4 max-w-2xl">
        <div className="flex justify-end mb-4">
          <LogoutButton />
        </div>
      </div>
      <main className="container mx-auto p-4 max-w-2xl pb-24">
        <div className="space-y-8">
          <p className="text-center text-slate-600">
            Log your meal, exercise, and lifestyle choices to receive an Ayurvedic-based blood glucose prediction and health insights.
          </p>
          
          <GlucoseMonitor />
          <MealLogger mealItems={mealItems} setMealItems={setMealItems} />
          <ExerciseLogger exercise={exercise} setExercise={setExercise} />
          <LifestyleLogger lifestyleFactors={lifestyleFactors} setLifestyleFactors={setLifestyleFactors} />
          <DoshaSelector selectedDosha={dosha} setSelectedDosha={setDosha} />

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          {isLoading && (
            <div className="flex justify-center items-center p-6 bg-white rounded-lg shadow-md border border-slate-200">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
              <p className="ml-4 text-slate-600">Generating your Ayurvedic analysis...</p>
            </div>
          )}

          {prediction && <PredictionResult data={prediction} />}
        </div>
      </main>

      <div className="fixed bottom-0 left-0 right-0 p-4 bg-white/80 backdrop-blur-sm border-t border-slate-200 shadow-t-lg">
        <div className="container mx-auto max-w-2xl">
          <button
            onClick={handlePredict}
            disabled={isLoading || mealItems.filter(item => item.value.trim() !== '').length === 0}
            className="w-full bg-emerald-600 text-white font-bold py-3 px-4 rounded-lg shadow-lg hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors duration-300"
          >
            {isLoading ? 'Analyzing...' : 'Predict Glucose & Get Insights'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;