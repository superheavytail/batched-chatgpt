from typing import List, Union
from pprint import pprint
from multiprocessing import Queue, Process
from pathlib import Path
import time
import os

from tqdm import tqdm
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

from .utils import pickle_bobj, get_saving_filename_safely


def process_chunk_element(i, queue, item, model_name):
    chat = ChatOpenAI(model=model_name, temperature=0)
    res = chat.invoke(item)
    queue.put((i, res))


def process_chunk(chunk, model_name, timeout=13):
    processes = []
    output_queue = Queue()
    results = [None] * len(chunk)  # Pre-allocate list for results

    for i, item in enumerate(chunk):
        p = Process(target=process_chunk_element, args=(i, output_queue, item, model_name))
        processes.append(p)
        p.start()
        time.sleep(0.2)  # restrict too dense api calling

    start_time = time.time()
    completed = 0

    while completed < len(processes) and time.time() - start_time < timeout:
        if not output_queue.empty():
            index, result = output_queue.get()
            results[index] = result
            completed += 1

    # Terminate any remaining processes
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join()

    return results


def batched_multiprocess_auto_retry(items, model_name, chunk_size, timeout_each, sleep_between_chunk, pkl_path, verbose=False):
    """returns list of chatgpt output string

    timeout-ed output be None"""
    pkl_path = get_saving_filename_safely(pkl_path) if pkl_path else None  # if pkl_path, result saved.

    outputs = [None] * len(items)
    while not all(outputs):
        # printing remained queries if the number of remained queries is small
        num_of_remains = outputs.count(None)
        print(f"num of remains: {num_of_remains}") if verbose else ...
        if verbose and num_of_remains <= chunk_size:
            pprint(f"printing remains...:\n{[items[i][1].content for i, o in enumerate(outputs) if o is None]}")

        remain_inputs = [(i, item) for i, item in enumerate(items) if outputs[i] is None]  # store failed item indices
        remain_indices, remain_items = list(zip(*remain_inputs))
        chunks = [remain_items[i:i + chunk_size] for i in range(0, len(remain_items), chunk_size)]  # re-chunk remains

        for i, chunk in enumerate(tqdm(chunks, "Batches")):  # tqdm num is the num of chunks
            results = process_chunk(chunk, model_name, timeout_each)
            results = list(map(lambda x: x.content if x else None, results))
            for j, result in enumerate(results):
                outputs[remain_indices[i * chunk_size + j]] = result

            # save the outputs which may be incomplete
            pickle_bobj(outputs, pkl_path) if pkl_path else None

            time.sleep(sleep_between_chunk) if not all(outputs) else ...
    return outputs


def call_chatgpt(
        human_message: List[str],
        system_message: Union[str, List[str]] = "You're a helpful assistant",
        model_name: str = "gpt-3.5-turbo",
        chunk_size: int = 20,
        timeout_each: int = 60,
        sleep_between_chunk: int = 10,
        pkl_path: Union[Path, str] = None,
        verbose: bool = False) -> List[str]:
    """call batched chatgpt api, and automatically save the responses.

    if pkl_path is not None, then this function automatically save the results to pkl_path.
    :param human_message: list of human message
    :param system_message: list of system prompt. It can be a str or a list of str that has same length to human_message
    :param model_name: ChatGPT API name ("gpt-4-1106-preview")
    :param chunk_size: The number of examples which send in one batch
    :param timeout_each: API call timeout
    :param sleep_between_chunk: sleep time between batches
    :param pkl_path: Chatgpt output will be saved to this path
    :param verbose: If true, the debugging message will be printed.

    :return: list of the answers from chatgpt
    """
    assert isinstance(system_message, list) or isinstance(system_message, str)
    assert isinstance(human_message, list)
    if isinstance(system_message, str):
        system_message = [system_message] * len(human_message)
    assert len(system_message) == len(human_message)
    assert os.environ['OPENAI_API_KEY']

    messages_list = [[
        SystemMessage(content=system_message[i]),
        HumanMessage(
            content=human_message[i]
        )
    ] for i in range(len(system_message))]

    resp = batched_multiprocess_auto_retry(
        messages_list, model_name, chunk_size, timeout_each, sleep_between_chunk, pkl_path, verbose)
    return resp