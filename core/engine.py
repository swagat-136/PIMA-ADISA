import random
import copy

# The 16 Metrics
METRIC_KEYS = [
    "GDP", "Social Trust", "Education Index", "Crime Rate", 
    "Democracy Score", "Coup Count", "Amendments Passed",
    "Healthcare Quality", "Press Freedom", "Income Inequality",
    "Tech Innovation", "Environment Health", "Military Power",
    "Infrastructure", "Corruption Index", "Happiness Index",
    "Accuracy", "Fairness", "Privacy Risk", "Governance Trust", 
    "AI Legitimacy", "Bias Risk", "Citizen Satisfaction", "Surveillance Level"
]

PILLAR_MAP = {
    "💰 Money": ["GDP", "Infrastructure", "Tech Innovation"],
    "🕊️ Freedom": ["Democracy Score", "Press Freedom", "Amendments Passed"],
    "😊 Happiness": ["Happiness Index", "Healthcare Quality", "Education Index", "Environment Health", "Social Trust"],
    "🛡️ Safety": ["Crime Rate", "Coup Count", "Military Power", "Surveillance Level"],
    "🤖 AI Health": ["Accuracy", "Fairness", "AI Legitimacy", "Governance Trust", "Privacy Risk", "Bias Risk"]
}

def get_pillar_scores(state):
    """Calculates averaged scores for 5 core pillars."""
    scores = {}
    for pillar, keys in PILLAR_MAP.items():
        vals = []
        for k in keys:
            v = state.get(k, 50)
            # Invert negative metrics for the pillar average
            if k in ["Crime Rate", "Coup Count", "Privacy Risk", "Bias Risk"]:
                vals.append(100 - v)
            else:
                vals.append(v)
        scores[pillar] = sum(vals) / len(vals)
    return scores

def get_status_details(score):
    """Returns (label, color, icon) for a given 0-100 score."""
    if score >= 81:
        return "THRIVING", "#00C897", "⭐"
    elif score >= 61:
        return "GOOD", "#4ECDC4", "🟢"
    elif score >= 41:
        return "STABLE", "#F9D423", "🟡"
    elif score >= 21:
        return "AT RISK", "#FF7043", "⚠️"
    else:
        return "CRISIS", "#FF4B4B", "🚨"

def init_mock_state():
    """Initializes a mostly neutral dictionary of the 16 metrics for Year 0."""
    return {
        "Year": 2024,
        "GDP": 50.0,
        "Social Trust": 60.0,
        "Education Index": 65.0,
        "Crime Rate": 40.0,
        "Democracy Score": 70.0,
        "Coup Count": 0.0,
        "Amendments Passed": 0.0,
        "Healthcare Quality": 60.0,
        "Press Freedom": 65.0,
        "Income Inequality": 50.0,
        "Tech Innovation": 45.0,
        "Environment Health": 55.0,
        "Military Power": 40.0,
        "Infrastructure": 50.0,
        "Corruption Index": 45.0,
        "Happiness Index": 60.0,
        "Accuracy": 85.0,
        "Fairness": 75.0,
        "Privacy Risk": 30.0,
        "Governance Trust": 65.0,
        "AI Legitimacy": 70.0,
        "Bias Risk": 25.0,
        "Citizen Satisfaction": 60.0,
        "Surveillance Level": 20.0
    }

def get_regime_type(state):
    """
    Classifies the current state of society based on Democracy Score, Coup Count, etc.
    Possible Outputs: Liberal Democracy, Electoral Democracy, Hybrid, Authoritarian, Autocracy, Theocracy
    """
    ds = state.get("Democracy Score", 50)
    cc = state.get("Coup Count", 0)
    pf = state.get("Press Freedom", 50)
    st = state.get("Social Trust", 50)

    if ds >= 85 and pf >= 80:
        return "Liberal Democracy 🕊️"
    elif ds >= 60:
        return "Electoral Democracy 🗳️"
    elif ds >= 40:
        if cc > 1:
            return "Hybrid Regime ⚖️"
        else:
            return "Illiberal Democracy 🏛️"
    elif ds >= 20:
        # Just an arbitrary rule for theocracy: low democracy, high social trust (conformity)
        if st > 70 and pf < 30:
            return "Theocracy ⛪"
        return "Authoritarian Regime ⛓️"
    else:
        return "Autocracy 👑"

def apply_event(state, event_name):
    """Applies metric modifiers based on an event"""
    ns = copy.deepcopy(state)
    
    # We step the year by 1 when an event (or just a turn) occurs
    ns["Year"] += 1

    actions_log = f"Year {ns['Year']}: {event_name.upper()} Triggered.\\n"

    if event_name == "Coup":
        ns["Coup Count"] += 1
        ns["Democracy Score"] -= 20
        ns["Military Power"] += 15
        ns["Social Trust"] -= 25
        ns["Press Freedom"] -= 30
        ns["Crime Rate"] += 20
        ns["GDP"] -= 15
        ns["Happiness Index"] -= 20
        ns["Governance Trust"] -= 40
        ns["AI Legitimacy"] -= 30
        ns["Accuracy"] -= 10
    elif event_name == "Civil War":
        ns["Democracy Score"] -= 30
        ns["Infrastructure"] -= 40
        ns["Healthcare Quality"] -= 30
        ns["Education Index"] -= 20
        ns["GDP"] -= 35
        ns["Social Trust"] -= 40
        ns["Crime Rate"] += 40
        ns["Military Power"] += 25
    elif event_name == "Election Reform":
        ns["Democracy Score"] += 15
        ns["Amendments Passed"] += 1
        ns["Social Trust"] += 10
        ns["Corruption Index"] -= 15
        ns["Press Freedom"] += 10
        ns["Governance Trust"] += 15
        ns["AI Legitimacy"] += 10
    elif event_name == "Tech Revolution":
        ns["Tech Innovation"] += 30
        ns["GDP"] += 20
        ns["Education Index"] += 10
        ns["Income Inequality"] += 15
        ns["Infrastructure"] += 15
        ns["Accuracy"] += 20
        ns["Tech Innovation"] += 15
    elif event_name == "Amnesty":
        ns["Crime Rate"] -= 10
        ns["Social Trust"] += 15
        ns["Happiness Index"] += 10
        ns["Press Freedom"] += 5
    elif event_name == "Green New Deal":
        ns["Environment Health"] += 30
        ns["GDP"] -= 8
        ns["Tech Innovation"] += 10
        ns["Happiness Index"] += 12
        ns["Infrastructure"] += 10
    elif event_name == "Anti-Corruption Drive":
        ns["Corruption Index"] -= 25
        ns["GDP"] += 10
        ns["Social Trust"] += 15
        ns["Democracy Score"] += 8
        ns["Press Freedom"] += 8
        ns["Governance Trust"] += 20
        ns["Bias Risk"] -= 15
    elif event_name == "Universal Healthcare":
        ns["Healthcare Quality"] += 30
        ns["Happiness Index"] += 20
        ns["GDP"] -= 10
        ns["Social Trust"] += 10
        ns["Education Index"] += 5
    elif event_name == "Education Revolution":
        ns["Education Index"] += 25
        ns["Tech Innovation"] += 15
        ns["GDP"] += 8
        ns["Social Trust"] += 8
        ns["Income Inequality"] -= 10
    elif event_name == "Foreign Invasion":
        ns["Military Power"] += 10
        ns["GDP"] -= 25
        ns["Infrastructure"] -= 30
        ns["Healthcare Quality"] -= 15
        ns["Social Trust"] -= 20
        ns["Crime Rate"] += 15
        ns["Happiness Index"] -= 25
    elif event_name == "Market Crash":
        ns["GDP"] -= 35
        ns["Income Inequality"] += 20
        ns["Crime Rate"] += 20
        ns["Social Trust"] -= 20
        ns["Happiness Index"] -= 25
        ns["Corruption Index"] += 10
    elif event_name == "Peace Treaty":
        ns["Military Power"] -= 10
        ns["Social Trust"] += 20
        ns["GDP"] += 15
        ns["Happiness Index"] += 20
        ns["Infrastructure"] += 10
        ns["Democracy Score"] += 10
    elif event_name == "Standard Year Progression":
        pass # just tick the year

    # Clamp all metrics (except Year, Coup Count, and Amendments) between 0 and 100
    for k, v in ns.items():
        if k not in ["Year", "Coup Count", "Amendments Passed"]:
            ns[k] = max(0.0, min(100.0, v))
            
    return ns

def get_empty_log():
    """Returns a structure for the Governance Ledger."""
    return []

def log_event(state, event_name, impact_summary):
    """Adds an entry to the governance ledger (stored in session state)."""
    if "ledger" not in state:
        state["ledger"] = []
    state["ledger"].append({
        "Year": state["Year"],
        "Event": event_name,
        "Impact": impact_summary
    })

def apply_policy_impact(state, policies):
    """
    Calculates the impact of continuous policy sliders on nation metrics.
    policies: dict of slider values (0-100)
    """
    ns = copy.deepcopy(state)
    ns["Year"] += 1
    
    # ── Policy Logic ────────────────────────────────────────────────────────
    # Transparency improves trust, reduces corruption
    transparency = policies.get("Transparency", 50)
    ns["Governance Trust"] += (transparency - 50) * 0.2
    ns["Corruption Index"] -= (transparency - 50) * 0.15
    
    # Surveillance reduces crime but tanks privacy and trust
    surveillance = policies.get("Surveillance", 20)
    ns["Surveillance Level"] = surveillance
    ns["Crime Rate"] = ns.get("Crime Rate", 40) - (surveillance - 20) * 0.3
    ns["Privacy Risk"] = ns.get("Privacy Risk", 30) + (surveillance - 20) * 0.4
    ns["Social Trust"] = ns.get("Social Trust", 60) - (surveillance - 20) * 0.2
    
    # Oversight reduces bias risk and improves AI legitimacy
    oversight = policies.get("Oversight", 50)
    ns["Bias Risk"] = ns.get("Bias Risk", 25) - (oversight - 50) * 0.2
    ns["AI Legitimacy"] = ns.get("AI Legitimacy", 70) + (oversight - 50) * 0.15
    
    # Health Digitization improves quality but risks privacy
    health_digi = policies.get("Health Digitization", 50)
    ns["Healthcare Quality"] = ns.get("Healthcare Quality", 60) + (health_digi - 50) * 0.2
    ns["Privacy Risk"] = ns.get("Privacy Risk", 30) + (health_digi - 50) * 0.1
    
    # Education Investment - long term growth
    edu_invest = policies.get("Education Investment", 50)
    ns["Education Index"] += (edu_invest - 50) * 0.25
    ns["Tech Innovation"] += (edu_invest - 50) * 0.15
    
    # Clamp results
    for k, v in ns.items():
        if k in METRIC_KEYS:
            ns[k] = max(0.0, min(100.0, v))
            
    return ns
