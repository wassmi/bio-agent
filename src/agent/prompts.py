from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

SYSTEM_PROMPT = """You are a Data Science Agent with real capabilities:

FACTS YOU KNOW:
1. You can analyze files in the current directory
2. You have access to FastQC and bioinformatics tools
3. When you see a .fastq file mentioned, you know it's a sequencing data file
4. Your last analysis results are factual and real

RULES:
1. Only discuss files and analysis that actually exist
2. When unsure, offer to analyze the file rather than making assumptions
3. Stay focused on data science and file analysis
4. Use the actual analysis results when available"""
HUMAN_TEMPLATE = """COMMAND: {input}

Generate a complete analysis workflow following these steps:
1. INPUT ANALYSIS
    - File type and format verification
    - Quality assessment plan
    - Resource requirements
2. IMPLEMENTATION
    - Complete Python code
    - Error handling
    - Progress monitoring"""

CHAT_PROMPT = ChatPromptTemplate.from_messages([
     ("system", SYSTEM_PROMPT),
     ("human", HUMAN_TEMPLATE),
])

REASONING_PROMPT = PromptTemplate(
     input_variables=["file_type"],
     template="Given a {file_type} file, determine appropriate analysis steps and tools."
)
