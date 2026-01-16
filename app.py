import gradio as gr 

def UI():
    with gr.Blocks() as demo:
        gr.Markdown("# Blog Summarizer")
        url_input = gr.Textbox(label="Enter Blog URLs (comma separated)", placeholder="https://example.com/blog1, https://example.com/blog2")
        summarize_button = gr.Button("Summarize")
        output_area = gr.Textbox(label="Summary Output")

        def summarize_blogs(urls):
            url_list = [url.strip() for url in urls.split(',')]
            # Call the main summarization function from main.py
            from main import summarize_content
            summary = summarize_content(url_list)
            return summary

        summarize_button.click(fn=summarize_blogs, inputs=url_input, outputs=output_area)

    demo.launch()

UI()