from notionapi import NotionAPI
import os

# Initialize the NotionAPI with your integration token
notion = NotionAPI(os.environ["NOTION_API_KEY"])

# # Define the query parameters
filter_params = {
    "property": "interface",
    "multi_select": {
        "is_not_empty": True
    }
}

# Query the database using the database ID, filter, and sorting parameters
query_params = {
    "filter": filter_params,
}
result = notion.database.query(os.environ["NOTION_DB_ID"], query_params)

# Print the result
print(result)
