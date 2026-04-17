"""
Historical Constitutional Scenarios Dataset
Curated data representing real historical governance transitions.
Each scenario has:
- A starting state (normalized to 0-100)
- A sequence of historical events
- Key lessons learned
- Notable outcomes
"""

HISTORICAL_SCENARIOS = {
    "Weimar Republic Collapse (1919-1933)": {
        "description": (
            "Germany's Weimar Republic began as a promising democracy after WWI "
            "but collapsed under extreme hyperinflation, political polarization, "
            "rising paramilitary violence, and economic depression, ultimately "
            "giving rise to Adolf Hitler's Nazi regime."
        ),
        "era": "1919–1933",
        "region": "Europe",
        "category": "Democratic Collapse",
        "icon": "🏚️",
        "starting_state": {
            "Year": 1919, "GDP": 30, "Social Trust": 40, "Education Index": 72,
            "Crime Rate": 55, "Democracy Score": 65, "Coup Count": 2,
            "Amendments Passed": 4, "Healthcare Quality": 40, "Press Freedom": 70,
            "Income Inequality": 72, "Tech Innovation": 45, "Environment Health": 50,
            "Military Power": 35, "Infrastructure": 45, "Corruption Index": 55,
            "Happiness Index": 28
        },
        "event_sequence": [
            ("Hyperinflation Crisis", {"GDP": -35, "Happiness Index": -30, "Social Trust": -25, "Crime Rate": 20}),
            ("Great Depression Shock", {"GDP": -20, "Income Inequality": 15, "Crime Rate": 15, "Democracy Score": -15}),
            ("Paramilitary Violence", {"Crime Rate": 25, "Press Freedom": -20, "Social Trust": -20, "Military Power": 10}),
            ("Emergency Decree Rule", {"Democracy Score": -30, "Press Freedom": -25, "Coup Count": 1, "Corruption Index": 15}),
            ("Nazi Seizure of Power", {"Democracy Score": -40, "Press Freedom": -50, "Social Trust": -30, "Crime Rate": 20, "Coup Count": 1}),
        ],
        "lessons": [
            "Hyperinflation destroys the social contract faster than any military threat",
            "Proportional representation without safeguards enables extremism",
            "Economic desperation precedes democratic collapse by 3-5 years",
            "Emergency powers, once granted, are rarely returned",
            "Institutional erosion is gradual until it suddenly isn't"
        ],
        "final_outcome": "Totalitarian Regime",
        "resilience_score": 8
    },

    "Nordic Social Democracy Rise (1930-1970)": {
        "description": (
            "Sweden, Norway, and Denmark transformed from moderate capitalist states "
            "into the world's leading social democracies through cross-class compromise, "
            "strong unions, and a 'historical compromise' between labor and capital. "
            "The result was high equality, high trust, and sustained prosperity."
        ),
        "era": "1930–1970",
        "region": "Scandinavia",
        "category": "Democratic Flourishing",
        "icon": "🌿",
        "starting_state": {
            "Year": 1930, "GDP": 45, "Social Trust": 55, "Education Index": 65,
            "Crime Rate": 30, "Democracy Score": 72, "Coup Count": 0,
            "Amendments Passed": 3, "Healthcare Quality": 45, "Press Freedom": 80,
            "Income Inequality": 58, "Tech Innovation": 35, "Environment Health": 70,
            "Military Power": 35, "Infrastructure": 50, "Corruption Index": 40,
            "Happiness Index": 52
        },
        "event_sequence": [
            ("Class Compromise Pact", {"Social Trust": 20, "Income Inequality": -15, "Democracy Score": 10, "Happiness Index": 15}),
            ("Universal Healthcare Expansion", {"Healthcare Quality": 30, "Social Trust": 10, "GDP": -5, "Happiness Index": 20}),
            ("Education Revolution", {"Education Index": 25, "Tech Innovation": 15, "GDP": 10, "Social Trust": 8}),
            ("Press Freedom Consolidation", {"Press Freedom": 15, "Democracy Score": 8, "Social Trust": 10, "Corruption Index": -15}),
            ("Welfare State Maturation", {"Happiness Index": 25, "Income Inequality": -20, "Healthcare Quality": 15, "GDP": 15}),
        ],
        "lessons": [
            "Cross-class compromise is the foundation of lasting stability",
            "Investing in education precedes economic growth by a decade",
            "Universal healthcare boosts social trust more than any single policy",
            "Strong press freedom creates self-correcting institutions",
            "Equality and prosperity reinforce each other in a virtuous cycle"
        ],
        "final_outcome": "Liberal Democracy",
        "resilience_score": 94
    },

    "Arab Spring & Aftermath (2010-2015)": {
        "description": (
            "Mass protests swept the Arab world beginning in Tunisia (2010), "
            "spreading to Egypt, Libya, Syria, Yemen, and Bahrain. While Tunisia "
            "achieved a democratic transition, most nations descended into civil war, "
            "military coups, or authoritarian re-consolidation."
        ),
        "era": "2010–2015",
        "region": "Middle East & North Africa",
        "category": "Revolutionary Wave",
        "icon": "🌊",
        "starting_state": {
            "Year": 2010, "GDP": 35, "Social Trust": 30, "Education Index": 52,
            "Crime Rate": 45, "Democracy Score": 25, "Coup Count": 1,
            "Amendments Passed": 1, "Healthcare Quality": 42, "Press Freedom": 22,
            "Income Inequality": 70, "Tech Innovation": 35, "Environment Health": 40,
            "Military Power": 60, "Infrastructure": 48, "Corruption Index": 72,
            "Happiness Index": 32
        },
        "event_sequence": [
            ("Popular Uprising", {"Democracy Score": 20, "Social Trust": -10, "Crime Rate": 15, "Press Freedom": 15, "Military Power": -10}),
            ("Military Intervention", {"Democracy Score": -15, "Military Power": 20, "Crime Rate": 10, "Press Freedom": -10, "Coup Count": 1}),
            ("Constitutional Crisis", {"Social Trust": -20, "Democracy Score": -10, "GDP": -15, "Infrastructure": -10}),
            ("Foreign Intervention", {"Military Power": -15, "Infrastructure": -25, "GDP": -20, "Healthcare Quality": -20}),
            ("Counter-Revolution", {"Democracy Score": -20, "Press Freedom": -20, "Coup Count": 1, "Social Trust": -15, "Corruption Index": 10}),
        ],
        "lessons": [
            "Mass mobilization without institutional channels leads to chaos",
            "Military loyalty is the decisive variable in revolutionary outcomes",
            "Economic grievances require economic solutions, not just political ones",
            "Foreign intervention almost always worsens long-term outcomes",
            "Constitutional design in crisis moments determines decades of politics"
        ],
        "final_outcome": "Authoritarian Regime",
        "resilience_score": 18
    },

    "Singapore's Lee Kuan Yew Model (1965-2000)": {
        "description": (
            "Singapore emerged from British colonialism as a tiny city-state with no "
            "natural resources. Under Lee Kuan Yew's PAP government, it achieved "
            "spectacular economic growth, low corruption, and strong infrastructure — "
            "but at the cost of press freedom, political pluralism, and civil liberties."
        ),
        "era": "1965–2000",
        "region": "Southeast Asia",
        "category": "Developmental Authoritarianism",
        "icon": "🏙️",
        "starting_state": {
            "Year": 1965, "GDP": 20, "Social Trust": 45, "Education Index": 45,
            "Crime Rate": 55, "Democracy Score": 45, "Coup Count": 0,
            "Amendments Passed": 2, "Healthcare Quality": 35, "Press Freedom": 40,
            "Income Inequality": 55, "Tech Innovation": 20, "Environment Health": 40,
            "Military Power": 20, "Infrastructure": 25, "Corruption Index": 60,
            "Happiness Index": 40
        },
        "event_sequence": [
            ("Anti-Corruption Drive", {"Corruption Index": -35, "Social Trust": 15, "GDP": 10, "Infrastructure": 10}),
            ("Export-Led Industrialization", {"GDP": 30, "Tech Innovation": 20, "Infrastructure": 25, "Income Inequality": 10}),
            ("Education Investment Surge", {"Education Index": 35, "Tech Innovation": 15, "GDP": 15, "Social Trust": 10}),
            ("Press Restrictions Tighten", {"Press Freedom": -25, "Democracy Score": -15, "Social Trust": -5, "Crime Rate": -10}),
            ("Global Finance Hub Status", {"GDP": 30, "Tech Innovation": 20, "Infrastructure": 15, "Happiness Index": 20}),
        ],
        "lessons": [
            "Anti-corruption is the single highest-ROI reform any state can make",
            "Export-led growth requires massive infrastructure investment first",
            "The 'Asian Values' trade-off: prosperity at the cost of political freedom",
            "Education investment has a 15-20 year time-horizon before ROI",
            "Small states can outperform large ones through institutional excellence"
        ],
        "final_outcome": "Hybrid Regime",
        "resilience_score": 78
    },

    "Soviet Union Collapse (1985-1991)": {
        "description": (
            "Mikhail Gorbachev's twin reforms — Glasnost (openness) and Perestroika "
            "(restructuring) — intended to modernize Soviet communism but instead "
            "unleashed centrifugal forces the system could not contain. The USSR "
            "dissolved into 15 independent states on December 25, 1991."
        ),
        "era": "1985–1991",
        "region": "Eastern Europe",
        "category": "State Collapse",
        "icon": "🧱",
        "starting_state": {
            "Year": 1985, "GDP": 55, "Social Trust": 42, "Education Index": 80,
            "Crime Rate": 30, "Democracy Score": 10, "Coup Count": 0,
            "Amendments Passed": 0, "Healthcare Quality": 60, "Press Freedom": 10,
            "Income Inequality": 35, "Tech Innovation": 62, "Environment Health": 40,
            "Military Power": 95, "Infrastructure": 65, "Corruption Index": 70,
            "Happiness Index": 38
        },
        "event_sequence": [
            ("Glasnost Media Liberalization", {"Press Freedom": 35, "Democracy Score": 15, "Social Trust": -5, "Corruption Index": -10}),
            ("Perestroika Economic Reforms", {"GDP": -20, "Income Inequality": 15, "Tech Innovation": -10, "Social Trust": -15}),
            ("Satellite State Breakaways", {"Military Power": -25, "GDP": -15, "Social Trust": -20, "Democracy Score": 10}),
            ("Coup Attempt", {"Coup Count": 1, "Democracy Score": 10, "Military Power": -15, "Social Trust": -25}),
            ("State Dissolution", {"GDP": -30, "Infrastructure": -20, "Military Power": -30, "Social Trust": -30, "Coup Count": 1}),
        ],
        "lessons": [
            "Controlled liberalization often becomes uncontrolled collapse",
            "Military-industrial states that cannot convert are economically fragile",
            "Corruption corrodes state legitimacy silently for decades before an acute crisis",
            "Nations held together by ideology collapse faster than ethnic ones",
            "Economic decline precedes political dissolution — not the other way around"
        ],
        "final_outcome": "State Dissolution → Multiple Democracies/Autocracies",
        "resilience_score": 15
    },

    "Rwanda's Recovery (1994-2020)": {
        "description": (
            "Following one of the worst genocides in history (800,000+ killed in 100 days), "
            "Rwanda rebuilt under President Paul Kagame. It achieved remarkable economic "
            "growth, eliminated corruption in key sectors, and improved human development — "
            "but remains a competitive authoritarian state with limited political pluralism."
        ),
        "era": "1994–2020",
        "region": "Sub-Saharan Africa",
        "category": "Post-Conflict Recovery",
        "icon": "🌱",
        "starting_state": {
            "Year": 1994, "GDP": 12, "Social Trust": 5, "Education Index": 28,
            "Crime Rate": 90, "Democracy Score": 20, "Coup Count": 2,
            "Amendments Passed": 1, "Healthcare Quality": 15, "Press Freedom": 20,
            "Income Inequality": 65, "Tech Innovation": 8, "Environment Health": 50,
            "Military Power": 45, "Infrastructure": 15, "Corruption Index": 80,
            "Happiness Index": 10
        },
        "event_sequence": [
            ("Genocide Tribunal & Reconciliation", {"Social Trust": 25, "Crime Rate": -30, "Democracy Score": 10, "Happiness Index": 15}),
            ("Anti-Corruption Drive", {"Corruption Index": -40, "GDP": 15, "Social Trust": 15, "Infrastructure": 10}),
            ("Universal Education Push", {"Education Index": 35, "Healthcare Quality": 15, "GDP": 10, "Tech Innovation": 12}),
            ("One-Party Stabilization", {"GDP": 20, "Infrastructure": 25, "Democracy Score": -10, "Press Freedom": -10, "Crime Rate": -15}),
            ("Tech & Innovation Hub Strategy", {"Tech Innovation": 30, "GDP": 20, "Infrastructure": 15, "Happiness Index": 20}),
        ],
        "lessons": [
            "Even the most catastrophic crises can be recovered from with decisive leadership",
            "Anti-corruption is a prerequisite for all other reforms in post-conflict states",
            "Economic recovery and democratic consolidation often trade off in the short term",
            "Education investment is the highest long-term predictor of stability",
            "National identity reconstruction is as important as physical reconstruction"
        ],
        "final_outcome": "Hybrid Regime / Developmental State",
        "resilience_score": 58
    },

    "Pinochet's Chile (1973-1990)": {
        "description": (
            "General Augusto Pinochet's military coup on September 11, 1973 overthrew "
            "democratically-elected Salvador Allende. The subsequent 17-year military "
            "dictatorship implemented radical free-market reforms (the 'Chicago Boys'), "
            "suppressing political opposition through torture, disappearances, and exile."
        ),
        "era": "1973–1990",
        "region": "Latin America",
        "category": "Military Coup & Economic Shock",
        "icon": "⚔️",
        "starting_state": {
            "Year": 1973, "GDP": 38, "Social Trust": 42, "Education Index": 68,
            "Crime Rate": 35, "Democracy Score": 72, "Coup Count": 0,
            "Amendments Passed": 3, "Healthcare Quality": 55, "Press Freedom": 65,
            "Income Inequality": 55, "Tech Innovation": 30, "Environment Health": 55,
            "Military Power": 55, "Infrastructure": 50, "Corruption Index": 45,
            "Happiness Index": 45
        },
        "event_sequence": [
            ("Military Coup", {"Coup Count": 1, "Democracy Score": -50, "Press Freedom": -45, "Crime Rate": 20, "Social Trust": -30, "Military Power": 20}),
            ("Chicago Boys Shock Therapy", {"GDP": 10, "Income Inequality": 25, "Healthcare Quality": -20, "Education Index": -10}),
            ("Political Repression", {"Crime Rate": 15, "Press Freedom": -15, "Social Trust": -15, "Democracy Score": -10, "Happiness Index": -20}),
            ("Economic Miracle Phase", {"GDP": 30, "Tech Innovation": 15, "Infrastructure": 20, "Income Inequality": 15}),
            ("Plebiscite & Transition", {"Democracy Score": 30, "Press Freedom": 20, "Social Trust": 10, "Coup Count": 0}),
        ],
        "lessons": [
            "Economic growth does not require democracy, but democracy sustains growth long-term",
            "Shock therapy creates inequality crises that outlast the economic gains",
            "Military coups have 40-year institutional aftershocks on social trust",
            "Constitutional design by a military can still create durable democratic frameworks",
            "International economic integration constrains authoritarian economic choices"
        ],
        "final_outcome": "Electoral Democracy (fragile)",
        "resilience_score": 45
    },

    "Post-WWII West Germany (1945-1969)": {
        "description": (
            "The Federal Republic of Germany rose from total destruction in 1945 — "
            "with the 'Stunde Null' (Zero Hour) — to become Europe's largest economy "
            "through the 'Wirtschaftswunder' (economic miracle). The Basic Law constitution "
            "was specifically designed with safeguards against Weimar-style collapse."
        ),
        "era": "1945–1969",
        "region": "Europe",
        "category": "Democratic Reconstruction",
        "icon": "🔨",
        "starting_state": {
            "Year": 1945, "GDP": 10, "Social Trust": 20, "Education Index": 60,
            "Crime Rate": 60, "Democracy Score": 30, "Coup Count": 0,
            "Amendments Passed": 0, "Healthcare Quality": 25, "Press Freedom": 35,
            "Income Inequality": 50, "Tech Innovation": 40, "Environment Health": 30,
            "Military Power": 5, "Infrastructure": 10, "Corruption Index": 55,
            "Happiness Index": 15
        },
        "event_sequence": [
            ("Marshall Plan Injection", {"GDP": 30, "Infrastructure": 35, "Healthcare Quality": 20, "Social Trust": 15}),
            ("Basic Law Constitution Ratified", {"Democracy Score": 40, "Press Freedom": 40, "Amendments Passed": 1, "Social Trust": 20}),
            ("Economic Miracle (Wirtschaftswunder)", {"GDP": 35, "Tech Innovation": 25, "Infrastructure": 20, "Happiness Index": 30}),
            ("Denazification & Re-Education", {"Education Index": 20, "Social Trust": 10, "Crime Rate": -25, "Corruption Index": -20}),
            ("European Integration", {"GDP": 10, "Social Trust": 15, "Democracy Score": 10, "Trade": 20, "Happiness Index": 15}),
        ],
        "lessons": [
            "External financial aid (Marshall Plan) was essential but insufficient alone",
            "Constitutional design must explicitly learn from past failures",
            "Economic reconstruction must precede democratic consolidation",
            "Accountability for past atrocities builds long-term institutional trust",
            "Regional integration creates economic and security incentives for stability"
        ],
        "final_outcome": "Liberal Democracy",
        "resilience_score": 88
    },
}

# Category colors for UI
CATEGORY_COLORS = {
    "Democratic Collapse": "#FF4B4B",
    "Democratic Flourishing": "#00C897",
    "Revolutionary Wave": "#FF9500",
    "Developmental Authoritarianism": "#6C5CE7",
    "State Collapse": "#E17055",
    "Post-Conflict Recovery": "#00B4D8",
    "Military Coup & Economic Shock": "#D63031",
    "Democratic Reconstruction": "#2ECC71",
}

CATEGORY_ICONS = {
    "Democratic Collapse": "🏚️",
    "Democratic Flourishing": "🌿",
    "Revolutionary Wave": "🌊",
    "Developmental Authoritarianism": "🏙️",
    "State Collapse": "🧱",
    "Post-Conflict Recovery": "🌱",
    "Military Coup & Economic Shock": "⚔️",
    "Democratic Reconstruction": "🔨",
}
