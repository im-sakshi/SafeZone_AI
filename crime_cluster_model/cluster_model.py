import pandas as pd
from sklearn.cluster import KMeans


# Step 1: Load the dataset
def load_data(db):
    docs = db.collection("crime_dataset").stream()

    # Convert Firestore documents to a list of dictionaries
    data = []
    for doc in docs:
        data.append(doc.to_dict())

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    return df


# Step 2: Prepare the data for modeling
def prepare_data(df):
    # Count the number of crimes for each location
    aggregated_data = df.groupby("Location").size().reset_index(name="Crime Count")
    return aggregated_data

# Step 3: Train the K-Means model
def train_kmeans(data, num_clusters=2):
    # Initialize K-Means model
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data["Zone"] = kmeans.fit_predict(data[["Crime Count"]])  # Fit the model
    return data, kmeans


def cluster_and_upload(db): 
    print("Loading data...")
    df = load_data(db)

    print("Preparing data...")
    aggregated_data = prepare_data(df)

    print("Training K-Means model...")
    clustered_data, kmeans = train_kmeans(aggregated_data)

    # Assign cluster labels for user understanding
    clustered_data["Zone Label"] = clustered_data["Zone"].map({0: "Green Zone", 1: "Red Zone"})

    #save clustered data to the firestore db
    collection_ref = db.collection("clustered_data_points")

    # Iterate over the rows of the DataFrame and save them to Firestore
    for _ ,row in clustered_data.iterrows():
        data = row.to_dict()  # Convert each row to a dictionary
        collection_ref.add(data)  # Add the data to Firestore

    print("Clustered data saved to Firestore.")
