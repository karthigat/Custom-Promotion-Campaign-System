from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,ServiceContext
import os
import pickle
def load_csv():
    # loader = CSVLoader(file_path=r'C:\Users\Karthiga Thangavelu\Documents\Custom-Promotion-Prediction-System\src\Custom_promotion\property_details_10.csv', encoding='utf-8', csv_args={'delimiter': ','})
    file_path = r"C:\Users\Karthiga Thangavelu\Documents\Custom-Promotion-Prediction-System\src\Custom_promotion\csv_to_document.pkl"
    if os.path.exists(file_path):
        print('from file')
        # with open(file_path, 'r') as file:
        #     content_read = file.read().strip()
        with open(file_path, 'rb') as f:
            documents = pickle.load(f)
        print(documents)
        print(type(documents))
        return documents
    else:
        # Load data
        print('from csv file')
        reader = SimpleDirectoryReader(input_files=[r'C:\Users\Karthiga Thangavelu\Documents\Custom-Promotion-Prediction-System\src\Custom_promotion\property_details_10.csv'])
        documents = reader.load_data()
        with open(file_path, 'wb') as f:
            pickle.dump(documents, f)
        
        return documents

