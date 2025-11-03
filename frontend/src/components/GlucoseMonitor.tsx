import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { apiClient } from '../services/apiClient';

interface GlucoseReading {
  value: float;
  timestamp: string;
  notes?: string;
}

export const GlucoseMonitor: React.FC = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [showInput, setShowInput] = useState(false);
  const [glucoseValue, setGlucoseValue] = useState('');
  const [notes, setNotes] = useState('');
  const [history, setHistory] = useState<GlucoseReading[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const token = await getAccessTokenSilently();
      const data = await apiClient.getGlucoseHistory(token, 7);
      setHistory(data.data || []);
    } catch (error) {
      console.error('Error loading glucose history:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!glucoseValue) return;

    setIsLoading(true);
    try {
      const token = await getAccessTokenSilently();
      await apiClient.addGlucoseReading(token, {
        value: parseFloat(glucoseValue),
        timestamp: new Date().toISOString(),
        notes
      });
      
      setGlucoseValue('');
      setNotes('');
      setShowInput(false);
      await loadHistory();
    } catch (error) {
      console.error('Error adding glucose reading:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getGlucoseColor = (value: number) => {
    if (value < 70) return 'text-blue-600';
    if (value < 100) return 'text-green-600';
    if (value < 140) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md border border-slate-200">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-slate-700">Glucose Monitor</h2>
        <button
          onClick={() => setShowInput(!showInput)}
          className="text-emerald-600 hover:text-emerald-700 font-medium"
        >
          {showInput ? 'Cancel' : '+ Add Reading'}
        </button>
      </div>

      {showInput && (
        <form onSubmit={handleSubmit} className="mb-4 p-4 bg-slate-50 rounded-lg">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-3">
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">
                Glucose Level (mg/dL)
              </label>
              <input
                type="number"
                value={glucoseValue}
                onChange={(e) => setGlucoseValue(e.target.value)}
                placeholder="e.g., 95"
                className="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">
                Notes (Optional)
              </label>
              <input
                type="text"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g., After breakfast"
                className="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-emerald-600 text-white py-2 px-4 rounded-md hover:bg-emerald-700 disabled:bg-slate-400"
          >
            {isLoading ? 'Saving...' : 'Save Reading'}
          </button>
        </form>
      )}

      {history.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-600 mb-2">Recent Readings (7 days)</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {history.slice(0, 5).map((reading, index) => (
              <div key={index} className="flex justify-between items-center p-2 bg-slate-50 rounded">
                <div>
                  <span className={`font-bold text-lg ${getGlucoseColor(reading.value)}`}>
                    {reading.value} mg/dL
                  </span>
                  {reading.notes && (
                    <span className="text-sm text-slate-500 ml-2">• {reading.notes}</span>
                  )}
                </div>
                <span className="text-xs text-slate-400">
                  {new Date(reading.timestamp).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {history.length === 0 && !showInput && (
        <p className="text-sm text-slate-500 text-center py-4">
          No glucose readings yet. Add your first reading to start tracking!
        </p>
      )}
    </div>
  );
};