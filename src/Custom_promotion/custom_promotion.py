from langchain.document_loaders.csv_loader import CSVLoader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,ServiceContext
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import PromptTemplate
import os
from dotenv import load_dotenv
import pickle
import logging

load_dotenv()

mistral_api_key = os.getenv('mistral_api_key')


def get_promotion(property_details, targeted_audience):
    Var_document = load_csv()
    Var_prompt = get_prompt(property_details, targeted_audience)
    Var_llm = call_llm(Var_document,Var_prompt)
    return Var_llm


def load_csv():
    file_path = r"C:\Users\Karthiga Thangavelu\Documents\Custom-Promotion-Prediction-System\src\Custom_promotion\csv_to_document.pkl"
    if os.path.exists(file_path):
        logging.info("Reading from existing file")
        with open(file_path, 'rb') as f:
            documents = pickle.load(f)
        return documents
    else:
        # Load data
        logging.info("Reading from csv file")
        reader = SimpleDirectoryReader(input_files=[r'C:\Users\Karthiga Thangavelu\Documents\Custom-Promotion-Prediction-System\src\Custom_promotion\property_details_10.csv'])
        documents = reader.load_data()
        with open(file_path, 'wb') as f:
            pickle.dump(documents, f)
        
        return documents

def get_prompt(property_details, targeted_audience):
    
    print(type(property_details))
    property_details = property_details
    targeted_group = targeted_audience


    prompt_template = """\ Your a helpful assisstant for creating an marketing pitch for real estate property\
    For the given property details and target audience generate a tailored and compelling pitch.\

    property details: {property_details}
    target audience: {target_audience}

    The response strictly should be in JSON format with 3 to 4 sentences.\
    For example:
    {{
    "Reponse: {{"pitch":"Experience the pinnacle of luxury at Ocean Breeze Residences in Newport Beach, CA. Designed for dynamic professionals, our stunning beachfront homes offer private beach access, infinity pools, and a state-of-the-art spa. Choose from exquisite 2, 3, or 4-bedroom residences, priced from $1.8M to $4M, each featuring gourmet kitchens and high-end finishes. Elevate your lifestyle in a community where sophistication meets coastal serenity"}}
    """

    template_var_mapping = {"property_str":"property_details", "target_str":"target_audience"}

    prompt_tmpl = PromptTemplate(
        prompt_template, template_var_mappings=template_var_mapping
    )
  
    fmt_prompt = prompt_tmpl.format(property_details=property_details, target_audience=targeted_group)
    return fmt_prompt

def call_llm(Var_document,Var_prompt):
    llm = MistralAI(api_key= mistral_api_key, model="mistral-small")
    embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=mistral_api_key)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

# Create vector store index
    index = VectorStoreIndex.from_documents(Var_document, service_context=service_context)

# Create query engine
    query_engine = index.as_query_engine(similarity_top_k=2)

    formatted_query = Var_prompt
    response = query_engine.query(
        formatted_query
    )
    print(str(response))
    return str(response)