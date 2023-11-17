from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import os
import Keys

base_path = os.getcwd()
directory = os.path.join(base_path, r'csvFiles')

def uploadCSVtoBlob():
    os.environ['CONNECTION_STRING'] = Keys.AZURE_STORE_CONNECTION_STRING

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(os.environ['CONNECTION_STRING'])
    # Now you can use the blob_service_client to interact with your blob storage

    # Name of the container
    container_name = "sandp100"
    container_client = blob_service_client.get_container_client(container_name)

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # Create the full file path
            file_path = os.path.join(directory, filename)

            # Create the blob name, could be filename or a combination of folder and filename
            blob_name = f"StagingArea/{filename}"

            # Upload the file
            try:
                with open(file_path, "rb") as data:
                    print(f"Uploading {filename} to blob storage...")
                    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
                    print(f"Uploaded {filename}")
            except FileNotFoundError:
                print(f"The file at {file_path} was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    uploadCSVtoBlob()

