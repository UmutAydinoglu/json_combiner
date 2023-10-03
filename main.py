"""
This is a simple Json combiner and parser.

The e-commerce website I am working on does not have an export feature.
The website is connected to an ERP system using Navision Dynamics.
It pulls item information from Navision but info can be manipulated in the website as well.

There are some items that are passive in Navision and active in the website.
Navision and website does not communicate the status of the item between each other.

My task was to find said items and change their status to passive in the website

I extracted the product json objects using web browser developer tools.
In my case products consist of 8 individual pages with ~50 products each.
I extracted all 8 json objects individually and combined them here.

Once combined, I parsed them to take only the item codes and put them in a pandas dataframe.
And from the pandas dataframe I created an Excel file to compare the passive Navision items with the data extracted.
"""

import json
import os
import pandas as pd

PATH = ".\\json_files"

json_files = [os.path.join(PATH, file) for file in os.listdir(PATH)]


def combine_json(json_files: list):
    # combine the json files return as a list
    combined_data = []

    for file_name in json_files:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

            data_array = data.get("data", [])

            combined_data.extend(data_array)

    return combined_data


def create_json(combined_data: list):
    # take the json list and create a json file

    output_file_name = "combined.json"

    with open(output_file_name, "w") as output_file:

        json.dump(combined_data, output_file, indent=4)

    return output_file_name


def extract_item_codes(combined_json_file):
    # extract item codes from the combined json file and return as list
    with open(combined_json_file, "r") as json_file:
        data = json.load(json_file)

    codes = [product["code"] for product in data]

    return codes


def items_to_excel(items: list) -> None:
    # convert the item codes list to a dataframe and create an Excel file from it

    df = pd.DataFrame(items)
    df.to_excel("items.xlsx", index=False)


if __name__ == '__main__':

    data = combine_json(json_files=json_files)
    combined_json = create_json(data)
    codes = extract_item_codes(combined_json)
    items_to_excel(codes)
