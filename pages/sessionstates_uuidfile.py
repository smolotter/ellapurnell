import streamlit as st
import json
import uuid
import os

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

# Create a directory to store JSON files
storage_dir = "session_states"
os.makedirs(storage_dir, exist_ok=True)

st.write("contents of dir:")
st.write(os.listdir(storage_dir))


# Function to save session state to a JSON file
def save_session_state_to_file():
    file_uuid = str(uuid.uuid4())  # Generate a unique identifier
    file_path = os.path.join(storage_dir, f"{file_uuid}.json")
    serialized_state = json.dumps(st.session_state.selected_values, indent=4)
    with open(file_path, "w") as f:
        f.write(serialized_state)
    st.write(f"Session state saved with UUID: **{file_uuid}**")
    st.success("Session state saved successfully!")

# Function to load session state from a file based on UUID
def load_session_state_from_uuid():
    user_uuid = st.text_input("Enter UUID to load session state:", key="uuid_input")
    if st.button("Load Session State"):
        file_path = os.path.join(storage_dir, f"{user_uuid}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                loaded_state = json.load(f)
            # Validate and update session state
            if all(key in loaded_state for key in ['fruits', 'animals', 'drinks']):
                st.session_state.selected_values = loaded_state
                st.session_state.fruits_select = loaded_state['fruits']
                st.session_state.animals_select = loaded_state['animals']
                st.session_state.drinks_select = loaded_state['drinks']
                st.success("Session state loaded successfully!")
            else:
                st.error("Invalid JSON structure in the file.")
        else:
            st.error("No file found for the given UUID.")

# Function to update session state from widget changes
def update_fruits():
    st.session_state.selected_values['fruits'] = st.session_state.fruits_select

def update_animals():
    st.session_state.selected_values['animals'] = st.session_state.animals_select

def update_drinks():
    st.session_state.selected_values['drinks'] = st.session_state.drinks_select

# Create multiselect widgets with on_change functions
selected_fruits = st.multiselect('Select Fruits', fruits, key="fruits_select", on_change=update_fruits)
selected_animals = st.multiselect('Select Animals', animals, key="animals_select", on_change=update_animals)
selected_drinks = st.multiselect('Select Drinks', drinks, key="drinks_select", on_change=update_drinks)

# Button to save the current session state
if st.button("Save Session State"):
    save_session_state_to_file()

# Text field and button to load a session state by UUID
load_session_state_from_uuid()

# Display JSON content
st.write("Current Session State (JSON):")
st.code(json.dumps(st.session_state.selected_values, indent=4))

# Display selected values
st.write(f"Selected Fruits: {st.session_state.selected_values['fruits']}")
st.write(f"Selected Animals: {st.session_state.selected_values['animals']}")
st.write(f"Selected Drinks: {st.session_state.selected_values['drinks']}")
