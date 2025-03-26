
import streamlit as st

st.set_page_config(page_title="Traveler Type Classifier", layout="centered")
st.title("🚆 Traveler Type Classifier")

st.markdown("""
_With this small app, you can discover your travel personality and receive suggested rail routes that best match your traveler type for a more enriching rail experience._

Please rate each statement from **1 (Not Important)** to **5 (Very Important)**.
Your responses will help us determine what type of traveler you are!
""")

# Questions & Metadata
questionnaire = {
    "DT1": "High-speed Wi-Fi on trains",
    "DT2": "Ease of online booking",
    "DT3": "Real-time info on mobile apps",
    "DT4": "Personalized digital services",
    "HS1": "Cleanliness and hygiene",
    "HS2": "Spacious seating",
    "HS3": "Health and safety tech",
    "HS4": "Reduced passenger interaction",
    "SU1": "Environmental sustainability",
    "SU2": "Use of green technologies",
    "SU3": "Sustainable practices commitment",
    "SU4": "Renewable energy use",
    "RA1": "Access to rural areas",
    "RA2": "Scenic routes",
    "RA3": "Cultural/historical sites",
    "RA4": "Immersive rural experiences",
    "RA5": "Bicycle boarding option",
    "LX1": "Luxury and comfort",
    "LX2": "Private/personalized services",
    "LX3": "Luxury amenities",
    "LX4": "Entertainment and programming"
}

indicator_weights = {
    'DT1': 0.223197, 'DT2': 0.178092, 'DT3': 0.171690, 'DT4': 0.214467,
    'HS1': 0.247296, 'HS2': 0.263718, 'HS3': 0.268548, 'HS4': 0.189980,
    'SU1': 0.186825, 'SU2': 0.221840, 'SU3': 0.223485, 'SU4': 0.222075,
    'RA1': 0.140420, 'RA2': 0.206108, 'RA3': 0.195398, 'RA4': 0.200396, 'RA5': 0.055454,
    'LX1': 0.249352, 'LX2': 0.224360, 'LX3': 0.233732, 'LX4': 0.213852
}

indicator_to_construct = {
    'DT1': 'Digital', 'DT2': 'Digital', 'DT3': 'Digital', 'DT4': 'Digital',
    'HS1': 'Health', 'HS2': 'Health', 'HS3': 'Health', 'HS4': 'Health',
    'SU1': 'Sustainability', 'SU2': 'Sustainability', 'SU3': 'Sustainability', 'SU4': 'Sustainability',
    'RA1': 'Rural', 'RA2': 'Rural', 'RA3': 'Rural', 'RA4': 'Rural', 'RA5': 'Rural',
    'LX1': 'Luxury', 'LX2': 'Luxury', 'LX3': 'Luxury', 'LX4': 'Luxury'
}

constructs = set(indicator_to_construct.values())
scores = {k: 0.0 for k in constructs}

responses = {}
for code, question in questionnaire.items():
    response = st.slider(f"{code}: {question}", 1, 5, 3)
    responses[code] = response
    weight = indicator_weights[code]
    construct = indicator_to_construct[code]
    scores[construct] += response * weight

def classify(scores):
    top_two = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
    top1, top2 = top_two[0][0], top_two[1][0]

    hybrid = {
        ('Sustainability', 'Rural'): ("🌿🚴 Eco-Explorer", "Immersive travel in nature and rural areas with cultural depth."),
        ('Health', 'Digital'): ("🧘🧠 Health-Connected Explorer", "Seeks wellness and cleanliness through smart, digital systems."),
        ('Luxury', 'Digital'): ("💼🧠 Tech-Savvy Luxury Traveler", "Loves luxury, speed, and digital convenience."),
        ('Luxury', 'Sustainability'): ("💼🌿 Eco-Lux Traveler", "Combines high-end comfort with eco-conscious values."),
        ('Health', 'Rural'): ("🧘🚴 Active Wellness Nomad", "Prefers space, nature, biking, and clean journeys.")
    }

    base = {
        'Digital': ("🧠 Always-Connected Traveler", "Values digital tools, apps, and seamless connectivity."),
        'Health': ("🧘 Health-Aware Passenger", "Cares about cleanliness, safety, and peace of mind."),
        'Sustainability': ("🌿 Value-Aligned Eco Traveler", "Prioritizes low carbon, green trains, and eco credentials."),
        'Rural': ("🚴 Multimodal Nomad", "Loves slow travel, remote areas, and multi-modal freedom."),
        'Luxury': ("💼 Mindful Luxury Traveler", "Enjoys exclusive, quiet, and premium onboard experiences.")
    }

    key = tuple(sorted([top1, top2]))
    if key in hybrid:
        return hybrid[key], [top1, top2]
    return base[top1], [top1]

if st.button("Classify Me!"):
    (traveler_type, guidance), relevant = classify(scores)
    st.subheader(f"🎉 You are: {traveler_type}")
    st.info(guidance)

    suggestions = {
        'Luxury': ["Venice Simplon-Orient-Express", "Glacier Express", "Golden Eagle Trans-Siberian", "Royal Scotsman"],
        'Sustainability': ["Bernina Express", "West Highland Line", "Biosfera Train"],
        'Rural': ["Danube Bike & Rail Path", "Ligurian Cycle-Rail Paths", "Loire à Vélo Rail"],
        'Digital': ["Dutch & German Rail (Digital-First)", "Trenitalia Frecciarossa"],
        'Health': ["Swiss/Austrian Wellness Trains", "German Quiet Zones", "Czech Spa Routes"]
    }

    st.markdown("**Suggested Routes:**")
    for tag in relevant:
        if tag in suggestions:
            for route in suggestions[tag]:
                st.markdown(f"- {route}")

    st.caption("App Created by Alireza Moradpour – Based on Master's Thesis Research in Future Rail Tourism.")
