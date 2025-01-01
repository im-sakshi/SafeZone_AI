import pandas as pd

# Function to upload data to Firestore
def upload_to_firestore_with_id(db , excel_file, collection_name):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Iterate through each row and upload data
    for index, row in df.iterrows():
        # Convert row to dictionary
        row_data = row.to_dict()

        # Add document to the specified Firestore collection
        db.collection(collection_name).add(row_data)

    print("Data uploaded Successfully!")

