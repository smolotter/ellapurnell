import streamlit as st
 
def main():
    st.title("Dynamic File Uploader")

    # Create a dropdown menu with options from 1 to 50
    num_files = st.selectbox("Select Number of Files", range(1, 101))

    # Create a list to store the uploaded files
    uploaded_files = []

    # Create the appropriate number of file upload boxes
    for i in range(num_files):
        uploaded_file = st.file_uploader(f"Upload File {i+1}")
        uploaded_files.append(uploaded_file)

    # Process the uploaded files (optional)
    if uploaded_files:
        st.write("Uploaded Files:")
        for i, file in enumerate(uploaded_files):
            if file is not None:
                st.write(f"File {i+1}: {file.name}")
                # You can process the file content here, e.g., read it, analyze it, etc.
                # For example:
                # file_content = file.read()
                # st.write(file_content)

if __name__ == "__main__":
    main()