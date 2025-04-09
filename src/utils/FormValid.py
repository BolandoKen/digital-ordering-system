from PyQt6.QtWidgets import QMessageBox

def formValidated(dataTuple, panelName):
    error_messages = []
    
    if panelName == "category":
        name = dataTuple[0]
        if (not name.strip()):
            error_messages.append("category name is empty")
        if len(name) > 128: #same as table
            error_messages.append("category name is too long (max 128 chars)")
            
    elif panelName == "food":
        name, price = dataTuple[0], dataTuple[1]
        if (not name.strip()):
            error_messages.append("food name cannot be empty")
        if len(name) > 128: #same as table
            error_messages.append("food name is too long (max 128 chars)")
        if (not price.strip()):
                error_messages.append("price cannot be empty")
        else:     
            try:
                price_float = float(price)
                if (price_float <= 0):
                    error_messages.append("price must be greater than 0")
                if (price_float > 999.99):
                    error_messages.append("price is too high (max 999.99)")
            except ValueError:
                error_messages.append("price must be a valid number")
    
    if error_messages:
        QMessageBox.warning(
            None,
            "invalid input",
            "\n".join(error_messages) 
        )
        return False
    return True
        