from PyQt6.QtWidgets import QMessageBox

def formValidated(dataTuple, panelName):
    error_messages = []
    error_dict = {
        "category_name" : None,
        "food_name" : None,
        "food_price" : None,
        "profile_name" : None,
        "final" : True,
    }
    if panelName == "category":
        name = dataTuple[0]
        if (not name.strip()):
            error_dict["category_name"] = "cannot be empty"
            error_messages.append("category name is empty")
        if len(name) > 128: #same as table
            error_dict["category_name"] = "too long (max 128 chars)"
            error_messages.append("category name is too long (max 128 chars)")       
    elif panelName == "food":
        name, price = dataTuple[0], dataTuple[1]
        if (not name.strip()):
            error_dict["food_name"] = "cannot be empty"
            error_messages.append("food name cannot be empty")
        if len(name) > 128: #same as table
            error_dict["food_name"] = "too long (max 128 chars)"
            error_messages.append("food name is too long (max 128 chars)")
        if (not price.strip()):
            error_dict["food_price"] = "price cannot be empty"
            error_messages.append("price cannot be empty")
        else:     
            try:
                price_float = float(price)
                if (price_float <= 0):
                    error_dict["food_price"] = "must be greater than 0"
                    error_messages.append("price must be greater than 0")
                if (price_float > 999.99):
                    error_dict["food_price"] = "too high (max 999.99)"
                    error_messages.append("price is too high (max 999.99)")
            except ValueError:
                error_dict["food_price"] = "invalid number"
                error_messages.append("price must be a valid number")
    elif panelName == "profile" :
        name = dataTuple[0]
        if (not name.strip()):
            error_dict["profile_name"] = "cannot be empty"
            error_messages.append("profile name is empty")
        if len(name) > 128: #same as table
            error_dict["profile_name"] = "too long (max 128 chars)"
            error_messages.append("profile name is too long (max 128 chars)")       
            
    if error_messages:
        error_dict["final"] = False
        return error_dict
    return error_dict
        