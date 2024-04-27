"""
The render_image_playground_tab function builds the UI that enables the app user to interact with the Gemini 1.0 Pro Vision
model. It creates a set of tabs: "Furniture recommendation", "Oven instructions", "ER diagrams", "Math reasoning" in the UI.
You write the code for the remaining tabs in subsequent tasks in this lab.

In the Furniture recommendation tab, a living room scene is used to perform visual understanding.
Along with a set of additional images of chairs, the code invokes the Gemini 1.0 Pro Vision multimodal API endpoint to get a
recommendation of a chair that complements the living room scene.

The code uses more than one text prompt and the images of the living room and chairs, and provides that in a list to the model.
The Part class is used to obtain the image from the multi-part content URI that is hosted in a Cloud Storage bucket.
The prompt also specifies a tabular format for the model output, and to include the rationale for the recommendation.
"""
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel, Part
from response_utils import *
import logging

# render the Image Playground tab with multiple child tabs
def render_image_playground_tab(multimodal_model_pro: GenerativeModel):

    st.write("Using Gemini 1.0 Pro Vision - Multimodal model")
    recommendations, screens, diagrams, equations = st.tabs(["Furniture recommendation", "Oven instructions", "ER diagrams", "Math reasoning"])

    with recommendations:
        room_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/living_room.jpeg"
        chair_1_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair1.jpeg"
        chair_2_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair2.jpeg"
        chair_3_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair3.jpeg"
        chair_4_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair4.jpeg"

        room_image_url = "https://storage.googleapis.com/"+room_image_uri.split("gs://")[1]
        chair_1_image_url = "https://storage.googleapis.com/"+chair_1_image_uri.split("gs://")[1]
        chair_2_image_url = "https://storage.googleapis.com/"+chair_2_image_uri.split("gs://")[1]
        chair_3_image_url = "https://storage.googleapis.com/"+chair_3_image_uri.split("gs://")[1]
        chair_4_image_url = "https://storage.googleapis.com/"+chair_4_image_uri.split("gs://")[1]

        room_image = Part.from_uri(room_image_uri, mime_type="image/jpeg")
        chair_1_image = Part.from_uri(chair_1_image_uri,mime_type="image/jpeg")
        chair_2_image = Part.from_uri(chair_2_image_uri,mime_type="image/jpeg")
        chair_3_image = Part.from_uri(chair_3_image_uri,mime_type="image/jpeg")
        chair_4_image = Part.from_uri(chair_4_image_uri,mime_type="image/jpeg")

        st.image(room_image_url,width=350, caption="Image of a living room")
        st.image([chair_1_image_url,chair_2_image_url,chair_3_image_url,chair_4_image_url],width=200, caption=["Chair 1","Chair 2","Chair 3","Chair 4"])

        st.write("Our expectation: Recommend a chair that would complement the given image of a living room.")
        prompt_list = ["Consider the following chairs:",
                    "chair 1:", chair_1_image,
                    "chair 2:", chair_2_image,
                    "chair 3:", chair_3_image, "and",
                    "chair 4:", chair_4_image, "\n"
                    "For each chair, explain why it would be suitable or not suitable for the following room:",
                    room_image,
                    "Only recommend for the room provided and not other rooms. Provide your recommendation in a table format with chair name and reason as columns.",
            ]

        tab1, tab2 = st.tabs(["Response", "Prompt"])
        generate_image_description = st.button("Generate recommendation", key="generate_image_description")
        with tab1:
            if generate_image_description and prompt_list:
                with st.spinner("Generating recommendation using Gemini..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro, prompt_list)
                    st.markdown(response)
                    logging.info(response)
        with tab2:
            st.write("Prompt used:")
            st.text(prompt_list)

    """
    Equipped with the ability to extract information from visual elements on screens, Gemini can analyze screenshots,
    icons, and layouts to provide a holistic understanding of the depicted scene.

    In this task, you provide an image of a kitchen oven's control panel to the model, and then prompt the model to
    generate instructions for a specific function.
    """
    with screens:
        oven_screen_uri = "gs://cloud-training/OCBL447/gemini-app/images/oven.jpg"
        oven_screen_url = "https://storage.googleapis.com/"+oven_screen_uri.split("gs://")[1]

        oven_screen_img = Part.from_uri(oven_screen_uri, mime_type="image/jpeg")
        st.image(oven_screen_url, width=350, caption="Image of an oven control panel")
        st.write("Provide instructions for resetting the clock on this appliance in English")

        prompt = """How can I reset the clock on this appliance? Provide the instructions in English.
                If instructions include buttons, also explain where those buttons are physically located.
                """

        tab1, tab2 = st.tabs(["Response", "Prompt"])
        generate_instructions_description = st.button("Generate instructions", key="generate_instructions_description")
        with tab1:
            if generate_instructions_description and prompt:
                with st.spinner("Generating instructions using Gemini..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro, [oven_screen_img, prompt])
                    st.markdown(response)
                    logging.info(response)
        with tab2:
            st.write("Prompt used:")
            st.text(prompt+"\n"+"input_image")


    """
    Gemini's multimodal capabilities enable it to comprehend diagrams and take actionable steps, such as d
    ocument or code generation. In this task, you use the Gemini 1.0 Pro Vision model to analyze an Entity-Relationship (ER)
    diagram and generate documentation on the entities and relationships found in the diagram.
    """
    with diagrams:
        er_diag_uri = "gs://cloud-training/OCBL447/gemini-app/images/er.png"
        er_diag_url = "https://storage.googleapis.com/"+er_diag_uri.split("gs://")[1]

        er_diag_img = Part.from_uri(er_diag_uri,mime_type="image/png")
        st.image(er_diag_url, width=350, caption="Image of an ER diagram")
        st.write("Document the entities and relationships in this ER diagram.")

        prompt = """Document the entities and relationships in this ER diagram."""

        tab1, tab2 = st.tabs(["Response", "Prompt"])
        er_diag_img_description = st.button("Generate documentation", key="er_diag_img_description")
        with tab1:
            if er_diag_img_description and prompt:
                with st.spinner("Generating..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro,[er_diag_img,prompt])
                    st.markdown(response)
                    logging.info(response)
        with tab2:
            st.write("Prompt used:")
            st.text(prompt+"\n"+"input_image")


    """
    Gemini 1.0 Pro Vision can also recognize math formulas and equations and extract specific information from them.
    This capability is particularly useful for generating explanations for math problems.
    """
    with equations:
        math_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/math_eqn.jpg"
        math_image_url = "https://storage.googleapis.com/"+math_image_uri.split("gs://")[1]

        math_image_img = Part.from_uri(math_image_uri,mime_type="image/jpeg")
        st.image(math_image_url,width=350, caption="Image of a math equation")
        st.markdown(f"""
                Ask questions about the math equation as follows:
                - Extract the formula.
                - What is the symbol right before Pi? What does it mean?
                - Is this a famous formula? Does it have a name?
                    """)

        prompt = """Follow the instructions. Surround math expressions with $. Use a table with a row for each instruction and its result.
                INSTRUCTIONS:
                - Extract the formula.
                - What is the symbol right before Pi? What does it mean?
                - Is this a famous formula? Does it have a name?
                """

        tab1, tab2 = st.tabs(["Response", "Prompt"])
        math_image_description = st.button("Generate answers", key="math_image_description")
        with tab1:
            if math_image_description and prompt:
                with st.spinner("Generating answers for formula using Gemini..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro, [math_image_img, prompt])
                    st.markdown(response)
                    logging.info(response)
        with tab2:
            st.write("Prompt used:")
            st.text(prompt)
