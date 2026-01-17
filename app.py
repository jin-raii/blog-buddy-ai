import gradio as gr 
from pocket_tts import TTSModel 
import scipy.io.wavfile 

def generate_audio(text):
    tts_model = TTSModel.load_model()
    voice_state = tts_model.get_state_for_audio_prompt("hf://kyutai/tts-voices/alba-mackenna/casual.wav")

    audio = tts_model.generate_audio(voice_state, "hello world, how are you?")
    scipy.io.wavfile.write("output.wav", tts_model.sample_rate, audio.numpy())


def UI():
    with gr.Blocks() as demo:
        gr.Markdown("# Blog Summarizer")
        url_input = gr.Textbox(label="Enter Blog URLs (comma separated)", placeholder="https://example.com/blog1, https://example.com/blog2")
        summarize_button = gr.Button("Summarize")
        output_area = gr.Textbox(label="Summary Output", lines=20)

        def summarize_blogs(urls):
            url_list = [url.strip() for url in urls.split(',')]
            # Call the main summarization function from main.py
            from main import summarize_content
            summary = summarize_content(url_list)
            return summary

        summarize_button.click(fn=summarize_blogs, inputs=url_input, outputs=output_area)

    demo.launch()

UI()