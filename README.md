# LLMs

**Help desk** allows you to create a Question Answering bot with a streamlit UI using your company Confluence data.

<p align="center">
  <img src="./docs/help_desk.gif" alt="animated" />
</p>

# How to use

- Make sure you have installed `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Create a virtual environnement:
    - `uv lock && uv sync`
    - `source .venv/bin/activate`

- Copy the `env.template` file and fill in the environment variables
     - `cp .env.template .env`

- Create your Confluence API key [here]('https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/')

- To run the streamlit app run:
```
cd src
streamlit run streamlit.py
```

- To evaluate the quality of the RAG model:
```
# First replace the evaluation dataset file in the data folder with your topic questions
cd src
python evaluate.py
```

- To use and deep dive with the notebook
```
ipython kernel install --name RAG --user  # Add the notebook kernel
jupyter lab
```

## How it works ?
    .
    ├── data/
        ├── evaluation_dataset.tsv  # Questions and answers useful for evaluation

    ├── docs/                       # Documentation files
    ├── src/                        # The main directory for computer demo
        ├── __init__.py
        ├── load_db.py              # Load data from confluence and creates smart chunks
        ├── help_desk.py            # Instantiates the LLMs, retriever and chain
        ├── main.py                 # Run the Chatbot for a simple question
        ├── streamlit.py            # Run the Chatbot in streamlit where you can ask your own questions
        ├── evaluate.py             # Evaluate the RAG model based on questions-answers samples

    ├── notebooks/                  # Interactive code, useful for try and learn
    ├── .env.template               # Environment variables to feed
    ├── .gitignore
    ├── LICENSE                     # MIT License
    ├── README.md                   # Where to start
    └── requirements.txt            # The dependencies


The process is the following:
- Loading data from Confluence
  - You can keep the Markdown style using the `keep_markdown_format` option added in our [MR]('https://github.com/langchain-ai/langchain/pull/8246')
  - See the `help_desk.ipynb` for a more deep dive analysis
  - Otherwise, you cannot split text in a smart manner using the [MarkdownHeaderTextSplitter]('https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata')
- Load data
- Markdown and RecursiveCharacterTextSplitter
- LLM used: Open AI LLM and embedding
- The QARetrievalChain
- Streamlit as a data interface
