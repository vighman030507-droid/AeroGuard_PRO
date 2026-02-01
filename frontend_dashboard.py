# ============================================
# AeroGuard Pro - Air Quality Dashboard
# Python Flask Version with Tailwind CSS
# ============================================

# ----- IMPORTS -----
from flask import Flask, render_template_string, request, jsonify
import json
from datetime import datetime, timedelta
import random

# ----- FLASK APP -----
app = Flask(__name__)

# ----- HELPER FUNCTIONS -----
def get_aqi_category(aqi):
    """Returns AQI category, color, and description"""
    if aqi <= 50:
        return "Fresh Air", "#22c55e", "Air quality is excellent. Perfect for outdoor activities!"
    elif aqi <= 100:
        return "Moderate", "#eab308", "Air quality is acceptable. Sensitive individuals should limit prolonged outdoor exposure."
    elif aqi <= 150:
        return "Take Care", "#f97316", "Sensitive groups may experience health effects. Consider reducing outdoor activities."
    elif aqi <= 200:
        return "Poor", "#ef4444", "Everyone may begin to experience health effects. Limit outdoor activities."
    elif aqi <= 300:
        return "Very Poor", "#dc2626", "Health alert! Significant health effects possible. Avoid outdoor activities."
    else:
        return "Hazardous", "#7c2d12", "Emergency conditions. Stay indoors and use air purifiers."

def calculate_aqi(pm25, pm10, weather_index, volatility):
    """Calculate AQI based on pollutant levels"""
    pm25_contribution = pm25 * 2.5
    pm10_contribution = pm10 * 1.0
    weather_factor = 1 + (weather_index - 50) / 100
    volatility_factor = 1 + volatility / 200
    aqi = (pm25_contribution + pm10_contribution) * weather_factor * volatility_factor
    return min(max(int(aqi), 0), 500)

def generate_forecast_data(current_aqi):
    """Generate 6-hour forecast data"""
    data = []
    now = datetime.now()
    for i in range(7):
        hour = (now + timedelta(hours=i)).strftime("%I %p")
        variation = random.randint(-20, 30)
        value = max(20, min(400, current_aqi + variation))
        data.append({"hour": hour, "aqi": value})
    return data

def generate_trend_data():
    """Generate historical trend data"""
    data = []
    now = datetime.now()
    for i in range(12, 0, -1):
        hour = (now - timedelta(hours=i)).strftime("%I %p")
        value = random.randint(60, 180)
        data.append({"hour": hour, "aqi": value})
    return data

# ----- CITY DATA -----
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "population": "32M"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "population": "21M"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "population": "13M"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "population": "11M"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "population": "15M"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "population": "10M"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "population": "7M"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "population": "8M"}
}

# ----- HTML TEMPLATE -----
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroGuard Pro - AI Air Quality Forecast</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <!-- Chart.js (equivalent to Recharts) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Google Fonts - Geist equivalent (Inter) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        background: '#0f0f1a',
                        card: '#1a1a2e',
                        'card-hover': '#16213e',
                        primary: '#6366f1',
                        accent: '#22d3ee',
                        'aqi-good': '#22c55e',
                        'aqi-moderate': '#eab308',
                        'aqi-unhealthy': '#f97316',
                        'aqi-poor': '#ef4444',
                        'aqi-hazardous': '#7c2d12',
                    }
                }
            }
        }
    </script>
    
    <style>
        html { scroll-behavior: smooth; }
        body { 
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f0f1a 100%);
            min-height: 100vh;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0.3; }
            25% { transform: translateY(-20px) translateX(10px); opacity: 0.6; }
            50% { transform: translateY(-10px) translateX(-5px); opacity: 0.4; }
            75% { transform: translateY(-30px) translateX(5px); opacity: 0.5; }
        }
        
        @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(10px); }
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
            50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
        }
        
        .animate-float { animation: float 8s ease-in-out infinite; }
        .animate-gradient { 
            background-size: 200% 200%; 
            animation: gradient-shift 3s ease infinite; 
        }
        .animate-bounce-slow { animation: bounce 2s ease-in-out infinite; }
        .animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
        
        .gradient-text {
            background: linear-gradient(135deg, #6366f1 0%, #22d3ee 50%, #22c55e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .card-glass {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(99, 102, 241, 0.2);
        }
        
        .card-glass:hover {
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
        }
        
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        
        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: linear-gradient(90deg, #22c55e 0%, #eab308 33%, #f97316 66%, #ef4444 100%);
        }
        
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        }
        
        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            border: none;
        }
        
        select {
            background-color: rgba(26, 26, 46, 0.9);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        
        select:focus {
            outline: none;
            border-color: rgba(99, 102, 241, 0.6);
        }
    </style>
</head>
<body class="font-sans text-white">
    
    <!-- Hero Section -->
    <section id="hero" class="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
        <!-- Animated Background Particles -->
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute w-4 h-4 bg-primary/30 rounded-full top-1/4 left-1/4 animate-float" style="animation-delay: 0s;"></div>
            <div class="absolute w-3 h-3 bg-accent/30 rounded-full top-1/3 right-1/4 animate-float" style="animation-delay: 1s;"></div>
            <div class="absolute w-5 h-5 bg-aqi-good/30 rounded-full bottom-1/4 left-1/3 animate-float" style="animation-delay: 2s;"></div>
            <div class="absolute w-2 h-2 bg-primary/30 rounded-full top-2/3 right-1/3 animate-float" style="animation-delay: 3s;"></div>
            <div class="absolute w-6 h-6 bg-accent/20 rounded-full bottom-1/3 right-1/4 animate-float" style="animation-delay: 4s;"></div>
        </div>
        
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-background/50 to-background"></div>
        
        <!-- Hero Content -->
        <div class="relative z-10 text-center px-4">
            <div class="w-24 h-24 mx-auto mb-8 rounded-3xl bg-gradient-to-br from-primary to-accent flex items-center justify-center animate-pulse-glow">
                <i data-lucide="wind" class="w-12 h-12 text-white"></i>
            </div>
            
            <h1 class="text-5xl md:text-7xl font-extrabold mb-4 gradient-text animate-gradient">
                AeroGuard
            </h1>
            
            <p class="text-lg md:text-xl text-gray-400 max-w-lg mx-auto mb-12">
                Your intelligent companion for understanding air quality.
                Making healthier living decisions easier for everyone across India.
            </p>
            
            <a href="#features" class="inline-flex flex-col items-center text-gray-400 hover:text-white transition-colors">
                <span class="text-sm mb-2">Scroll to explore</span>
                <div class="animate-bounce-slow">
                    <i data-lucide="chevron-down" class="w-6 h-6"></i>
                </div>
            </a>
        </div>
    </section>
    
    <!-- Features Showcase -->
    <section id="features" class="py-16 px-4 max-w-7xl mx-auto">
        <h2 class="text-2xl font-bold mb-8 text-center">Explore Features</h2>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            <a href="#pollutants" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
                    <i data-lucide="cloud" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Pollutants</span>
            </a>
            
            <a href="#weather" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                    <i data-lucide="thermometer" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Weather</span>
            </a>
            
            <a href="#trends" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                    <i data-lucide="trending-up" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Trends</span>
            </a>
            
            <a href="#forecast" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                    <i data-lucide="clock" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Forecast</span>
            </a>
            
            <a href="#risk" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center">
                    <i data-lucide="alert-triangle" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Risk Level</span>
            </a>
            
            <a href="#health" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                    <i data-lucide="heart" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Health Tips</span>
            </a>
            
            <a href="#location" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
                    <i data-lucide="map-pin" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Location</span>
            </a>
            
            <a href="#insights" class="card-glass rounded-2xl p-6 text-center transition-all hover:-translate-y-1">
                <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
                    <i data-lucide="brain" class="w-7 h-7 text-white"></i>
                </div>
                <span class="text-sm font-medium">Insights</span>
            </a>
        </div>
    </section>
    
    <!-- Main Dashboard -->
    <section class="py-8 px-4 max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Left Column -->
            <div class="space-y-6">
                
                <!-- Location Selector -->
                <div id="location" class="card-glass rounded-2xl p-6 transition-all">
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
                            <i data-lucide="map-pin" class="w-5 h-5 text-white"></i>
                        </div>
                        <h3 class="text-lg font-semibold">Select Your City</h3>
                    </div>
                    
                    <select id="citySelect" class="w-full p-3 rounded-xl text-white" onchange="updateDashboard()">
                        {% for city, data in cities.items() %}
                        <option value="{{ city }}" {% if city == 'Delhi' %}selected{% endif %}>{{ city }}</option>
                        {% endfor %}
                    </select>
                    
                    <p id="cityInfo" class="mt-3 text-sm text-gray-400">
                        Population: 32M | Coordinates: 28.61N, 77.21E
                    </p>
                </div>
                
                <!-- Pollutant Levels -->
                <div id="pollutants" class="card-glass rounded-2xl p-6 transition-all">
                    <div class="flex items-center gap-3 mb-6">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
                            <i data-lucide="cloud" class="w-5 h-5 text-white"></i>
                        </div>
                        <h3 class="text-lg font-semibold">Pollutant Levels</h3>
                    </div>
                    
                    <div class="space-y-6">
                        <!-- PM2.5 -->
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-medium">Fine Particles (PM2.5)</span>
                                <span id="pm25Value" class="text-aqi-good font-bold">45 ug/m3</span>
                            </div>
                            <p class="text-sm text-gray-400 mb-3">Tiny particles that can enter your lungs</p>
                            <input type="range" id="pm25Slider" min="0" max="500" value="45" 
                                   class="w-full" oninput="updateDashboard()">
                            <p id="pm25Status" class="text-sm mt-2 text-aqi-good">Safe levels</p>
                        </div>
                        
                        <!-- PM10 -->
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-medium">Dust Particles (PM10)</span>
                                <span id="pm10Value" class="text-aqi-moderate font-bold">80 ug/m3</span>
                            </div>
                            <p class="text-sm text-gray-400 mb-3">Larger particles from dust and pollen</p>
                            <input type="range" id="pm10Slider" min="0" max="500" value="80" 
                                   class="w-full" oninput="updateDashboard()">
                            <p id="pm10Status" class="text-sm mt-2 text-aqi-moderate">Moderate levels</p>
                        </div>
                    </div>
                </div>
                
                <!-- Weather Conditions -->
                <div id="weather" class="card-glass rounded-2xl p-6 transition-all">
                    <div class="flex items-center gap-3 mb-6">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                            <i data-lucide="thermometer" class="w-5 h-5 text-white"></i>
                        </div>
                        <h3 class="text-lg font-semibold">Weather Conditions</h3>
                    </div>
                    
                    <div class="space-y-6">
                        <!-- Weather Index -->
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-medium">Weather Impact</span>
                                <span id="weatherValue" class="text-accent font-bold">65</span>
                            </div>
                            <p class="text-sm text-gray-400 mb-3">How weather affects pollutant dispersion</p>
                            <input type="range" id="weatherSlider" min="0" max="100" value="65" 
                                   class="w-full" oninput="updateDashboard()">
                            <p id="weatherStatus" class="text-sm mt-2 text-gray-300">Good conditions</p>
                        </div>
                        
                        <!-- Air Stability -->
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-medium">Air Stability</span>
                                <span id="stabilityValue" class="text-accent font-bold">30</span>
                            </div>
                            <p class="text-sm text-gray-400 mb-3">How stable or changeable the air quality is</p>
                            <input type="range" id="stabilitySlider" min="0" max="100" value="30" 
                                   class="w-full" oninput="updateDashboard()">
                            <p id="stabilityStatus" class="text-sm mt-2 text-gray-300">Very stable</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Right Column -->
            <div class="space-y-6">
                
                <!-- AQI Gauge -->
                <div id="risk" class="card-glass rounded-2xl p-6 transition-all">
                    <div class="flex items-center gap-3 mb-6">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center">
                            <i data-lucide="activity" class="w-5 h-5 text-white"></i>
                        </div>
                        <h3 class="text-lg font-semibold">Current Air Quality</h3>
                    </div>
                    
                    <div class="text-center py-8">
                        <!-- AQI Value -->
                        <div id="aqiGauge" class="relative w-48 h-48 mx-auto mb-6">
                            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                                <!-- Background Arc -->
                                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(99,102,241,0.2)" stroke-width="10"/>
                                <!-- Progress Arc -->
                                <circle id="aqiArc" cx="50" cy="50" r="45" fill="none" stroke="#22c55e" stroke-width="10"
                                        stroke-dasharray="283" stroke-dashoffset="141" stroke-linecap="round"/>
                            </svg>
                            <div class="absolute inset-0 flex flex-col items-center justify-center">
                                <span id="aqiValue" class="text-5xl font-extrabold text-aqi-good">156</span>
                                <span id="aqiLabel" class="text-lg font-semibold text-aqi-good">Take Care</span>
                            </div>
                        </div>
                        
                        <p id="aqiDescription" class="text-gray-400 max-w-sm mx-auto">
                            Sensitive groups may experience health effects. Consider reducing outdoor activities.
                        </p>
                    </div>
                    
                    <!-- Risk Badge -->
                    <div class="text-center mt-4">
                        <span id="riskBadge" class="inline-block px-6 py-2 rounded-full text-sm font-semibold bg-aqi-unhealthy/20 text-aqi-unhealthy border border-aqi-unhealthy/40">
                            High Risk
                        </span>
                    </div>
                </div>
                
                <!-- 6-Hour Forecast -->
                <div id="forecast" class="card-glass rounded-2xl p-6 transition-all">
                    <div class="flex items-center gap-3 mb-6">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                            <i data-lucide="clock" class="w-5 h-5 text-white"></i>
                        </div>
                        <h3 class="text-lg font-semibold">6-Hour Forecast</h3>
                    </div>
                    
                    <div class="h-64">
                        <canvas id="forecastChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Trends Section -->
    <section id="trends" class="py-8 px-4 max-w-7xl mx-auto">
        <div class="flex items-center gap-3 mb-8">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                <i data-lucide="trending-up" class="w-5 h-5 text-white"></i>
            </div>
            <h2 class="text-2xl font-bold">Air Quality Trends</h2>
        </div>
        
        <!-- Trend Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="card-glass rounded-2xl p-6 text-center">
                <p id="pastAqi" class="text-4xl font-bold text-accent">126</p>
                <p class="text-sm text-gray-400 mt-2">3 Hours Ago</p>
            </div>
            <div class="card-glass rounded-2xl p-6 text-center">
                <p id="currentAqiMetric" class="text-4xl font-bold text-aqi-unhealthy">156</p>
                <p class="text-sm text-gray-400 mt-2">Current AQI</p>
            </div>
            <div class="card-glass rounded-2xl p-6 text-center">
                <p id="trendChange" class="text-4xl font-bold text-aqi-poor">+24%</p>
                <p id="trendLabel" class="text-sm text-gray-400 mt-2">Worsening</p>
            </div>
        </div>
        
        <!-- Trend Chart -->
        <div class="card-glass rounded-2xl p-6">
            <div class="h-72">
                <canvas id="trendChart"></canvas>
            </div>
        </div>
    </section>
    
    <!-- Health Recommendations -->
    <section id="health" class="py-8 px-4 max-w-7xl mx-auto">
        <div class="flex items-center gap-3 mb-8">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                <i data-lucide="heart" class="w-5 h-5 text-white"></i>
            </div>
            <h2 class="text-2xl font-bold">Health Recommendations</h2>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Children & Elderly -->
            <div id="healthCard1" class="card-glass rounded-2xl p-6 border-l-4 border-aqi-unhealthy">
                <div class="flex items-center gap-3 mb-4">
                    <i data-lucide="baby" class="w-6 h-6 text-aqi-unhealthy"></i>
                    <h3 class="font-semibold">Children & Elderly</h3>
                </div>
                <p id="healthText1" class="text-gray-300 text-sm leading-relaxed">
                    Limit outdoor time to 30 minutes. Keep windows closed at home.
                </p>
            </div>
            
            <!-- Active People -->
            <div id="healthCard2" class="card-glass rounded-2xl p-6 border-l-4 border-aqi-unhealthy">
                <div class="flex items-center gap-3 mb-4">
                    <i data-lucide="bike" class="w-6 h-6 text-aqi-unhealthy"></i>
                    <h3 class="font-semibold">Active People</h3>
                </div>
                <p id="healthText2" class="text-gray-300 text-sm leading-relaxed">
                    Move workouts indoors. Avoid outdoor exercise completely.
                </p>
            </div>
            
            <!-- General Public -->
            <div id="healthCard3" class="card-glass rounded-2xl p-6 border-l-4 border-aqi-unhealthy">
                <div class="flex items-center gap-3 mb-4">
                    <i data-lucide="users" class="w-6 h-6 text-aqi-unhealthy"></i>
                    <h3 class="font-semibold">General Public</h3>
                </div>
                <p id="healthText3" class="text-gray-300 text-sm leading-relaxed">
                    Reduce prolonged outdoor exposure. Consider wearing an N95 mask outside.
                </p>
            </div>
        </div>
    </section>
    
    <!-- Smart Insights -->
    <section id="insights" class="py-8 px-4 max-w-7xl mx-auto">
        <div class="flex items-center gap-3 mb-8">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
                <i data-lucide="brain" class="w-5 h-5 text-white"></i>
            </div>
            <h2 class="text-2xl font-bold">Smart Insights</h2>
        </div>
        
        <div id="insightsContainer" class="space-y-4">
            <!-- Insights will be dynamically populated -->
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="py-12 px-4 mt-16 border-t border-primary/20">
        <div class="max-w-7xl mx-auto text-center">
            <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                <i data-lucide="wind" class="w-8 h-8 text-white"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">AeroGuard</h3>
            <p class="text-gray-400 max-w-md mx-auto mb-4">
                Your trusted companion for understanding air quality.
                Making healthier living decisions easier for everyone.
            </p>
            <p class="text-sm text-gray-500 mb-6">Built with care for Indian cities</p>
            
            <div class="pt-6 border-t border-primary/20">
                <p class="text-xs text-gray-500">
                    Data Source: 
                    <a href="https://github.com/cp099/India-Air-Quality-Dataset/releases?utm_source=chatgpt.com" 
                       target="_blank" rel="noopener noreferrer"
                       class="text-primary hover:text-accent transition-colors underline">
                        India Air Quality Dataset on GitHub
                    </a>
                </p>
            </div>
        </div>
    </footer>
    
    <!-- JavaScript -->
    <script>
        // City Data
        const cities = {{ cities | tojson }};
        
        // Chart instances
        let forecastChart = null;
        let trendChart = null;
        
        // Initialize Lucide Icons
        lucide.createIcons();
        
        // Initialize Charts
        function initCharts() {
            const forecastCtx = document.getElementById('forecastChart').getContext('2d');
            const trendCtx = document.getElementById('trendChart').getContext('2d');
            
            // Forecast Chart
            forecastChart = new Chart(forecastCtx, {
                type: 'line',
                data: {
                    labels: ['Now', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM'],
                    datasets: [{
                        label: 'AQI',
                        data: [156, 162, 175, 168, 155, 148, 142],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#6366f1',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(99, 102, 241, 0.1)' },
                            ticks: { color: '#9ca3af' }
                        },
                        y: {
                            grid: { color: 'rgba(99, 102, 241, 0.1)' },
                            ticks: { color: '#9ca3af' },
                            min: 0,
                            max: 300
                        }
                    }
                }
            });
            
            // Trend Chart
            trendChart = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM'],
                    datasets: [{
                        label: 'AQI',
                        data: [120, 115, 108, 102, 98, 95, 110, 125, 140, 155, 148, 156],
                        borderColor: '#22d3ee',
                        backgroundColor: 'rgba(34, 211, 238, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#22d3ee',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(34, 211, 238, 0.1)' },
                            ticks: { color: '#9ca3af' }
                        },
                        y: {
                            grid: { color: 'rgba(34, 211, 238, 0.1)' },
                            ticks: { color: '#9ca3af' },
                            min: 0,
                            max: 300
                        }
                    }
                }
            });
        }
        
        // Calculate AQI
        function calculateAQI(pm25, pm10, weather, stability) {
            const pm25Contribution = pm25 * 2.5;
            const pm10Contribution = pm10 * 1.0;
            const weatherFactor = 1 + (weather - 50) / 100;
            const stabilityFactor = 1 + stability / 200;
            let aqi = (pm25Contribution + pm10Contribution) * weatherFactor * stabilityFactor;
            return Math.min(Math.max(Math.round(aqi), 0), 500);
        }
        
        // Get AQI Category
        function getAQICategory(aqi) {
            if (aqi <= 50) return { label: 'Fresh Air', color: '#22c55e', risk: 'Low Risk', desc: 'Air quality is excellent. Perfect for outdoor activities!' };
            if (aqi <= 100) return { label: 'Moderate', color: '#eab308', risk: 'Moderate Risk', desc: 'Air quality is acceptable. Sensitive individuals should limit prolonged outdoor exposure.' };
            if (aqi <= 150) return { label: 'Take Care', color: '#f97316', risk: 'High Risk', desc: 'Sensitive groups may experience health effects. Consider reducing outdoor activities.' };
            if (aqi <= 200) return { label: 'Poor', color: '#ef4444', risk: 'Severe Risk', desc: 'Everyone may begin to experience health effects. Limit outdoor activities.' };
            if (aqi <= 300) return { label: 'Very Poor', color: '#dc2626', risk: 'Very Severe Risk', desc: 'Health alert! Significant health effects possible. Avoid outdoor activities.' };
            return { label: 'Hazardous', color: '#7c2d12', risk: 'Emergency', desc: 'Emergency conditions. Stay indoors and use air purifiers.' };
        }
        
        // Get Health Recommendations
        function getHealthRecommendations(aqi) {
            if (aqi <= 50) {
                return {
                    children: 'Perfect day for outdoor activities! Enjoy parks and playgrounds freely.',
                    active: 'Great conditions for jogging, cycling, and outdoor sports!',
                    general: 'Excellent air quality. No special precautions needed.',
                    color: '#22c55e'
                };
            } else if (aqi <= 100) {
                return {
                    children: 'Outdoor activities are fine. Take breaks if feeling tired.',
                    active: 'Light exercise is okay. Avoid strenuous activities during peak hours.',
                    general: 'Most people can continue normal activities. Sensitive individuals should be cautious.',
                    color: '#eab308'
                };
            } else if (aqi <= 150) {
                return {
                    children: 'Limit outdoor time to 30 minutes. Keep windows closed at home.',
                    active: 'Move workouts indoors. Avoid outdoor exercise completely.',
                    general: 'Reduce prolonged outdoor exposure. Consider wearing an N95 mask outside.',
                    color: '#f97316'
                };
            } else {
                return {
                    children: 'Stay indoors. Use air purifiers if available. Avoid all outdoor activities.',
                    active: 'Cancel all outdoor activities. Exercise indoors only with filtered air.',
                    general: 'Avoid going outside. Use N95 masks if you must. Keep all windows sealed.',
                    color: '#ef4444'
                };
            }
        }
        
        // Generate Insights
        function generateInsights(pm25, pm10, weather, stability, aqi) {
            const insights = [];
            
            if (pm25 > 100) {
                insights.push({ icon: 'car', text: 'High fine particle levels detected. This is often caused by vehicle emissions and industrial activity.' });
            }
            if (pm10 > 150) {
                insights.push({ icon: 'construction', text: 'Elevated dust levels in the air. Construction activity or dry weather may be contributing factors.' });
            }
            if (weather > 70) {
                insights.push({ icon: 'cloud', text: 'Current weather conditions are trapping pollutants close to the ground.' });
            }
            if (stability > 60) {
                insights.push({ icon: 'activity', text: 'Air quality is changing rapidly throughout the day. Check back frequently for updates.' });
            }
            if (aqi <= 50) {
                insights.push({ icon: 'sun', text: 'Excellent air quality today! This is a perfect day for spending time outdoors.' });
            }
            
            if (insights.length === 0) {
                insights.push({ icon: 'info', text: 'Air quality is within acceptable levels. Continue monitoring for any changes.' });
            }
            
            return insights;
        }
        
        // Update Dashboard
        function updateDashboard() {
            // Get values
            const pm25 = parseInt(document.getElementById('pm25Slider').value);
            const pm10 = parseInt(document.getElementById('pm10Slider').value);
            const weather = parseInt(document.getElementById('weatherSlider').value);
            const stability = parseInt(document.getElementById('stabilitySlider').value);
            const city = document.getElementById('citySelect').value;
            
            // Calculate AQI
            const aqi = calculateAQI(pm25, pm10, weather, stability);
            const category = getAQICategory(aqi);
            const health = getHealthRecommendations(aqi);
            
            // Update PM2.5
            document.getElementById('pm25Value').textContent = pm25 + ' ug/m3';
            const pm25Status = pm25 <= 35 ? 'Safe levels' : pm25 <= 75 ? 'Moderate levels' : pm25 <= 150 ? 'Unhealthy levels' : 'Dangerous levels';
            const pm25Color = pm25 <= 35 ? '#22c55e' : pm25 <= 75 ? '#eab308' : pm25 <= 150 ? '#f97316' : '#ef4444';
            document.getElementById('pm25Value').style.color = pm25Color;
            document.getElementById('pm25Status').textContent = pm25Status;
            document.getElementById('pm25Status').style.color = pm25Color;
            
            // Update PM10
            document.getElementById('pm10Value').textContent = pm10 + ' ug/m3';
            const pm10Status = pm10 <= 50 ? 'Safe levels' : pm10 <= 100 ? 'Moderate levels' : pm10 <= 250 ? 'Unhealthy levels' : 'Dangerous levels';
            const pm10Color = pm10 <= 50 ? '#22c55e' : pm10 <= 100 ? '#eab308' : pm10 <= 250 ? '#f97316' : '#ef4444';
            document.getElementById('pm10Value').style.color = pm10Color;
            document.getElementById('pm10Status').textContent = pm10Status;
            document.getElementById('pm10Status').style.color = pm10Color;
            
            // Update Weather
            document.getElementById('weatherValue').textContent = weather;
            const weatherStatus = weather <= 30 ? 'Excellent dispersion' : weather <= 60 ? 'Good conditions' : 'Poor dispersion';
            document.getElementById('weatherStatus').textContent = weatherStatus;
            
            // Update Stability
            document.getElementById('stabilityValue').textContent = stability;
            const stabilityStatus = stability <= 25 ? 'Very stable' : stability <= 50 ? 'Moderate changes expected' : 'Rapidly changing';
            document.getElementById('stabilityStatus').textContent = stabilityStatus;
            
            // Update City Info
            const cityData = cities[city];
            document.getElementById('cityInfo').textContent = `Population: ${cityData.population} | Coordinates: ${cityData.lat.toFixed(2)}N, ${cityData.lon.toFixed(2)}E`;
            
            // Update AQI Display
            document.getElementById('aqiValue').textContent = aqi;
            document.getElementById('aqiValue').style.color = category.color;
            document.getElementById('aqiLabel').textContent = category.label;
            document.getElementById('aqiLabel').style.color = category.color;
            document.getElementById('aqiDescription').textContent = category.desc;
            
            // Update AQI Arc
            const arcOffset = 283 - (aqi / 500) * 283;
            document.getElementById('aqiArc').style.strokeDashoffset = arcOffset;
            document.getElementById('aqiArc').style.stroke = category.color;
            
            // Update Risk Badge
            document.getElementById('riskBadge').textContent = category.risk;
            document.getElementById('riskBadge').style.backgroundColor = category.color + '33';
            document.getElementById('riskBadge').style.color = category.color;
            document.getElementById('riskBadge').style.borderColor = category.color + '66';
            
            // Update Trends
            const pastAqi = Math.max(20, aqi - Math.floor(Math.random() * 30));
            const change = Math.round(((aqi - pastAqi) / pastAqi) * 100);
            document.getElementById('pastAqi').textContent = pastAqi;
            document.getElementById('currentAqiMetric').textContent = aqi;
            document.getElementById('currentAqiMetric').style.color = category.color;
            document.getElementById('trendChange').textContent = (change >= 0 ? '+' : '') + change + '%';
            document.getElementById('trendChange').style.color = change < 0 ? '#22c55e' : '#ef4444';
            document.getElementById('trendLabel').textContent = change < 0 ? 'Improving' : change > 0 ? 'Worsening' : 'Stable';
            
            // Update Health Cards
            document.getElementById('healthText1').textContent = health.children;
            document.getElementById('healthText2').textContent = health.active;
            document.getElementById('healthText3').textContent = health.general;
            
            document.querySelectorAll('#healthCard1, #healthCard2, #healthCard3').forEach(card => {
                card.style.borderLeftColor = health.color;
            });
            
            document.querySelectorAll('#healthCard1 svg, #healthCard2 svg, #healthCard3 svg').forEach(icon => {
                icon.style.color = health.color;
            });
            
            // Update Insights
            const insights = generateInsights(pm25, pm10, weather, stability, aqi);
            const insightsContainer = document.getElementById('insightsContainer');
            insightsContainer.innerHTML = insights.map(insight => `
                <div class="card-glass rounded-xl p-4 flex items-start gap-4">
                    <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-primary/30 to-accent/30 flex items-center justify-center flex-shrink-0">
                        <i data-lucide="${insight.icon}" class="w-5 h-5 text-accent"></i>
                    </div>
                    <p class="text-gray-300 leading-relaxed">${insight.text}</p>
                </div>
            `).join('');
            
            // Reinitialize Lucide icons
            lucide.createIcons();
            
            // Update Charts
            if (forecastChart) {
                const forecastData = [];
                for (let i = 0; i < 7; i++) {
                    forecastData.push(Math.max(20, Math.min(400, aqi + Math.floor(Math.random() * 50) - 25)));
                }
                forecastChart.data.datasets[0].data = forecastData;
                forecastChart.update();
            }
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            updateDashboard();
        });
    </script>
</body>
</html>
'''

# ----- ROUTES -----
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, cities=CITIES)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.json
    pm25 = data.get('pm25', 45)
    pm10 = data.get('pm10', 80)
    weather = data.get('weather', 65)
    volatility = data.get('volatility', 30)
    
    aqi = calculate_aqi(pm25, pm10, weather, volatility)
    category, color, description = get_aqi_category(aqi)
    forecast = generate_forecast_data(aqi)
    trends = generate_trend_data()
    
    return jsonify({
        'aqi': aqi,
        'category': category,
        'color': color,
        'description': description,
        'forecast': forecast,
        'trends': trends
    })

# ----- RUN APP -----
if __name__ == '__main__':
    app.run(debug=True, port=5000)
