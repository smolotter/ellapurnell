



import streamlit as st
import json

# Initialize session state
if 'selected_values' not in st.session_state:
    st.session_state.selected_values = {
        'fruits': [],
        'animals': [],
        'drinks': []
    }

# Define options for multiselect widgets
fruits = ['apple', 'banana', 'carrot']
animals = ['dog', 'cow', 'cat']
drinks = ['water', 'juice', 'soup']

# Create multiselect widgets with on_change functions
def update_fruits(selected):
    st.session_state.selected_values['fruits'] = selected

def update_animals(selected):
    st.session_state.selected_values['animals'] = selected

def update_drinks(selected):
    st.session_state.selected_values['drinks'] = selected

selected_fruits = st.multiselect('Select Fruits', fruits, on_change=update_fruits)
selected_animals = st.multiselect('Select Animals', animals, on_change=update_animals)
selected_drinks = st.multiselect('Select Drinks', drinks, on_change=update_drinks)

# Download session state (JSON)
def download_json():
    serialized_state = json.dumps(st.session_state.selected_values, indent=4)  # Indent for better readability
    st.download_button(
        label="Download Session State (JSON)",
        data=serialized_state,
        file_name="session_state.json",
        mime="application/json"
    )

# Display JSON content
st.write("Current Session State (JSON):")
st.code(json.dumps(st.session_state.selected_values, indent=4))

# Display selected values
st.write(f"Selected Fruits: {st.session_state.selected_values['fruits']}")
st.write(f"Selected Animals: {st.session_state.selected_values['animals']}")
st.write(f"Selected Drinks: {st.session_state.selected_values['drinks']}")


