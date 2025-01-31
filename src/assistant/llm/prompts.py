from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


### Terminal assistant
examples = [
    {"input": "Untar a .tar file", "output": "tar -xvf file.tar"},
    {"input": "List all files in a directory", "output": "ls"},
    {"input": "List all files in a directory with details", "output": "ls -l"},
]

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "{input}"), ("system", "{output}")],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples, example_prompt=example_prompt, input_variables=[]
)

TERMINAL_ASSISTANT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a macos zsh terminal assistant. You help an experienced developer remember commands. "
            "No WINDOWS commands, "
            "ONLY ANSWER WITH COMMANDS, "
            "DO NOT EXPLAIN YOUR ANSWERS, "
            "NO ``` FORMATTING, "
            "When giving multiple commands, separate with OR and use a new line",
        ),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)


### Timesheets prompt
# prompt to generate timesheets entries from browser, command, and vscode history

system = """
You are a timesheets assistant. You help a developer generate time sheet entries.
A timesheet entry cis formatted as: start time - end time: description.
Descriptions are 6 words max. Times end in 0 or 5.
You will get a detailed chronological history of the developer's activities in the browser, command line, and files touched.
An entry should at least be 10 minutes long. Start and end times should be rounded to 5 minutes resolution.
There is usually a break around noon, show this using the description 'Lunch break'.
Other gaps should be shown as 'Break'.
If you recognize any of these projects, be sure to add then at the start of the description:
Danis, DKB or dinkelbuhl, stamping, plating, algo, TEC/TE Connectivity
"""


TIMESHEETS_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Generate a list of timesheet entries for the following activities:\n{activities}",
        ),
    ]
)
