import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="CV Analyzer AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HARDCODED API KEY (untuk demo)
# ============================================================================
GEMINI_API_KEY = "ubah disini"  

# ============================================================================
# CUSTOM CSS - GREY MINIMALIST THEME
# ============================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1a1a1a;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 15px;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px dashed #cbd5e0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #4a5568;
    }
    
    /* Cards/Containers */
    .css-1r6slb0 {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: #2d3748;
    }
    
    /* Code blocks */
    code {
        font-family: 'JetBrains Mono', monospace;
        background: #f7fafc;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        color: #2d3748;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: #cbd5e0;
    }
    
    .stSlider > div > div > div > div {
        background: #2d3748;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .stError {
        background: #fff5f5;
        border-left: 4px solid #f56565;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        if not text.strip():
            return None, "PDF tidak mengandung text yang bisa dibaca"
        
        return text, None
    except Exception as e:
        return None, f"Error saat membaca PDF: {str(e)}"


def analyze_cv_with_gemini(cv_text, temperature, top_p):
    """Analyze CV using Google Gemini API"""
    try:
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "max_output_tokens": 2048,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config
        )
        
        
        prompt = f"""Analyze this CV/Resume for an AI Engineer position. Provide a detailed, structured analysis.

CV Content:
{cv_text}

Please provide your analysis in the following format:

##  STRENGTHS
List 3-5 key strengths of this CV. Be specific and mention concrete examples from the CV.

##  WEAKNESSES  
List 3-5 areas that need improvement. Be constructive and specific.

##  IMPROVEMENT SUGGESTIONS
Provide 5-7 actionable suggestions to improve this CV. Number each suggestion.

##  OVERALL ASSESSMENT
- **Technical Skills Score**: X/10
- **Experience Relevance Score**: X/10  
- **Presentation Quality Score**: X/10
- **Overall Score**: X/10

Provide a brief justification for the overall score.

## 🎓 FINAL RECOMMENDATION
Provide a 2-3 sentence summary of whether this candidate is suitable for an AI Engineer role and what the main focus areas for improvement should be.
"""
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text, None
        else:
            return None, "Tidak ada response dari Gemini API"
            
    except Exception as e:
        return None, f"Error saat analisis: {str(e)}"


def format_analysis_for_download(analysis_text, filename):
    """Format analysis text for download"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    download_content = f"""
================================================================================
CV ANALYSIS REPORT
================================================================================
Generated: {timestamp}
File: {filename}
Analyzer: Gemini Pro AI
================================================================================

{analysis_text}

================================================================================
Report generated by CV Analyzer AI
================================================================================
"""
    return download_content

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>📄 CV Analyzer AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096; font-size: 1.1rem; margin-top: 0.5rem;'>Powered by Google Gemini • AI-driven Resume Analysis</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar - AI Parameters
    with st.sidebar:
        st.markdown("### ⚙️ AI Settings")
        st.markdown("Adjust these parameters to control the AI's creativity and randomness.")
        
        st.markdown("---")
        
        # Temperature slider
        st.markdown("**🌡️ Temperature**")
        st.caption("Controls randomness: 0 = focused, 2 = creative")
        temperature = st.slider(
            "temperature_slider",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            label_visibility="collapsed"
        )
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem; font-weight: 600;'>{temperature}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top P slider  
        st.markdown("**🎯 Top P**")
        st.caption("Nucleus sampling: 0 = deterministic, 1 = diverse")
        top_p = st.slider(
            "top_p_slider",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.05,
            label_visibility="collapsed"
        )
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem; font-weight: 600;'>{top_p}</p>", unsafe_allow_html=True)
        
        
    
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload CV/Resume")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Maximum file size: 5MB"
        )
        
        if uploaded_file is not None:
            # Show file info
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            
            st.success(f" File uploaded: **{uploaded_file.name}**")
            st.info(f" Size: {file_size_mb:.2f} MB")
            
            # Validate file size
            if file_size_mb > 5:
                st.error(" File too large! Maximum size is 5MB.")
                return
            
            # Extract text
            with st.spinner(" Extracting text from PDF..."):
                cv_text, error = extract_text_from_pdf(uploaded_file)
            
            if error:
                st.error(f" {error}")
                return
            
            if cv_text:
                # Show preview
                with st.expander(" Preview Extracted Text"):
                    preview_text = cv_text[:500] + "..." if len(cv_text) > 500 else cv_text
                    st.code(preview_text, language="text")
                    st.caption(f"Total characters: {len(cv_text)}")
                
                st.markdown("---")
                
                # Analyze button
                if st.button(" Analyze CV", use_container_width=True):
                    with st.spinner(" AI is analyzing your CV... This may take 10-30 seconds."):
                        analysis, error = analyze_cv_with_gemini(cv_text, temperature, top_p)
                    
                    if error:
                        st.error(f" {error}")
                    else:
                        # Store in session state
                        st.session_state['analysis'] = analysis
                        st.session_state['filename'] = uploaded_file.name
                        st.success(" Analysis complete!")
                        st.rerun()
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        if 'analysis' in st.session_state and st.session_state['analysis']:
            # Display analysis
            st.markdown(st.session_state['analysis'])
            
            st.markdown("---")
            
            # Download button
            download_content = format_analysis_for_download(
                st.session_state['analysis'],
                st.session_state.get('filename', 'unknown.pdf')
            )
            
            st.download_button(
                label="📥 Download Report",
                data=download_content,
                file_name=f"CV_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Clear button
            if st.button("🔄 Clear Results", use_container_width=True):
                del st.session_state['analysis']
                del st.session_state['filename']
                st.rerun()
        else:
            st.info(" Upload a CV and click 'Analyze' to see results here.")
            
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #718096; padding: 1rem;'>
        <p>Built using Streamlit & Google Gemini AI</p>
        <p style='font-size: 0.9rem;'>For best results, ensure your CV is well-formatted and contains clear sections for education, experience, and skills.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()
