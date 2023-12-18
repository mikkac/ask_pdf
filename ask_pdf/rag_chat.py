""" Converstaion handler for Retriever-Augmented Generation (RAG) model. """

import openai
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.llms import OpenAI
from llama_index.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import AutoMergingRetriever
from llama_index.vector_stores import QdrantVectorStore
from qdrant_client import QdrantClient


class RAGChat:
    """
    A class to handle conversation with a Retriever-Augmented Generation (RAG) model.

    Attributes:
        automerging_query_engine: Engine to handle RAG queries.

    Methods:
        create_embeddings(file): Processes a file to create embeddings.
        send_message(user_msg): Sends a message to the RAG model and returns the response.
    """

    def __init__(self, openai_api_key, qdrant_url):
        """
        Initializes the RAGChat with a specified token limit for
        conversation history and OpenAI API key.

        Args:
            openai_api_key (str): OpenAI API key for accessing GPT-3 services.
        """
        openai.api_key = openai_api_key
        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.qdrant_url = qdrant_url
        self.automerging_index = None
        self.automerging_query_engine = None
        # TODO: Make sure that all models are downloaded before first file upload

    def create_embeddings(self, file):
        """
        Processes the given file to create and store embeddings.

        Args:
            file (str): Path to the file to be processed.
        """
        documents = SimpleDirectoryReader(input_files=[file]).load_data()
        self.automerging_index = self._build_automerging_index(documents, self.llm)
        self.automerging_query_engine = self._get_automerging_query_engine(
            self.automerging_index
        )

    def send_message(self, user_msg):
        """
        Sends a user message to the RAG model and returns the model's response.

        The method formats the input to include both the conversation history
        and the new user message.

        Args:
            user_msg (str): The user's message to send to the model.

        Returns:
            str: The response generated by the RAG model.
        """
        return str(self.automerging_query_engine.query(user_msg))

    def _build_automerging_index(
        self,
        documents,
        llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
    ):
        """
        Builds an automerging index from the given documents using the specified
        language model and embedding model.

        Args:
            documents (list): A list of documents to be indexed.
            llm: The language model to be used for indexing.
            embed_model (str, optional): The embedding model to be used.
                                         Defaults to "local:BAAI/bge-small-en-v1.5".
            save_dir (str, optional): The directory where the index is to be saved.
                                      Defaults to "merging_index".

        Returns:
            An automerging index created from the provided documents and models.
        """
        chunk_sizes = [2048, 512, 128]
        node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)
        nodes = node_parser.get_nodes_from_documents(documents)
        leaf_nodes = get_leaf_nodes(nodes)
        merging_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

        qdrant_client = QdrantClient(url=self.qdrant_url)
        vector_db = QdrantVectorStore(client=qdrant_client, collection_name="documents")
        storage_context = StorageContext.from_defaults(vector_store=vector_db)
        storage_context.docstore.add_documents(nodes)

        return VectorStoreIndex(
            leaf_nodes,
            storage_context=storage_context,
            service_context=merging_context,
        )

    def _get_automerging_query_engine(
        self, automerging_index, similarity_top_k=12, rerank_top_n=2
    ):
        """
        Creates a query engine using the provided automerging index.

        Args:
            automerging_index: The automerging index to be used for creating the query engine.
            similarity_top_k (int, optional): The number of top similar items to retrieve.
                                              Defaults to 12.
            rerank_top_n (int, optional): The number of top items to rerank. Defaults to 2.

        Returns:
            A query engine built using the provided automerging index and specified parameters.
        """
        base_retriever = automerging_index.as_retriever(
            similarity_top_k=similarity_top_k
        )
        retriever = AutoMergingRetriever(
            base_retriever, automerging_index.storage_context, verbose=True
        )
        rerank = SentenceTransformerRerank(
            top_n=rerank_top_n, model="BAAI/bge-reranker-base"
        )
        auto_merging_engine = RetrieverQueryEngine.from_args(
            retriever, node_postprocessors=[rerank]
        )
        return auto_merging_engine
