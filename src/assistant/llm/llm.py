from assistant.llm.prompts import TERMINAL_ASSISTANT_PROMPT, TIMESHEETS_PROMPT
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI
import ollama

# get langchain_openai version


def terminal_assistant(input_text: str, model: str) -> str:
    # model = "codeqwen"
    # model = "mistral:7b-instruct"
    # model = "qwen2.5-coder:7b-instruct"
    installed_models = ollama.list().models
    model_names = [model["model"].replace(":latest", "") for model in installed_models]
    if model not in model_names:
        print(f"Model {model} not found. Available models:")
        for installed_model in model_names:
            print(f"  {installed_model}")
        print(f"Pull the model with `ollama pull {model}`")
        # ollama.pull(model)
        return ""

    model = OllamaLLM(model=model)
    # model = OpenAI()
    chain = TERMINAL_ASSISTANT_PROMPT | model
    return chain.invoke(input_text)


def time_sheets_assistant(history: str) -> str:
    model = ChatOpenAI()
    chain = TIMESHEETS_PROMPT | model
    response = chain.invoke(history)
    return response.content
