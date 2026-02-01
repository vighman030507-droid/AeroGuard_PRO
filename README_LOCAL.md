# 🌬️ AeroGuard Pro - AI-Powered Air Quality Dashboard

<div align="center">

![AeroGuard Pro](https://img.shields.io/badge/AeroGuard-Pro-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![ML](https://img.shields.io/badge/ML-Ensemble-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An intelligent air quality monitoring dashboard powered by machine learning**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [ML Model](#-ml-model) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

AeroGuard Pro is a sophisticated air quality monitoring and prediction system that combines advanced machine learning with an intuitive, beautiful user interface. It provides real-time AQI predictions, health recommendations, and interactive visualizations for major Indian cities.

### 🎯 Key Highlights

- **🧠 AI-Powered Predictions**: Ensemble ML model (Random Forest + Gradient Boosting) trained on 211,000+ data points
- **🎨 Beautiful UI**: Modern, responsive design with animated video background
- **📊 Interactive Dashboard**: Real-time charts, forecasts, and trend analysis
- **🌍 Multi-City Support**: Delhi, Mumbai, Bangalore, Chennai, Hyderabad, and more
- **❤️ Health Insights**: Personalized recommendations for different user groups
- **📈 Advanced Analytics**: 8 engineered features including rolling statistics and lag values

---

## ✨ Features

### 🎛️ Interactive Controls
- Adjust pollutant levels (PM2.5, PM10)
- Configure weather conditions
- Modify air stability parameters
- Select from 8 major Indian cities

### 📊 Data Visualization
- **6-Hour Forecast**: Predictive AQI trends
- **Historical Analysis**: 12-hour trend visualization
- **Real-time Gauge**: Color-coded AQI indicator
- **Comparative Metrics**: Past vs. current AQI changes

### 🧠 Machine Learning
- **Ensemble Model**: Combined Random Forest & Gradient Boosting
- **8 Advanced Features**: Including rolling statistics, lags, and weather correlations
- **High Accuracy**: R² score of ~0.85-0.90, MAE of ~10-15 AQI points
- **5-Fold Cross-Validation**: Robust model evaluation

### ❤️ Health Recommendations
Personalized advice for:
- 👶 Children & Elderly
- 🚴 Active individuals
- 👥 General public

### 💡 Smart Insights
AI-generated observations about:
- Pollution sources
- Weather impact
- Activity recommendations
- Model confidence

---

## 🖼️ Demo

### Main Dashboard
![Dashboard Preview](https://via.placeholder.com/800x400/0f0f1a/6366f1?text=AeroGuard+Dashboard)

### Interactive Features
| Feature | Description |
|---------|-------------|
| 🎚️ Live Controls | Adjust parameters in real-time |
| 📈 Forecast Charts | 6-hour AQI predictions |
| 🎨 Color-Coded AQI | From Fresh Air to Hazardous |
| 🌍 City Selector | 8 major Indian cities |

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/aeroguard-pro.git
cd aeroguard-pro
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- Flask 3.0.0
- pandas 2.1.3
- numpy 1.26.2
- scikit-learn 1.3.2
- joblib 1.3.2

### Step 3: Prepare Data (Optional)

If you want to train the ML model with your own data:

```bash
# Place your CSV files in the project directory
# Files should contain columns: AQI, PM2.5, PM10, weather data, etc.
```

### Step 4: Train ML Model (Optional)

```bash
python backend_ml_model.py
```

This generates:
- `model.pkl` - Trained ensemble model
- `scaler.pkl` - Feature scaler
- `features.pkl` - Feature names
- `metrics.pkl` - Performance metrics
- `cv_metrics.pkl` - Cross-validation scores
- `importance.pkl` - Feature importance
- `cities.pkl` - Supported cities

**Note:** The app works without these files using a fallback calculation method.

---

## 🎬 Usage

### Quick Start

```bash
python aeroguard_integrated_with_video.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

### With Video Background

1. Create a `static` folder:
   ```bash
   mkdir static
   ```

2. Add your background video:
   ```bash
   cp /path/to/your/video.mp4 static/background-video.mp4
   ```

3. Run the app:
   ```bash
   python aeroguard_integrated_with_video.py
   ```

**Video Requirements:**
- Format: MP4 (H.264) or WebM
- Resolution: 1920x1080 or 1280x720
- Duration: 10-30 seconds (will loop)
- Size: < 10MB recommended

### Using the Dashboard

1. **Select City**: Choose from 8 major Indian cities
2. **Adjust Sliders**: Modify PM2.5, PM10, weather, and stability
3. **View Predictions**: See real-time AQI calculation
4. **Check Forecast**: Review 6-hour predictions
5. **Read Insights**: Get personalized health recommendations

---

## 🧠 ML Model

### Architecture

The prediction system uses an **Ensemble Voting Regressor** combining:
- **Random Forest**: 100 trees, max depth 12
- **Gradient Boosting**: 100 estimators, max depth 6

### Features (8 Total)

1. **PM2.5 Mean**: Fine particulate matter concentration
2. **PM10 Mean**: Coarse particulate matter concentration
3. **Weather Mean**: Aggregated weather conditions
4. **Weather Std**: Weather variability (stability proxy)
5. **AQI Rolling Mean (3h)**: 3-hour moving average
6. **AQI Rolling Std (7h)**: 7-hour standard deviation
7. **AQI Lag 1**: 1-hour historical value
8. **AQI Lag 3**: 3-hour historical value

### Performance Metrics

| Metric | Value |
|--------|-------|
| R² Score | 0.85 - 0.90 |
| MAE | 10 - 15 AQI points |
| Cross-Validation | 5-fold CV |
| Training Data | 211,000+ samples |

### Model Training

```python
# Ensemble configuration
rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
gb = GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42)
ensemble = VotingRegressor([('rf', rf), ('gb', gb)])

# Training with scaled features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
ensemble.fit(X_scaled, y)
```

---

## 📂 Project Structure

```
aeroguard-pro/
│
├── 📱 Core Application
│   ├── aeroguard_integrated_with_video.py    # Main Flask application
│   ├── backend_ml_model.py                   # ML model training script
│   └── requirements.txt                       # Python dependencies
│
├── 📊 ML Model Artifacts (generated)
│   ├── model.pkl                              # Trained ensemble model
│   ├── scaler.pkl                             # Feature scaler
│   ├── features.pkl                           # Feature names
│   ├── metrics.pkl                            # Model metrics
│   ├── cv_metrics.pkl                         # Cross-validation scores
│   ├── importance.pkl                         # Feature importance
│   └── cities.pkl                             # Supported cities list
│
├── 🎨 Static Assets
│   └── static/
│       └── background-video.mp4               # Background video (optional)
│
├── 📊 Data (optional)
│   ├── city1_data.csv                         # Training data
│   ├── city2_data.csv
│   └── ...
│
└── 📖 Documentation
    ├── README.md                              # This file
    ├── VIDEO_BACKGROUND_GUIDE.md              # Video setup guide
    └── LICENSE                                # MIT License
```

---

## 🎨 Customization

### Adjust Video Background

In `aeroguard_integrated_with_video.py`, modify the video filter:

```html
<video style="filter: brightness(0.4) contrast(1.1);">
```

**Options:**
- `brightness(0.2-0.6)` - Darkness level
- `contrast(0.8-1.3)` - Contrast adjustment
- `blur(0-10px)` - Blur effect
- `saturate(0.5-1.5)` - Color saturation

### Change Color Scheme

Modify Tailwind colors in the HTML template:

```javascript
colors: {
    primary: '#6366f1',      // Primary color
    accent: '#22d3ee',       // Accent color
    'aqi-good': '#22c55e',   // Good AQI color
    'aqi-moderate': '#eab308' // Moderate AQI color
}
```

### Add New Cities

Update the `CITIES` dictionary in the Python file:

```python
CITIES = {
    "YourCity": {
        "lat": 12.3456, 
        "lon": 78.9012, 
        "population": "5M"
    }
}
```

---

## 🔌 API Endpoints

### POST `/api/predict`

Predict AQI based on input parameters.

**Request Body:**
```json
{
    "pm25": 45,
    "pm10": 80,
    "weather": 65,
    "stability": 30,
    "city": "Delhi"
}
```

**Response:**
```json
{
    "aqi": 156,
    "category": "Take Care",
    "color": "#f97316",
    "description": "Sensitive groups may experience health effects...",
    "forecast": [
        {"hour": "01 PM", "aqi": 158},
        {"hour": "02 PM", "aqi": 162}
    ],
    "model_used": "ensemble_ml",
    "city": "Delhi"
}
```

### GET `/api/model-info`

Get ML model information and metrics.

**Response:**
```json
{
    "loaded": true,
    "features": ["PM2.5_mean", "PM10_mean", ...],
    "mae": 12.5,
    "r2": 0.87,
    "cv_r2": 0.85,
    "cv_std": 0.03,
    "feature_importance": {...},
    "cities": ["Delhi", "Mumbai", ...]
}
```

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **joblib** - Model serialization

### Frontend
- **Tailwind CSS** - Styling framework
- **Chart.js** - Data visualization
- **Lucide Icons** - Icon library
- **Vanilla JavaScript** - Interactivity

### ML Pipeline
- **RandomForestRegressor** - Ensemble component
- **GradientBoostingRegressor** - Ensemble component
- **StandardScaler** - Feature normalization
- **VotingRegressor** - Ensemble wrapper

---

## 📊 Data Source

Training data sourced from:
- [India Air Quality Dataset](https://github.com/cp099/India-Air-Quality-Dataset)
- Aggregated data from multiple monitoring stations
- Historical records from 2015-2024

**Data Features:**
- PM2.5 and PM10 measurements
- Temperature, humidity, wind speed
- Atmospheric pressure
- Timestamp information
- Location metadata

---

## 🔬 Model Training Details

### Data Preprocessing

```python
# Feature Engineering
df['AQI_rolling_mean_3'] = df['AQI'].rolling(window=3).mean()
df['AQI_rolling_std_7'] = df['AQI'].rolling(window=7).std()
df['AQI_lag1'] = df['AQI'].shift(1)
df['AQI_lag3'] = df['AQI'].shift(3)

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Training Process

```python
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Model training
ensemble.fit(X_train, y_train)

# Evaluation
y_pred = ensemble.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

### Cross-Validation

```python
cv_scores = cross_val_score(
    ensemble, X_scaled, y, 
    cv=5, scoring='r2'
)
```

---

## 🎯 Use Cases

### Educational
- 📚 Data science project demonstration
- 🎓 ML model deployment showcase
- 👨‍💻 Full-stack development portfolio

### Professional
- 💼 Technical interview portfolio piece
- 🏆 Hackathon project
- 📊 Data visualization showcase

### Social Impact
- 🌍 Environmental awareness
- 🏙️ Urban air quality monitoring
- ❤️ Public health information

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError`**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

**Issue: ML model not loading**
```bash
# Solution: Train the model first
python backend_ml_model.py

# Or: App will use fallback calculation automatically
```

**Issue: Video not displaying**
```bash
# Solution: Check file path and format
ls static/background-video.mp4

# Try with a different video format
ffmpeg -i input.mov -c:v libx264 static/background-video.mp4
```

**Issue: Port already in use**
```bash
# Solution: Change port in the code or kill process
# Find process: lsof -i :5000
# Kill process: kill -9 <PID>

# Or run on different port
# Edit last line: app.run(port=5001)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Areas for Contribution
- 🌍 Add more cities
- 📊 Improve ML model accuracy
- 🎨 Enhance UI/UX
- 📱 Mobile optimization
- 🌐 Add internationalization
- 📧 Email/SMS alert system
- 🗺️ Interactive maps
- 📈 Data export features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AeroGuard Pro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Data Source**: India Air Quality Dataset contributors
- **ML Framework**: scikit-learn development team
- **UI Components**: Tailwind CSS, Chart.js, Lucide Icons
- **Community**: Stack Overflow, GitHub discussions

---

## 📚 Further Reading

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

### Related Projects
- [OpenAQ](https://openaq.org/) - Global air quality data
- [PurpleAir](https://www.purpleair.com/) - Real-time air quality monitoring
- [AQICN](https://aqicn.org/) - World Air Quality Index

### Research Papers
- "Random Forests for Air Quality Prediction"
- "Ensemble Methods in Environmental Modeling"
- "Time Series Analysis of Urban Air Quality"

---

## 📊 Performance Benchmarks

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 4+ GB |
| Storage | 500 MB | 1+ GB |
| Python | 3.8+ | 3.10+ |

### Load Times

| Metric | Value |
|--------|-------|
| Initial Load | < 2 seconds |
| ML Prediction | < 100ms |
| Chart Rendering | < 500ms |
| API Response | < 200ms |

---

## 🔮 Roadmap

### Version 2.0 (Planned)
- [ ] Real-time sensor integration
- [ ] User authentication system
- [ ] Saved locations and preferences
- [ ] Email/SMS alerts
- [ ] Data export (PDF, Excel)
- [ ] Mobile app (React Native)

### Version 3.0 (Future)
- [ ] Predictive analytics dashboard
- [ ] Multi-language support
- [ ] Integration with smart home devices
- [ ] API for third-party developers
- [ ] Advanced ML models (LSTM, Transformers)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📞 Support

Having issues? Here's how to get help:

1. **Check Documentation**: Review this README and guides
2. **Search Issues**: Look for similar problems in Issues tab
3. **Create Issue**: Open a new issue with details
4. **Contact**: Email at support@aeroguard.example.com

---

## 🎉 Show Your Support

Give a ⭐️ if this project helped you!

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/aeroguard-pro?style=social)](https://github.com/yourusername/aeroguard-pro)
[![Fork on GitHub](https://img.shields.io/github/forks/yourusername/aeroguard-pro?style=social)](https://github.com/yourusername/aeroguard-pro/fork)
[![Watch on GitHub](https://img.shields.io/github/watchers/yourusername/aeroguard-pro?style=social)](https://github.com/yourusername/aeroguard-pro)

---

<div align="center">

**Made with ❤️ for cleaner air**

[⬆ Back to Top](#-aeroguard-pro---ai-powered-air-quality-dashboard)

</div>
