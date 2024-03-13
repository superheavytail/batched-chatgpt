# batched-chatgpt
Extremely **easy-to-use ChatGPT** batched API caller.  
It only supports single turn conversation!

### Features
- Autosaves the responses. (auto-detect new filename and use pickle to save)
- Auto retry with customizable timeout.
- Customizable chunk size, and auto multiprocessing.
- Reserving the order of input list.

## Installation
```bash
pip install batched-chatgpt
```

## How to use
It requires ```OPENAI_API_KEY``` in your environment variable!
```bash
export OPENAI_API_KEY=<your_api_key>
```
### Simple version
```python
from batched_chatgpt import call_chatgpt

resp = call_chatgpt(
    human_message=PROMPTS,  # list of str
    pkl_path=FILE_DIR,  # ex) "result.pkl'
)
```

### Need more customization?
```python
from batched_chatgpt import call_chatgpt

resp = call_chatgpt(
    model_name=CHATGPT_VERSION_NAME,  # default is 'gpt-3.5-turbo'
    chunk_size=CHATGPT_CHUNK_SIZE,
    timeout_each=TIMEOUT_EACH,
    sleep_between_chunk=SLEEP_BETWEEN_CHUNK,
    human_message=PROMPTS,  # list of str
    system_message=['You are a helpful assistant.'] * len(prompts),
    pkl_path=file_dir,
    verbose=True
)
```

## Requirements
- langchain
- langchain-openai
- openai
