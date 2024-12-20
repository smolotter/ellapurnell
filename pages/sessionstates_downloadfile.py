import streamlit as st
import json

# Define options for multiselect widgets
fruits = ['apple', 'banana', 'carrot']
animals = ['dog', 'cow', 'cat']
drinks = ['water', 'juice', 'soup']

# Initialize session state with default values
if 'selected_values' not in st.session_state:
    st.session_state.selected_values = {
        'fruits': [],
        'animals': [],
        'drinks': []
    }

if 'fruits_select' not in st.session_state:
    st.session_state.fruits_select = st.session_state.selected_values['fruits']
if 'animals_select' not in st.session_state:
    st.session_state.animals_select = st.session_state.selected_values['animals']
if 'drinks_select' not in st.session_state:
    st.session_state.drinks_select = st.session_state.selected_values['drinks']

# Function to load session state from JSON file
def load_session_state_from_json():
    uploaded_file = st.file_uploader("Upload Session State (JSON)", type="json")
    if uploaded_file is not None:
        try:
            contents = uploaded_file.read()
            loaded_state = json.loads(contents)
            # Check if required keys are in the uploaded JSON
            if all(key in loaded_state for key in ['fruits', 'animals', 'drinks']):
                # Update session state BEFORE creating widgets
                st.session_state.selected_values = loaded_state
                st.session_state.fruits_select = loaded_state['fruits']
                st.session_state.animals_select = loaded_state['animals']
                st.session_state.drinks_select = loaded_state['drinks']
                st.success("Session state loaded successfully!")
            else:
                st.error("Invalid JSON structure. Required keys: 'fruits', 'animals', 'drinks'.")
        except json.JSONDecodeError:
            st.error("Invalid JSON file.")

# Call function to load session state from JSON
load_session_state_from_json()

# Create multiselect widgets with on_change functions
def update_fruits():
    st.session_state.selected_values['fruits'] = st.session_state.fruits_select

def update_animals():
    st.session_state.selected_values['animals'] = st.session_state.animals_select

def update_drinks():
    st.session_state.selected_values['drinks'] = st.session_state.drinks_select

# Widgets are created after session state update
selected_fruits = st.multiselect('Select Fruits', fruits, key="fruits_select", on_change=update_fruits)
selected_animals = st.multiselect('Select Animals', animals, key="animals_select", on_change=update_animals)
selected_drinks = st.multiselect('Select Drinks', drinks, key="drinks_select", on_change=update_drinks)

# Download session state (JSON)
def download_json():
    serialized_state = json.dumps(st.session_state.selected_values, indent=4)
    st.download_button(
        label="Download Session State (JSON)",
        data=serialized_state,
        file_name="session_state.json",
        mime="application/json"
    )

download_json()

# Display JSON content
st.write("Current Session State (JSON):")
st.code(json.dumps(st.session_state.selected_values, indent=4))

# Display selected values
st.write(f"Selected Fruits: {st.session_state.selected_values['fruits']}")
st.write(f"Selected Animals: {st.session_state.selected_values['animals']}")
st.write(f"Selected Drinks: {st.session_state.selected_values['drinks']}")
