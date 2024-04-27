"""
The app uses streamlit to create a number of tabs in the UI. In this initial version of the app, we build the first tab Story that contains functionality to generate a story, and then incrementally build the other tabs in subsequent tasks in the lab.

The app first initializes the Vertex AI SDK passing in the values of the PROJECT_ID, and REGION environment variables.

It then loads the gemini-pro, and gemini-pro-vision models using the GenerativeModel class that represents a Gemini model. This class includes methods to help generate content from text, images, and video.

The app creates 4 tabs in the UI named Story, Marketing Campaign, Image Playground, and Video Playground.

The app code then invokes the render_tab1() function to create the UI for the Story tab in the app's UI.
"""

import os
import streamlit as st
from app_tab1 import render_story_tab
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging
from google.cloud import logging as cloud_logging

# configure logging
logging.basicConfig(level=logging.INFO)
# attach a Cloud Logging handler to the root logger
log_client = cloud_logging.Client()
log_client.setup_logging()

PROJECT_ID = os.environ.get('PROJECT_ID')   # Your Qwiklabs Google Cloud Project ID
LOCATION = os.environ.get('REGION')         # Your Qwiklabs Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)

@st.cache_resource
def load_models():
    text_model_pro = GenerativeModel("gemini-pro")
    multimodal_model_pro = GenerativeModel("gemini-pro-vision")
    return text_model_pro, multimodal_model_pro

st.header("Vertex AI Gemini API", divider="rainbow")
text_model_pro, multimodal_model_pro = load_models()

tab1, tab2, tab3, tab4 = st.tabs(["Story", "Marketing Campaign", "Image Playground", "Video Playground"])

with tab1:
    render_story_tab(text_model_pro)


from app_tab2 import render_mktg_campaign_tab

with tab2:
    render_mktg_campaign_tab(text_model_pro)

from app_tab3 import render_image_playground_tab

with tab3:
    render_image_playground_tab(multimodal_model_pro)

from app_tab4 import render_video_playground_tab

with tab4:
    render_video_playground_tab(multimodal_model_pro)
