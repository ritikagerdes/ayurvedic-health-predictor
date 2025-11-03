# 🌿 Ayurvedic Health Predictor

An intelligent health management application that combines ancient Ayurvedic wisdom with modern AI technology to predict blood glucose levels and provide personalized dietary recommendations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2+-blue.svg)](https://reactjs.org/)

## ✨ Features

### 🔐 Authentication
- Secure OAuth2 authentication via Auth0
- User profile management
- Privacy-focused data storage

### 📊 Health Tracking
- **Meal Logging**: Track food intake with detailed item-by-item recording
- **Exercise Tracking**: Log physical activities and duration
- **Glucose Monitoring**: Input and track blood glucose readings
- **Lifestyle Factors**: Record additional health-impacting factors

### 🧬 Ayurvedic Analysis
- **Dosha Profiling**: Personalized recommendations based on Vata, Pitta, Kapha
- **Blood Glucose Prediction**: AI-powered glucose level forecasting
- **Digestive Fire (Agni) Analysis**: Understanding your metabolic state
- **Food Compatibility**: Identify beneficial and harmful food combinations

### 💊 Health Management
Targeted support for:
- 🩸 Blood glucose regulation
- ❤️ Cholesterol management
- 🔥 Metabolism optimization
- 🫀 Liver health (Yakrit)
- 🥞 Pancreas function
- 🍽️ Digestive system wellness

### 📈 Personalized Recommendations
- Meal-specific dietary suggestions (Breakfast, Lunch, Dinner, Snacks)
- Foods to favor and avoid based on your dosha
- Portion sizes and preparation methods
- Timing recommendations for optimal digestion

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend│
│   (TypeScript)  │
│   + Auth0 SDK   │
└────────┬────────┘
         │ HTTPS/JWT
┌────────▼────────┐
│  FastAPI Backend│
│   (Python)      │
│  + Auth0 Verify │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼────┐ ┌─▼──────┐ ┌─▼─────┐ ┌──▼──────┐
│Supabase│ │ChromaDB│ │OpenAI│ │Auth0   │
│(Postgres)│Vector DB││  GPT  │ │(OAuth2) │
└────────┘ └────────┘ └───────┘ └─────────┘
```

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- Auth0 React SDK for authentication
- Tailwind CSS for styling
- Vite for building

**Backend:**
- FastAPI (Python web framework)
- Pydantic for data validation
- Python-JOSE for JWT verification

**Databases:**
- Supabase (PostgreSQL) - User data, meal logs, glucose readings
- ChromaDB - Vector database for Ayurvedic knowledge embeddings

**AI/ML:**
- OpenAI GPT - Natural language analysis and recommendations (or Groq for free alternative)
- Sentence Transformers - Semantic search over Ayurvedic corpus

**Authentication:**
- Auth0 - OAuth2/OIDC provider

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Auth0 account (free)
- Supabase account (free)
- OpenAI API key (free $5 credits) or Groq API key (unlimited free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ayurvedic-health-predictor.git
cd ayurvedic-health-predictor
```

2. **Set up Auth0**
   - Create a new Single Page Application
   - Create an API with identifier
   - Note down Domain, Client ID, and API Audience

3. **Set up Supabase**
   - Create a new project
   - Run the SQL schema from `database/schema.sql`
   - Note down URL and anon key

4. **Get OpenAI API Key**
   - Visit [platform.openai.com](https://platform.openai.com)
   - Create a new API key
   - **Free Alternative**: Use [Groq](https://console.groq.com) for unlimited free access

5. **Configure Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python init_vector_db.py  # Initialize vector database
```

6. **Configure Frontend**
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your credentials
```

7. **Run the Application**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000`

## 📖 Documentation

- [Complete Setup Guide](SETUP.md) - Detailed installation and configuration
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when backend is running)
- [Database Schema](database/schema.sql) - Complete database structure

## 🌐 Deployment

### Backend (Render)
1. Create new Web Service
2. Connect GitHub repository
3. Set environment variables
4. Deploy with `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Import GitHub repository
2. Set root directory to `frontend`
3. Add environment variables
4. Deploy

See [SETUP.md](SETUP.md) for detailed deployment instructions.

## 📊 Database Schema

```sql
user_profiles
├── id (UUID)
├── user_id (TEXT) - Auth0 user ID
├── dosha (TEXT)
├── health_goals (TEXT[])
└── ...

meal_logs
├── id (UUID)
├── user_id (TEXT)
├── meal_items (TEXT[])
├── exercise (JSONB)
└── timestamp

glucose_readings
├── id (UUID)
├── user_id (TEXT)
├── glucose_value (NUMERIC)
└── timestamp
```

## 🔒 Security

- OAuth2 authentication with Auth0
- JWT token verification on all API endpoints
- Row Level Security (RLS) in Supabase
- CORS configuration for allowed origins
- Environment variables for sensitive data

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ayurvedic principles from classical texts
- OpenAI GPT for AI analysis
- Auth0 for authentication
- Supabase for database hosting
- Open source community

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/ayurvedic-health-predictor](https://github.com/yourusername/ayurvedic-health-predictor)

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Integration with continuous glucose monitors (CGM)
- [ ] Recipe recommendations
- [ ] Meal planning assistant
- [ ] Community features
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Data export functionality

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult with a qualified healthcare provider before making any changes to your diet, exercise, or health management routine.

---

Made with ❤️ and 🌿 for holistic health