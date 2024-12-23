import streamlit as st
from src.ui import StreamlitUI

def main():
    st.set_page_config(page_title="Advanced Code Analysis Assistant", layout="wide")
    
    ui = StreamlitUI()

    with st.sidebar:
        st.header("Configuration")
        model = st.selectbox("Select Ollama Model", ui.available_models, index=0)
        extensions = st.multiselect(
            "File Extensions to Process",
            ui.file_extensions,
            default=['.py', '.js']
        )
        
        source = ui.render_source_input()
        if source:
            ui.handle_source_input(source, model, extensions)
    
    tab1, tab2 = st.tabs([  # Define tabs for functionality
        "Query Documentation",
        "Generate Documentation",
    ])

    with tab1:
        st.header("Ask Questions About Your Code")
        query = st.text_area("Enter your question about the code:")
        if st.button("Get Answer") and ui.documentation:
            with st.spinner("Processing your question..."):
                st.markdown(ui.documentation.query_documentation(query))

    with tab2:
        st.header("Generate Project Documentation")
        if st.button("Generate Complete Documentation") and ui.documentation:
            with st.spinner("Generating documentation..."):
                doc = ui.documentation.query_documentation(
                    "Generate comprehensive documentation for this project, "
                    "including main components, functions, and architecture."
                )
                st.markdown(doc)
                st.download_button(
                    "Download Documentation",
                    doc,
                    "project_documentation.md",
                    "text/markdown"
                )


if __name__ == "__main__":
    main()
