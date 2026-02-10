from src.config.settings import MODEL_NAME, MODEL_ID, MODEL_TEMPERATURE, MODEL_OPTIONS
from src.utils import update_chatbot

import gradio as gr

# Gradio Interface using Chatbot and conditional web search
with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="sky")) as app:
    gr.Markdown(f"# {MODEL_NAME}")
    with gr.Row():
        chatbot = gr.Chatbot(label="Chatbot Responses")
    with gr.Row():
        question_input = gr.Textbox(lines=2, label="Ask a Question")
        web_search_checkbox = gr.Checkbox(label="Enhance with Web Search", value=False)
    with gr.Row():
        model_input = gr.Dropdown(label="Model", value=MODEL_ID, choices=MODEL_OPTIONS)
        temperature_slider = gr.Slider(
            minimum=0.0,
            maximum=2.0,
            value=MODEL_TEMPERATURE,
            step=0.1,
            label="Temperature",
        )
        stream_checkbox = gr.Checkbox(label="Stream response", value=True)
    with gr.Row():
        submit_button = gr.Button("Submit")

    submit_button.click(
        fn=update_chatbot,
        inputs=[
            question_input,
            web_search_checkbox,
            chatbot,
            model_input,
            temperature_slider,
            stream_checkbox,
        ],
        outputs=[chatbot],
    )

if __name__ == "__main__":
    app.launch(share=True)
