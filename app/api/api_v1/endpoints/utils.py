async def validate_user_registration(collection,user_data_dict: dict):
    username = user_data_dict.get("username")
    email = user_data_dict.get("email")
    username_exist = await collection.find_one({"username": username})
    email_exist = await collection.find_one({"email": email})
    return username_exist, email_exist
