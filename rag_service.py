import os
import warnings
from transformers import logging as hf_logging
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

warnings.filterwarnings("ignore")
hf_logging.set_verbosity_error()

class RAGService:
    def __init__(self, data_path="./my_knowledge", index_path="./faiss_index"):
        self.data_path = data_path
        self.index_path = index_path
        # 使用本地免费的 Embedding 模型
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def build_vector_store(self):
        """加载文档并构建向量库"""
        # 如果用户clone代码后没有该文件夹，自动创建
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            print(f"\n[提示] 已自动创建 {self.data_path} 文件夹，请在其中放入 PDF 或 TXT 教学资料。")
            return None

        # 1. 加载数据 (支持 PDF 和 TXT)
        pdf_loader = DirectoryLoader(self.data_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader(self.data_path, glob="**/*.txt", loader_cls=TextLoader)

        docs = pdf_loader.load() + txt_loader.load()
        if not docs:
            print(f"\n[提示] {self.data_path} 文件夹为空，跳过构建本地知识库。")
            return None

        # 2. 切分文档 (防止文本过长)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        # 3. 创建并保存向量库
        print("\n[系统] 正在构建本地知识库向量索引，请稍候...")
        vectorstore = FAISS.from_documents(splits, self.embeddings)
        vectorstore.save_local(self.index_path)
        print("[系统] 本地知识库构建完成！")
        return vectorstore

    def get_retriever(self):
        """获取检索器"""
        if os.path.exists(self.index_path):
            vectorstore = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            vectorstore = self.build_vector_store()

        return vectorstore.as_retriever(search_kwargs={"k": 3}) if vectorstore else None