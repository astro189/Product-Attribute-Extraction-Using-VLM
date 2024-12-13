import json
import os
from CODE.inference import generate_response
from PIL import Image

def ask_questions(image, base_name):
    prompt= [
        """
    Describe the product attributes as shown in the image in the form (attribute:value) for the following attributes Name, Product Type, Barcode, Weight, Price, Country of Origin, Manufacturing Date, Expiration Date, Nutritional Information, Contact Information
    Manufacturer, FSSAI Certified. Include all attributes in response."""
    ]

    product_info = generate_response(image, prompt)

    output = {
    "image": base_name,
    "product_info": {
        "Product name": product_info.get("Name", ""),
        "Product type": product_info.get("Product Type", ""),
        "Identification number": product_info.get("Barcode", ""),
        "Barcode": product_info.get("Barcode", ""),
        "Quantity size": product_info.get("Weight", ""),
        "Weight": product_info.get("Weight", ""),
        "Volume": product_info.get("Weight", ""),
        "Expiration date": product_info.get("Expiration Date", ""),
        "Use before date": product_info.get("Manufacturing Date", ""),
        "Country of origin": product_info.get("Country of Origin", ""),
        "Manufacturing date": product_info.get("Manufacturing Date", ""),
        "Contact information": product_info.get("Contact Information", ""),
        "Price": product_info.get("Price", ""),
        "MRP": product_info.get("Price", ""),
        "Manufacturer": product_info.get("Manufacturer", ""),
        "FSSAI certified": product_info.get("FSSAI Certified", ""),
        "Nutritional information": product_info.get("Nutritional Information", "")
        }
    }

    with open("product_info.json", "w") as json_file:
        json.dump(output, json_file, indent=2)

    print("Product information has been saved to product_info.json")





if __name__== "__main__":
    image_path = ""
    product_info = ask_questions(image_path)