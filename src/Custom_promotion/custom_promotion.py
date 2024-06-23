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
    """
    Generates a promotion using property details and targeted audience information.

    Args:
        property_details (dict): A dictionary containing property details.
        targeted_audience (str): The targeted audience for the promotion.

    Returns:
        str: The generated promotion text.
    """

    # Load CSV document containing promotion templates
    Var_document = load_csv()
    
    # Generate prompt based on property details and targeted audience
    Var_prompt = get_prompt(property_details, targeted_audience)
    
    # Call RAG with document and prompt
    Var_response = call_llm(Var_document,Var_prompt)
    
    return Var_response


def load_csv():
    """
    Loads a CSV document containing promotion templates.

    Returns:
        list: List of documents loaded from the CSV file.

    The function checks if a pickle file exists for cached data. If the file exists,
    it reads the data from the pickle file. Otherwise, it reads the data from the CSV
    file, processes it, saves it as a pickle file for future use, and returns the loaded data.
    """

    try:
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
            logging.info("Converted to Pickle file")
            return documents
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def get_prompt(property_details, targeted_audience):
    """
       Generates a marketing pitch prompt based on property details and target audience.

    Args:
        property_details (dict): A dictionary containing property details.
        targeted_audience (str): The targeted audience for the marketing pitch.

    Returns:
        str: The formatted marketing pitch prompt.

    The function constructs a marketing pitch prompt using a template and variable mappings,
    substituting placeholders with actual property details and the target audience.
    """

    # Log the type of property_details
    logging.info(f"Type of property_details: {type(property_details)}")
    
    # Assign variables for better readability
    property_details = property_details
    targeted_group = targeted_audience

    # Define the prompt template    
    prompt_template = """\ Your a helpful assisstant for creating an marketing pitch for real estate property\
    For the given property details and target audience generate a tailored and compelling pitch.\

    property details: {property_details}
    target audience: {target_audience}

    The response strictly should be in JSON format with 3 to 4 sentences.\
    For example:
    {{
    "Reponse: {{"pitch":"Experience the pinnacle of luxury at Ocean Breeze Residences in Newport Beach, CA. Designed for dynamic professionals, our stunning beachfront homes offer private beach access, infinity pools, and a state-of-the-art spa. Choose from exquisite 2, 3, or 4-bedroom residences, priced from $1.8M to $4M, each featuring gourmet kitchens and high-end finishes. Elevate your lifestyle in a community where sophistication meets coastal serenity"}}
    """

    # Define variable mappings for the template
    template_var_mapping = {"property_str":"property_details", "target_str":"target_audience"}

    prompt_tmpl = PromptTemplate(
        prompt_template, template_var_mappings=template_var_mapping
    )
  
    fmt_prompt = prompt_tmpl.format(property_details=property_details, target_audience=targeted_group)
    return fmt_prompt

def call_llm(Var_document,Var_prompt):
    """
    Calls the RAG system and LLM API to generate a response based on the document and prompt.

    Args:
        Var_document (list): List of documents for indexing.
        Var_prompt (str): The prompt for generating a response.

    Returns:
        str: The generated response from the LLM API.
    """
    try:
        # Initialize MistralAI and MistralAIEmbedding objects with API keys
        llm = MistralAI(api_key= mistral_api_key, model="mistral-small")
        embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=mistral_api_key)

        # Create ServiceContext object from defaults
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

        # Create VectorStoreIndex from documents
        index = VectorStoreIndex.from_documents(Var_document, service_context=service_context)

        # Create query engine
        query_engine = index.as_query_engine(similarity_top_k=2)

        # Format the prompt as the query
        formatted_query = Var_prompt

        # Query the engine with the formatted query
        response = query_engine.query(
            formatted_query
        )

        logging.info(f"LLM API call successful. Response: {str(response)}")
      
        return str(response)
    
    except Exception as e:
        logging.error(f"An error occurred in call_llm: {e}")
        raise