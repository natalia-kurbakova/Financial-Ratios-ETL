import webscrape
import APIcalls
import uploadToAzureBlob


if __name__ == "__main__":
    webscrape.main()
    APIcalls.main()
    uploadToAzureBlob.main()
