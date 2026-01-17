import gradio as gr 
from pocket_tts import TTSModel 
import scipy.io.wavfile 

def generate_audio(text):
    try:
        # while generating audio, show spinner on UI
        progress = gr.Progress()
        progress(0.5, "Generating audio...")
        print('Generating audio for the text...')
        tts_model = TTSModel.load_model()
        progress(0.4, "Model loaded.")
        voice_state = tts_model.get_state_for_audio_prompt("hf://kyutai/tts-voices/alba-mackenna/casual.wav")
        progress(0.7, "Voice state prepared.")
        audio = tts_model.generate_audio(voice_state, text)
        progress(1.0, "Audio generation complete.")
        scipy.io.wavfile.write("output.wav", tts_model.sample_rate, audio.numpy())
        print("Audio generated and saved as output.wav")
    except Exception as e:
        print("Error generating audio:", e)

def UI():
    with gr.Blocks() as demo:
        gr.Markdown("# Blog Summarizer")
        url_input = gr.Textbox(label="Enter Blog URLs (comma separated)", placeholder="https://example.com")
        summarize_button = gr.Button("Summarize")
        output_area = gr.Textbox(label="Summary Output", lines=20)
        audio_button = gr.Button("Generate Audio")

        def summarize_blogs(urls):
            url_list = [url.strip() for url in urls.split(',')]
            # Call the main summarization function from main.py
            from main import summarize_content
            summary = summarize_content(url_list)
            return summary

        def generate_audio_from_summary(summary):
            print("Generating audio for the summary...", summary, end='')
            generate_audio(summary)

        summarize_button.click(fn=summarize_blogs, inputs=url_input, outputs=output_area)
        audio_button.click(fn=generate_audio_from_summary, inputs=output_area, outputs=None)

        # after generating audio, show audio on the UI 
        audio_output = gr.Audio(label="Generated Audio", streaming=True)
        audio_button.click(fn=lambda: "output.wav", inputs=None, outputs=audio_output)


    demo.launch()

UI()