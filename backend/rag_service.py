import os
from typing import List, Dict

from langchain_community.vectorstores.upstash import UpstashVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.runnables import RunnablePassthrough


UPSTASH_VECTOR_REST_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_chat_model():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.3
    )

def get_vector_store():
    return UpstashVectorStore(
        index_url=UPSTASH_VECTOR_REST_URL,
        index_token=UPSTASH_VECTOR_REST_TOKEN,
        embedding=True 
    )

def format_history(history: List[Dict]) -> List[BaseMessage]:
    """Converts raw history dicts into LangChain Message objects."""
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages

async def get_chat_response(message: str, history: List[Dict]) -> Dict:
   
    if not UPSTASH_VECTOR_REST_URL or not UPSTASH_VECTOR_REST_TOKEN:
        return {"response": "Error: Upstash Vector DB credentials not set.", "sources": []}
    
    if not GROQ_API_KEY:
        return {"response": "Error: Groq API Key not set.", "sources": []}

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = get_chat_model()

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])
    
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    # 2. Main QA Prompt
    qa_system_prompt = """You are "Buddhi Vetta AI", a Senior Fleet Maintenance Consultant. \
Use the following pieces of retrieved technical context to answer the question. \
If you don't know the answer, say that you don't know. \
Keep the response professional and provide bullet points for symptoms, causes, and fixes.

TECHNICAL CONTEXT:
{context}"""

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    # 3. Execution Logic
    chat_messages = format_history(history)
    
    # First, get the standalone question
    standalone_question = await contextualize_q_chain.ainvoke({
        "chat_history": chat_messages,
        "question": message
    })
    
    # Second, retrieve documents based on the standalone question
    docs = await retriever.ainvoke(standalone_question)
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("problem", "Unknown") for doc in docs]

    # Finally, generate the answer
    qa_chain = qa_prompt | llm | StrOutputParser()
    
    full_response = await qa_chain.ainvoke({
        "context": context,
        "chat_history": chat_messages,
        "question": standalone_question
    })

    return {
        "response": full_response,
        "sources": list(set(sources)) # Unique sources
    }
