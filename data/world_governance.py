"""
World Governance Benchmark Dataset
Based on normalized (0-100) interpretations of:
- Freedom House Freedom in the World
- World Bank Governance Indicators
- UN Human Development Index
- Transparency International CPI
- Economist Intelligence Unit Democracy Index
- SIPRI Military Expenditure
- World Happiness Report

All values normalized to 0-100 scale matching simulator metrics.
Higher = better EXCEPT for: Crime Rate, Income Inequality, Corruption Index, Coup Count
"""

WORLD_COUNTRIES = {
    "Norway 🇳🇴": {
        "GDP": 88, "Social Trust": 90, "Education Index": 92, "Crime Rate": 15,
        "Democracy Score": 98, "Coup Count": 0, "Amendments Passed": 12,
        "Healthcare Quality": 95, "Press Freedom": 97, "Income Inequality": 25,
        "Tech Innovation": 85, "Environment Health": 90, "Military Power": 55,
        "Infrastructure": 92, "Corruption Index": 12, "Happiness Index": 93
    },
    "Sweden 🇸🇪": {
        "GDP": 84, "Social Trust": 88, "Education Index": 90, "Crime Rate": 22,
        "Democracy Score": 96, "Coup Count": 0, "Amendments Passed": 10,
        "Healthcare Quality": 93, "Press Freedom": 96, "Income Inequality": 28,
        "Tech Innovation": 88, "Environment Health": 88, "Military Power": 52,
        "Infrastructure": 90, "Corruption Index": 14, "Happiness Index": 91
    },
    "Denmark 🇩🇰": {
        "GDP": 85, "Social Trust": 87, "Education Index": 89, "Crime Rate": 20,
        "Democracy Score": 97, "Coup Count": 0, "Amendments Passed": 8,
        "Healthcare Quality": 92, "Press Freedom": 94, "Income Inequality": 27,
        "Tech Innovation": 83, "Environment Health": 86, "Military Power": 48,
        "Infrastructure": 91, "Corruption Index": 10, "Happiness Index": 92
    },
    "Finland 🇫🇮": {
        "GDP": 82, "Social Trust": 89, "Education Index": 95, "Crime Rate": 18,
        "Democracy Score": 97, "Coup Count": 0, "Amendments Passed": 7,
        "Healthcare Quality": 90, "Press Freedom": 98, "Income Inequality": 26,
        "Tech Innovation": 86, "Environment Health": 87, "Military Power": 50,
        "Infrastructure": 89, "Corruption Index": 11, "Happiness Index": 94
    },
    "United States 🇺🇸": {
        "GDP": 92, "Social Trust": 52, "Education Index": 80, "Crime Rate": 55,
        "Democracy Score": 78, "Coup Count": 0, "Amendments Passed": 27,
        "Healthcare Quality": 78, "Press Freedom": 70, "Income Inequality": 62,
        "Tech Innovation": 98, "Environment Health": 58, "Military Power": 99,
        "Infrastructure": 75, "Corruption Index": 38, "Happiness Index": 70
    },
    "Germany 🇩🇪": {
        "GDP": 88, "Social Trust": 72, "Education Index": 87, "Crime Rate": 30,
        "Democracy Score": 92, "Coup Count": 0, "Amendments Passed": 65,
        "Healthcare Quality": 90, "Press Freedom": 82, "Income Inequality": 38,
        "Tech Innovation": 85, "Environment Health": 78, "Military Power": 70,
        "Infrastructure": 88, "Corruption Index": 20, "Happiness Index": 78
    },
    "France 🇫🇷": {
        "GDP": 82, "Social Trust": 60, "Education Index": 85, "Crime Rate": 42,
        "Democracy Score": 88, "Coup Count": 0, "Amendments Passed": 24,
        "Healthcare Quality": 88, "Press Freedom": 75, "Income Inequality": 42,
        "Tech Innovation": 78, "Environment Health": 72, "Military Power": 80,
        "Infrastructure": 86, "Corruption Index": 30, "Happiness Index": 71
    },
    "United Kingdom 🇬🇧": {
        "GDP": 83, "Social Trust": 65, "Education Index": 86, "Crime Rate": 38,
        "Democracy Score": 90, "Coup Count": 0, "Amendments Passed": 15,
        "Healthcare Quality": 82, "Press Freedom": 78, "Income Inequality": 48,
        "Tech Innovation": 82, "Environment Health": 68, "Military Power": 78,
        "Infrastructure": 82, "Corruption Index": 22, "Happiness Index": 73
    },
    "Japan 🇯🇵": {
        "GDP": 86, "Social Trust": 80, "Education Index": 92, "Crime Rate": 12,
        "Democracy Score": 82, "Coup Count": 0, "Amendments Passed": 1,
        "Healthcare Quality": 94, "Press Freedom": 60, "Income Inequality": 35,
        "Tech Innovation": 92, "Environment Health": 62, "Military Power": 68,
        "Infrastructure": 93, "Corruption Index": 25, "Happiness Index": 62
    },
    "South Korea 🇰🇷": {
        "GDP": 80, "Social Trust": 55, "Education Index": 90, "Crime Rate": 22,
        "Democracy Score": 80, "Coup Count": 2, "Amendments Passed": 9,
        "Healthcare Quality": 85, "Press Freedom": 52, "Income Inequality": 40,
        "Tech Innovation": 88, "Environment Health": 48, "Military Power": 72,
        "Infrastructure": 88, "Corruption Index": 35, "Happiness Index": 59
    },
    "Canada 🇨🇦": {
        "GDP": 85, "Social Trust": 75, "Education Index": 88, "Crime Rate": 35,
        "Democracy Score": 93, "Coup Count": 0, "Amendments Passed": 5,
        "Healthcare Quality": 85, "Press Freedom": 85, "Income Inequality": 40,
        "Tech Innovation": 80, "Environment Health": 75, "Military Power": 55,
        "Infrastructure": 82, "Corruption Index": 18, "Happiness Index": 80
    },
    "Australia 🇦🇺": {
        "GDP": 84, "Social Trust": 73, "Education Index": 87, "Crime Rate": 32,
        "Democracy Score": 92, "Coup Count": 0, "Amendments Passed": 8,
        "Healthcare Quality": 86, "Press Freedom": 83, "Income Inequality": 44,
        "Tech Innovation": 78, "Environment Health": 68, "Military Power": 58,
        "Infrastructure": 80, "Corruption Index": 20, "Happiness Index": 79
    },
    "Brazil 🇧🇷": {
        "GDP": 42, "Social Trust": 35, "Education Index": 60, "Crime Rate": 78,
        "Democracy Score": 65, "Coup Count": 5, "Amendments Passed": 32,
        "Healthcare Quality": 55, "Press Freedom": 55, "Income Inequality": 80,
        "Tech Innovation": 48, "Environment Health": 45, "Military Power": 60,
        "Infrastructure": 48, "Corruption Index": 65, "Happiness Index": 52
    },
    "Russia 🇷🇺": {
        "GDP": 52, "Social Trust": 38, "Education Index": 72, "Crime Rate": 52,
        "Democracy Score": 22, "Coup Count": 1, "Amendments Passed": 2,
        "Healthcare Quality": 58, "Press Freedom": 22, "Income Inequality": 68,
        "Tech Innovation": 60, "Environment Health": 40, "Military Power": 90,
        "Infrastructure": 62, "Corruption Index": 72, "Happiness Index": 42
    },
    "China 🇨🇳": {
        "GDP": 70, "Social Trust": 60, "Education Index": 78, "Crime Rate": 30,
        "Democracy Score": 15, "Coup Count": 0, "Amendments Passed": 5,
        "Healthcare Quality": 65, "Press Freedom": 12, "Income Inequality": 70,
        "Tech Innovation": 82, "Environment Health": 35, "Military Power": 88,
        "Infrastructure": 82, "Corruption Index": 58, "Happiness Index": 55
    },
    "India 🇮🇳": {
        "GDP": 45, "Social Trust": 48, "Education Index": 62, "Crime Rate": 48,
        "Democracy Score": 68, "Coup Count": 0, "Amendments Passed": 105,
        "Healthcare Quality": 52, "Press Freedom": 45, "Income Inequality": 72,
        "Tech Innovation": 65, "Environment Health": 38, "Military Power": 75,
        "Infrastructure": 55, "Corruption Index": 60, "Happiness Index": 45
    },
    "South Africa 🇿🇦": {
        "GDP": 38, "Social Trust": 30, "Education Index": 55, "Crime Rate": 82,
        "Democracy Score": 72, "Coup Count": 0, "Amendments Passed": 17,
        "Healthcare Quality": 48, "Press Freedom": 62, "Income Inequality": 88,
        "Tech Innovation": 42, "Environment Health": 42, "Military Power": 45,
        "Infrastructure": 50, "Corruption Index": 62, "Happiness Index": 40
    },
    "Venezuela 🇻🇪": {
        "GDP": 18, "Social Trust": 20, "Education Index": 48, "Crime Rate": 88,
        "Democracy Score": 20, "Coup Count": 3, "Amendments Passed": 4,
        "Healthcare Quality": 25, "Press Freedom": 20, "Income Inequality": 78,
        "Tech Innovation": 25, "Environment Health": 38, "Military Power": 40,
        "Infrastructure": 28, "Corruption Index": 82, "Happiness Index": 25
    },
    "Singapore 🇸🇬": {
        "GDP": 90, "Social Trust": 75, "Education Index": 92, "Crime Rate": 8,
        "Democracy Score": 55, "Coup Count": 0, "Amendments Passed": 18,
        "Healthcare Quality": 92, "Press Freedom": 40, "Income Inequality": 55,
        "Tech Innovation": 92, "Environment Health": 65, "Military Power": 62,
        "Infrastructure": 97, "Corruption Index": 8, "Happiness Index": 70
    },
    "North Korea 🇰🇵": {
        "GDP": 8, "Social Trust": 30, "Education Index": 52, "Crime Rate": 35,
        "Democracy Score": 2, "Coup Count": 0, "Amendments Passed": 1,
        "Healthcare Quality": 25, "Press Freedom": 2, "Income Inequality": 60,
        "Tech Innovation": 15, "Environment Health": 40, "Military Power": 65,
        "Infrastructure": 20, "Corruption Index": 88, "Happiness Index": 15
    },
}

# Regional groupings for filtering
REGIONS = {
    "Nordic": ["Norway 🇳🇴", "Sweden 🇸🇪", "Denmark 🇩🇰", "Finland 🇫🇮"],
    "Western Powers": ["United States 🇺🇸", "Germany 🇩🇪", "France 🇫🇷", "United Kingdom 🇬🇧"],
    "Asian Democracies": ["Japan 🇯🇵", "South Korea 🇰🇷", "Australia 🇦🇺", "India 🇮🇳"],
    "Authoritarian States": ["China 🇨🇳", "Russia 🇷🇺", "North Korea 🇰🇵", "Venezuela 🇻🇪"],
    "Emerging Markets": ["Brazil 🇧🇷", "India 🇮🇳", "South Africa 🇿🇦"],
    "City States": ["Singapore 🇸🇬"],
    "Anglo-Saxon": ["United States 🇺🇸", "United Kingdom 🇬🇧", "Canada 🇨🇦", "Australia 🇦🇺"],
}
