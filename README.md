# batched-chatgpt
Extremely **easy-to-use ChatGPT** batched API caller.  
It only supports single turn conversation!

## Installation
```bash
pip install batched-chatgpt
```

## Quickstart
It requires ```OPENAI_API_KEY``` in your environment variable.
```bash
export OPENAI_API_KEY=<your_api_key>
```
Or in python code,  
```python
import os
os.environ['OPENAI_API_KEY'] = "<your_api_key>"
```
### Simple version
```python
from batched_chatgpt import call_chatgpt

resp = call_chatgpt(
    human_message=PROMPTS,  # list of str
)
```

## Features
- Autosaves the responses if pkl_path is specified. (auto-detect new filename and use pickle to save)
    - Autosaves per single API call
    - saves like ```['blabla', 'blablabla', None, None, None, ...]``` and ```None``` is a placeholder not responded by ChatGPT.
    - That means, no ```None``` will be returned if everything goes well.
- Auto retry with customizable timeout.
- Customizable chunk size, and auto multiprocessing.
- Reserving the order of input list.

### Need more customization?
```python
from batched_chatgpt import call_chatgpt

resp = call_chatgpt(
    human_message=PROMPTS,  # list of str
    system_message=['You are a helpful assistant.'] * len(prompts),
    model_name=CHATGPT_VERSION_NAME,  # default is 'gpt-3.5-turbo'
    temperature=TEMPERATURE,  # default 0.0
    chunk_size=CHATGPT_CHUNK_SIZE,
    timeout_each=TIMEOUT_EACH,
    sleep_between_chunk=SLEEP_BETWEEN_CHUNK,
    pkl_path=file_dir,  # ex) "result.pkl'
    verbose=True
)
```
- ```human_message```: list of human message
- ```system_message```: list of system prompt. It can be a str or a list of str that has same length to human_message
- ```model_name```: ChatGPT API name (ex: "gpt-4-1106-preview")
- ```temperature```: Controls randomness of the generated text
- ```chunk_size```: The number of examples which send in one batch
- ```timeout_each```: API call timeout
- ```sleep_between_chunk```: sleep time between batches
- ```pkl_path```: Specifies the path where output will be saved. By default, outputs are not saved.
- ```verbose```: If true, debugging message will be printed.

## Requirements
- langchain
- langchain-openai
- openai
