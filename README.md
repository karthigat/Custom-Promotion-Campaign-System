# Custom-Promotion-Campaign-System

This project is designed to generate promotional content for real estate properties based on property details and targeted audience information.
The system design uses RAG approach and mistral api to generate compelling marketing pitches.

# File Structure:
.
├── src
│   ├── Custom_promotion
│   │   ├── custom_promotion.py
│   │   ├── property_details_10.csv
│   │   └── csv_to_document.pkl
│   ├── main.py
├── .env
├── request_promotion.py
├── requirements.txt
└── README.md

# custom_promotion.py:
  This file has the following steps:
  Step 1: Data ingestion:
    The main objective of this step is to load the property details data from csv file for converting and storing as a vector for RAG approach.
    This function checks if a pickle file exists for cached data. If it does, it loads the data from the pickle file; otherwise, it loads the data from the CSV file,     
    processes, saves it as a pickle file, and returns the loaded data.
  Step 2: Generating prompt:
    Function constructs a marketing pitch prompt using a template and variable mappings, substituting placeholders with actual property details and the target audience.
  Step 3: Call LLM API:
    This steps implements RAG approach with mistral api. The function initializes MistralAI and MistralAIEmbedding objects, creates a VectorStoreIndex from documents,            creates a query engine, formats the prompt as a query, queries the engine, and returns the response.

# main.py:
  The purpose of this file is to use FASTAPI to get and post the response generated by the llm. It provides an HTTP endpoint (/property) that accepts POST requests with JSON 
  data containing property details and targeted audience information. The function processes this input data, extracts the property details and targeted audience, generates 
  a promotion using the get_promotion function from the Custom_promotion module, and returns the generated promotion as a response.

# request_promotion.py:
  Ngrok: Ngrok allows us to create a secured tunnel from a public URL to your local machine, providing a way to expose servers to the internet. 
  The public URL that is generated through Ngrok is defined and called in request_promotion.py using requests which will get the response from the llm.
  
# Dependencies:
langchain
llama_index
dotenv
pickle
logging
