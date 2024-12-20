import os
import pickle
from pathlib import Path

from dotenv import load_dotenv
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ConfluenceLoader
from langchain_community.vectorstores import Chroma

load_dotenv()
datadir = Path(__file__).parent.parent / "data"


class DataLoader:
    """Create, load, save the DB using the confluence Loader"""

    def __init__(
        self,
        confluence_url=os.getenv("CONFLUENCE_BASE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        api_key=os.getenv("CONFLUENCE_API_KEY"),
        space_key=os.getenv("CONFLUENCE_SPACE_KEY"),
        persist_directory=Path(__file__).parent.parent / "data",
    ):
        self.confluence_url = confluence_url
        self.username = username
        self.api_key = api_key
        self.space_key = space_key
        self.persist_directory = persist_directory.as_posix()

    def load_from_confluence_loader(self):
        """Load HTML files from Confluence"""
        loader = ConfluenceLoader(
            url=self.confluence_url, username=self.username, api_key=self.api_key, space_key=self.space_key
        )
        # Define the path to the pickle file
        pickle_file = Path(datadir / "50_docs.pkl")
        if pickle_file.exists():
            docs = pickle.load(pickle_file.open("rb"))
            print("Data loaded from pickle file.")
        else:
            docs = loader.load()
            with pickle_file.open("wb") as f:
                pickle.dump(docs, f)
            print("Data written to pickle file.")

        return docs

    def split_docs(self, docs):
        # Markdown
        headers_to_split_on = [
            ("#", "Heading 1"),
            ("##", "Heading 2"),
            ("###", "Heading 3"),
        ]
        print(docs[0].page_content)
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        # Split based on markdown and add original metadata
        md_docs = []
        for doc in docs:
            md_doc = markdown_splitter.split_text(doc.page_content)
            for i in range(len(md_doc)):
                md_doc[i].metadata = md_doc[i].metadata | doc.metadata
            md_docs.extend(md_doc)

        # RecursiveTextSplitter
        # Chunk size big enough
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=20,
            separators=[r"\n\n", r"\n", r"(?<=\. )", " ", ""],
        )

        splitted_docs = splitter.split_documents(md_docs)
        return splitted_docs

    def save_to_db(self, splitted_docs, embeddings):
        """Save chunks to Chroma DB"""
        db = Chroma.from_documents(splitted_docs, embeddings, persist_directory=self.persist_directory)
        db.persist()
        return db

    def load_from_db(self, embeddings):
        """Loader chunks to Chroma DB"""
        db = Chroma(persist_directory=self.persist_directory, embedding_function=embeddings)
        return db

    def set_db(self, embeddings):
        """Create, save, and load db"""

        # Load docs
        docs = self.load_from_confluence_loader()

        # Split Docs
        splitted_docs = self.split_docs(docs)

        # Save to DB
        db = self.save_to_db(splitted_docs, embeddings)

        return db

    def get_db(self, embeddings):
        """Create, save, and load db"""
        db = self.load_from_db(embeddings)
        return db


if __name__ == "__main__":
    dl = DataLoader()
    docs = dl.load_from_confluence_loader()
