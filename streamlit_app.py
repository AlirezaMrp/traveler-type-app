
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Traveler Type Classifier", layout="centered")
st.title("🚆 Traveler Type Classifier")

st.markdown("""
_With this small app, you can discover your travel personality and receive suggested rail routes that best match your traveler type for a more enriching rail experience._

Please rate each statement from **1 (Not Important)** to **5 (Very Important)**.
Your responses will help us determine what type of traveler you are!
""")

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

indicator_averages = {
    "DT1": 3.0506, "DT2": 4.0545, "DT3": 3.9728, "DT4": 2.7821,
    "HS1": 3.6304, "HS2": 3.7704, "HS3": 3.1012, "HS4": 3.1012,
    "SU1": 3.6265, "SU2": 3.3230, "SU3": 3.2957, "SU4": 3.3502,
    "RA1": 4.0195, "RA2": 3.8755, "RA3": 3.8171, "RA4": 3.6459, "RA5": 3.0636,
    "LX1": 2.8716, "LX2": 3.1090, "LX3": 2.5564, "LX4": 2.3696
}


# Remaining metadata
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

if 'classified' not in st.session_state:
    st.session_state.classified = False
    st.session_state.scores = {}
    st.session_state.responses = {}
    st.session_state.show_detail = False

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
    return hybrid[key] if key in hybrid else base[top1], [top1, top2] if key in hybrid else [top1]

scores = {k: 0.0 for k in constructs}
responses = {}
for code, question in questionnaire.items():
    response = st.slider(f"{code}: {question}", 1, 5, 3)
    responses[code] = response
    weight = indicator_weights[code]
    construct = indicator_to_construct[code]
    scores[construct] += response * weight

if st.button("Classify Me!"):
    traveler, relevant = classify(scores)
    st.session_state.classified = True
    st.session_state.scores = scores
    st.session_state.traveler = traveler
    st.session_state.relevant = relevant
    st.session_state.responses = responses

if st.session_state.classified:
    traveler_type, guidance = st.session_state.traveler
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
    for tag in st.session_state.relevant:
        if tag in suggestions:
            for route in suggestions[tag]:
                st.markdown(f"- {route}")

    if st.button("📊 Compare with Survey Average"):
        avg_scores = {'Digital': 4.22, 'Health': 4.05, 'Sustainability': 3.74, 'Rural': 3.88, 'Luxury': 3.40}
        x = np.arange(len(avg_scores))
        fig, ax = plt.subplots()
        ax.bar(x - 0.2, [st.session_state.scores[k] for k in avg_scores], width=0.4, label='You', color='green')
        ax.bar(x + 0.2, list(avg_scores.values()), width=0.4, label='Survey Avg', color='blue')
        ax.set_title('🔍 How Do Your Preferences Compare with Others?')
        ax.set_xticks(x)
        ax.set_xticklabels(avg_scores.keys())
        ax.set_ylabel('Average Rating')
        ax.legend()
        st.pyplot(fig)
        st.session_state.show_detail = True

    if st.session_state.show_detail and st.button("📋 Indicator-by-Indicator Insights"):
        for construct in constructs:
            indicators = [i for i in questionnaire if indicator_to_construct[i] == construct]
            x = np.arange(len(indicators))
            fig, ax = plt.subplots()
            user_vals = [st.session_state.responses[i] for i in indicators]
            avg_vals = [indicator_averages[i] for i in indicators]
            ax.barh(x - 0.2, user_vals, height=0.4, label='You', color='green')
            ax.barh(x + 0.2, avg_vals, height=0.4, label='Survey Avg', color='blue')
            ax.set_yticks(x)
            ax.set_yticklabels(indicators)
            ax.set_xlim(1, 5)
            ax.set_title(f"🔎 {construct} Preferences vs Average")
            ax.set_xlabel("Rating (1-5)")
            ax.legend()
            st.pyplot(fig)

    st.caption("App Created by Alireza Moradpour – Based on Master's Thesis Research in Future Rail Tourism.")
