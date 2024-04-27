"""
The render_story_tab function generates the UI controls in the tab by invoking functions to render the text input fields, and other options.

The generate_prompt function generates the text prompt that is supplied to the Gemini API.
The prompt string is created by concatenating user entered values in the tab UI for the character of the story, and options
such as the story length (short, long), creativity level (low, high), and the story premise.

The function also returns a temperature value based on the selected creativity level of the story.
This value is supplied as the temperature configuration parameter to the model, which controls the randomness of the model's predictions.
The max_output_tokens configuration parameter specifies the maximum number of output tokens to generate per message.

To generate the model response, a button is created in the tab UI. When the button is clicked, the get_gemini_pro_text_response function is invoked,
which we will code in the next step in the lab.
"""

import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from response_utils import *
import logging

# create the model prompt based on user input.
def generate_prompt():
    # Story character input
    character_name = st.text_input("Enter character name: \n\n",key="character_name",value="Mittens")
    character_type = st.text_input("What type of character is it? \n\n",key="character_type",value="Cat")
    character_persona = st.text_input("What personality does the character have? \n\n",
                                      key="character_persona",value="Mitten is a very friendly cat.")
    character_location = st.text_input("Where does the character live? \n\n",key="character_location",value="Andromeda Galaxy")

    # Story length and premise
    length_of_story = st.radio("Select the length of the story: \n\n",["Short","Long"],key="length_of_story",horizontal=True)
    story_premise = st.multiselect("What is the story premise? (can select multiple) \n\n",["Love","Adventure","Mystery","Horror","Comedy","Sci-Fi","Fantasy","Thriller"],key="story_premise",default=["Love","Adventure"])
    creative_control = st.radio("Select the creativity level: \n\n",["Low","High"],key="creative_control",horizontal=True)
    if creative_control == "Low":
        temperature = 0.30
    else:
        temperature = 0.95

    prompt = f"""Write a {length_of_story} story based on the following premise: \n
    character_name: {character_name} \n
    character_type: {character_type} \n
    character_persona: {character_persona} \n
    character_location: {character_location} \n
    story_premise: {",".join(story_premise)} \n
    If the story is "short", then make sure to have 5 chapters or else if it is "long" then 10 chapters.
    Important point is that each chapter should be generated based on the premise given above.
    First start by giving the book introduction, chapter introductions and then each chapter. It should also have a proper ending.
    The book should have a prologue and an epilogue.
    """

    return temperature, prompt

# function to render the story tab, and call the model, and display the model prompt and response.
def render_story_tab (text_model_pro: GenerativeModel):
    st.write("Using Gemini 1.0 Pro - Text only model")
    st.subheader("Generate a story")

    temperature, prompt = generate_prompt()

    config = {
        "temperature": temperature,
        "max_output_tokens": 2048,
        }

    generate_t2t = st.button("Generate my story", key="generate_t2t")
    if generate_t2t and prompt:
        # st.write(prompt)
        with st.spinner("Generating your story using Gemini..."):
            first_tab1, first_tab2 = st.tabs(["Story response", "Prompt"])
            with first_tab1:
                response = get_gemini_pro_text_response(text_model_pro, prompt, generation_config=config)
                if response:
                    st.write("Your story:")
                    st.write(response)
                    logging.info(response)
            with first_tab2:
                st.text(prompt)
