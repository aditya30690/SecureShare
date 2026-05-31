from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://adidas30:adimongos3089@cluster0.vjgahs9.mongodb.net/?retryWrites=true&w=majority"
)

print(client.list_database_names())