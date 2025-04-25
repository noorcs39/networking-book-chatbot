import gradio as gr
from rag_pipeline import setup_vectorstore, create_rag_chain
import os
import gradio as gr
from rag_pipeline import setup_vectorstore, create_rag_chain

# Setup at first run
if not os.path.exists("db"):  # If no DB, create it
    setup_vectorstore()

rag_chain = create_rag_chain()

# Session state for multi-turn history
chat_history = []

def user_chat(user_message, chat_history_display):
    chat_history.append({"role": "user", "content": user_message})
    return gr.Textbox(value=""), chat_history_display

def bot_chat(user_message, chat_history_display):
    response = rag_chain.run(user_message)
    chat_history.append({"role": "assistant", "content": response})
    chat_display = []
    for turn in chat_history:
        if turn["role"] == "user":
            chat_display.append((turn["content"], None))
        else:
            chat_display.append((None, turn["content"]))
    return gr.Textbox(value=""), chat_display

with gr.Blocks() as demo:
    with gr.Tab("Chat with Networking Book @ Noor Uddin"):
        chatbot = gr.Chatbot()
        input_box = gr.Textbox(label="Ask anything about Computer Networking...")
        clear_button = gr.Button("Clear Chat")

        input_box.submit(user_chat, [input_box, chatbot], [input_box, chatbot], queue=False)
        input_box.submit(bot_chat, [input_box, chatbot], [input_box, chatbot])

        clear_button.click(lambda: ([], []), None, [input_box, chatbot], queue=False)

if __name__ == "__main__":
    demo.launch()
