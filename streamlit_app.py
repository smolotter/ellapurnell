import streamlit as st
  
def main():
    st.title("Dynamic File Uploader")

    # Create a dropdown menu with options from 1 to 50
    st.markdown("**How many zip files do you have?**")
    with st.expander("Click here to see examples")    
        st.write("The minimum is 2: One product body + One distribution list.")
        st.write("If there is an annex then 3: One product body + One annex + One distribution list.")
        st.write("If there is a covernote but no annex, also 3: One covernote + One product body + One distribution list.")
        st.write("If there is a covernote and an annex, then 4: One covernote + One product body + One annex + One distribution list.")
        st.write("If this is a ES package, you may need more. For example, One packaging note + One EN + One distribution + Five Pensketches + Five distribution lists = 13.")

    num_files = st.selectbox("Select Number of Files", range(2, 101))

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