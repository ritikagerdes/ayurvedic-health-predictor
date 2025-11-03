-- Ayurvedic Health Predictor Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT UNIQUE NOT NULL,
    email TEXT,
    name TEXT,
    dosha TEXT DEFAULT 'Vata-Pitta',
    age INTEGER,
    height NUMERIC,  -- in cm
    weight NUMERIC,  -- in kg
    health_goals TEXT[],
    health_conditions TEXT[],
    dietary_restrictions TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Meal Logs Table
CREATE TABLE IF NOT EXISTS meal_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    meal_items TEXT[] NOT NULL,
    exercise JSONB,
    lifestyle_factors TEXT,
    dosha TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
);

-- Glucose Readings Table
CREATE TABLE IF NOT EXISTS glucose_readings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    glucose_value NUMERIC NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE
);

-- Predictions Table (to store AI-generated predictions for analysis)
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    meal_log_id UUID,
    predicted_glucose TEXT NOT NULL,
    explanation TEXT NOT NULL,
    recommendations TEXT[],
    dietary_suggestions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    FOREIGN KEY (meal_log_id) REFERENCES meal_logs(id) ON DELETE SET NULL
);

-- Create Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_meal_logs_user_id ON meal_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_meal_logs_timestamp ON meal_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_glucose_readings_user_id ON glucose_readings(user_id);
CREATE INDEX IF NOT EXISTS idx_glucose_readings_timestamp ON glucose_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);

-- Row Level Security (RLS) Policies
-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE meal_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE glucose_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- User Profiles Policies
CREATE POLICY "Users can view own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid()::text = user_id);

CREATE POLICY "Users can update own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own profile"
    ON user_profiles FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Meal Logs Policies
CREATE POLICY "Users can view own meal logs"
    ON meal_logs FOR SELECT
    USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own meal logs"
    ON meal_logs FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Glucose Readings Policies
CREATE POLICY "Users can view own glucose readings"
    ON glucose_readings FOR SELECT
    USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own glucose readings"
    ON glucose_readings FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Predictions Policies
CREATE POLICY "Users can view own predictions"
    ON predictions FOR SELECT
    USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own predictions"
    ON predictions FOR INSERT
    WITH CHECK (auth.uid()::text = user_id);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on user_profiles
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create a view for user statistics
CREATE OR REPLACE VIEW user_statistics AS
SELECT
    up.user_id,
    up.dosha,
    COUNT(DISTINCT ml.id) as total_meal_logs,
    COUNT(DISTINCT gr.id) as total_glucose_readings,
    AVG(gr.glucose_value) as avg_glucose,
    MIN(gr.glucose_value) as min_glucose,
    MAX(gr.glucose_value) as max_glucose
FROM user_profiles up
LEFT JOIN meal_logs ml ON up.user_id = ml.user_id
LEFT JOIN glucose_readings gr ON up.user_id = gr.user_id
GROUP BY up.user_id, up.dosha;

-- Grant permissions on the view
GRANT SELECT ON user_statistics TO authenticated;