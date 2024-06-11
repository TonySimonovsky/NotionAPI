# NotionAPI

`NotionAPI` is a Python module that provides a high-level interface to interact with the Notion API. It allows you to manage Notion pages, databases, and blocks programmatically.

## Features

- Interact with Notion pages, databases, and blocks.
- Retrieve, create, update, and delete pages and blocks.
- Append children blocks to a parent block.
- Query databases.

## Installation

```bash
pip install git+https://github.com/TonySimonovsky/NotionAPI.git
```

## Usage

### Initialization

To use the `NotionAPI` module, you need to initialize it with your Notion API token:

```python
from notionapi import NotionAPI

# Initialize the NotionAPI with your API token
notion_api = NotionAPI(token="your_notion_api_token")
```

### Working with Pages

#### Retrieve a Page

To retrieve a page by its ID:

```python
page = notion_api.page.get(page_id="your_page_id")
print(page)
```

#### Update a Page

To update a page's properties:

```python
properties = {
    "Name": {
        "title": [
            {
                "text": {
                    "content": "Updated Page Title"
                }
            }
        ]
    }
}
updated_page = notion_api.page.update(page_id="your_page_id", properties=properties)
print(updated_page)
```

### Working with Blocks

#### Append Children Blocks

To append children blocks to a parent block:

```python
from notionapi.blocks import ImageBlock

children_blocks = [
    ImageBlock(image_url="https://example.com/image.png")
]

appended_blocks = notion_api.page.block.append(block_id="your_block_id", children=children_blocks)
print(appended_blocks)
```

#### Retrieve Block Children

To retrieve the children of a block:

```python
children = notion_api.page.block.get(block_id="your_block_id")
print(children)
```

### Working with Databases

#### Query a Database

To query a database:

```python
query = {
    "filter": {
        "property": "Status",
        "select": {
            "equals": "In Progress"
        }
    }
}
database_query = notion_api.database.query(database_id="your_database_id", query=query)
print(database_query)
```

## Classes and Methods

### NotionAPI

- `__init__(self, token: str)`: Initializes the NotionAPI with the provided token.
- `_get_headers(self) -> Dict[str, str]`: Returns the headers required for API requests.

### PageAPI

- `__init__(self, api: NotionAPI, page_id: str = None)`: Initializes the PageAPI with the provided NotionAPI instance and page ID.
- `get(self, page_id: str) -> PageObject`: Retrieves a page by its ID.
- `update(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]`: Updates a page's properties.

### BlockAPI

- `__init__(self, api: NotionAPI, parent_id: str = None)`: Initializes the BlockAPI with the provided NotionAPI instance and parent ID.
- `append(self, block_id: str, children: List[Union[Dict[str, Any], BaseModel]], after: Optional[str] = None) -> List[BlockObject]`: Appends children blocks to a parent block.
- `get(self, block_id: str, page_size: int = 100, start_cursor: Optional[str] = None) -> Dict[str, Any]`: Retrieves the children of a block.

### DatabaseObject

- `__init__(self, api: NotionAPI)`: Initializes the DatabaseObject with the provided NotionAPI instance.
- `query(self, database_id: str, query: Optional[Dict[str, Any]] = None) -> DatabaseQuery`: Queries a database.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
