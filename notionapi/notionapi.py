import requests
import json
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union, get_origin, get_args
from .types import *
from .blocks import *



class NotionAPI:
    """
    A high-level class to interact with the Notion API.

    Attributes:
        token (str): The API token for authentication.
        base_url (str): The base URL for the Notion API.
        database (DatabaseObject): An instance to interact with Notion databases.
        page (PageAPI): An instance to interact with Notion pages.
    """
    
    def __init__(self, token: str):
        """
        Initializes the NotionAPI with the provided token.

        Args:
            token (str): The API token for authentication.
        """
        self.token = token
        self.base_url = "https://api.notion.com/v1"

        self.database = DatabaseObject(self)
        self.page = PageAPI(self)

    def _get_headers(self) -> Dict[str, str]:
        """
        Returns the headers required for API requests.

        Returns:
            Dict[str, str]: A dictionary of headers.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }


"""
Page
"""

class PageObject(BaseModel):
    """
    A class representing a Notion page object.

    Attributes:
        object (str): The type of the object ("page").
        id (str): The ID of the page.
        created_time (CreatedTimeObject): The creation time of the page.
        last_edited_time (LastEditedTimeObject): The last edited time of the page.
        created_by (UserObject): The user who created the page.
        last_edited_by (UserObject): The user who last edited the page.
        cover (Optional[Any]): The cover image of the page.
        icon (Optional[Any]): The icon of the page.
        parent (Any): The parent object of the page.
        archived (bool): Whether the page is archived.
        properties (Dict[str, Any]): The properties of the page.
        url (str): The URL of the page.
    """
    object: str = "page"
    id: str
    created_time: CreatedTimeObject
    last_edited_time: LastEditedTimeObject
    created_by: 'UserObject'
    last_edited_by: 'UserObject'
    cover: Optional[Any] = None
    icon: Optional[Any] = None
    parent: Any
    archived: bool
    properties: Dict[str, Any]
    url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PageObject':
        """
        Initializes a PageObject from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing the page data.

        Returns:
            PageObject: A new instance of PageObject.
        """
        properties = {}

        for key, value in data['properties'].items():
            type_name = value.get('type')
            if type_name:
                properties[key] = initialize_type(type_name, **value)
            else:
                print("___ does this ever happen?")
                properties[key] = value

        return cls(
            object=data['object'],
            id=data['id'],
            created_time=CreatedTimeObject(created_time=data['created_time']),
            last_edited_time=LastEditedTimeObject(last_edited_time=data['last_edited_time']),
            created_by=UserObject(**data['created_by']),
            last_edited_by=UserObject(**data['last_edited_by']),
            # cover=Cover(**data['cover']) if data.get('cover') else None,
            # icon=Emoji(**data.get('icon')) if data.get('icon') else None,
            parent=ParentObject.from_dict(data['parent']),
            archived=data['archived'],
            properties=properties,
            url=data['url']
        )


class PageAPI:
    def __init__(self, api: NotionAPI, page_id: str = None):
        self.api = api
        self.page_id = page_id
        self.block = BlockAPI(api=api, parent_id=page_id)

    def get(self, page_id) -> 'PageObject':
        endpoint_url = f"{self.api.base_url}/pages/{page_id}"
        headers = self.api._get_headers()
        response = requests.get(endpoint_url, headers=headers)
        response.raise_for_status()

        page = PageObject.from_dict(response.json())

        return page

    def update(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        page = self.get(page_id=page_id)

        # Normalize properties to be passed to Notion API
        for k, v in properties.items():
            # if a string value was passed (a way to pass values without complex dict definition)
            if isinstance(v, str):
                # if the property is a list of values
                if isinstance(page.properties[k], list):
                    if len(page.properties[k]) > 0:
                        for elem in page.properties[k]:
                            elem.default = v
                    else:
                        print(f"...no data in... {k} {page.properties[k]}\n")
                # if the property is a single value
                else:
                    try:
                        page.properties[k].default = v
                    except Exception as e:
                        print(f"Error updating page property '{k}'")
                        print(f"...page.properties[{k}] (type {type(page.properties[k])}: {page.properties[k]}")
                        print(f"...error: {e}")
                        return None

                    print(f"...page.properties[{k}] (type {type(page.properties[k])}: {page.properties[k]}")
                    properties[k] = page.properties[k].dict()
            # if the property is passed as a properly structured dict
            elif isinstance(v, dict):
                properties[k] = v


        # Update page properties through Notion API
        print(f"trying to update page {page_id} with properties {properties}")
        url = f"{self.api.base_url}/pages/{page_id}"
        headers = self.api._get_headers()
        data = {
            "properties": properties
        }
        try:
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"updated page {page_id} with properties {properties}\n\n")
            return response.json()
        except Exception as e:
            print(f"...Error updating page properties: {e}, {vars(response)}")
            return None


"""
Block
"""

class BlockObject(BaseModel):
    object: str
    id: str
    parent: Dict[str, Any]
    created_time: str
    last_edited_time: str
    created_by: Dict[str, Any]
    last_edited_by: Dict[str, Any]
    has_children: bool
    archived: bool
    type: str
    block_type: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlockObject':
        block_type = data.get(data['type'], {})
        return cls(
            object=data['object'],
            id=data['id'],
            parent=data['parent'],
            created_time=data['created_time'],
            last_edited_time=data['last_edited_time'],
            created_by=data['created_by'],
            last_edited_by=data['last_edited_by'],
            has_children=data['has_children'],
            archived=data['archived'],
            type=data['type'],
            block_type=block_type
        )


class BlockAPI:
    def __init__(self, api: NotionAPI, parent_id: str = None):

        self.api = api
        self.parent_id = parent_id


    def append(self, block_id: str, children: List[Union[Dict[str, Any], BaseModel]], after: Optional[str] = None) -> List[BlockObject]:
        """
        Appends children blocks to a parent block.

        Args:
            block_id (str): The ID of the parent block.
            children (List[Union[Dict[str, Any], BaseModel]]): A list of children blocks, either as dictionaries or Block objects.
            after (Optional[str], optional): The ID of the block after which to append the children. Defaults to None.

        Returns:
            List[BlockObject]: A list of appended Block objects.
        """
        url = f"{self.api.base_url}/blocks/{block_id}/children"
        headers = self.api._get_headers()

        # Ensure all children are dictionaries
        serialized_children = []
        for child in children:
            if isinstance(child, BaseModel):
                serialized_children.append(child.dict())
            else:
                serialized_children.append(child)

        payload = {
            "children": serialized_children
        }
        if after:
            payload["after"] = after

        try:
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return [BlockObject.from_dict(block) for block in data.get("results", [])]
        except requests.exceptions.RequestException as e:
            print(f"Error appending children to block {block_id}: {e}")
            if e.response is not None:
                print(f"Response content: {e.response.content}")
            return []


    def get(self, block_id: str = None, page_size: int = 100, start_cursor: Optional[str] = None) -> Dict[str, Any]:
        if not block_id:
            block_id = self.parent_id
        
        url = f"{self.api.base_url}/blocks/{block_id}/children"
        headers = self.api._get_headers()
        params = {
            "page_size": page_size
        }
        if start_cursor:
            params["start_cursor"] = start_cursor

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving children for block {block_id}: {e}")
            if e.response is not None:
                print(f"Response content: {e.response.content}")
            return {}



# -------------------------------------
#
# [To clean]
#


class UserObject(BaseModel):
    object: str = "user"
    id: str
    type: Optional[str] = None  # "person" or "bot"
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None  # Only for "person" type
    owner: Optional[dict] = None  # Only for "bot" type
    workspace_name: Optional[str] = None  # Only for "bot" type


class ParentObject(BaseModel):
    type: str
    database_id: Optional[str] = None
    page_id: Optional[str] = None
    workspace: Optional[bool] = None
    block_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ParentObject':
        parent_type = data.get("type")
        if parent_type == "database_id":
            return cls(type=parent_type, database_id=data.get("database_id"))
        elif parent_type == "page_id":
            return cls(type=parent_type, page_id=data.get("page_id"))
        elif parent_type == "workspace":
            return cls(type=parent_type, workspace=data.get("workspace"))
        elif parent_type == "block_id":
            return cls(type=parent_type, block_id=data.get("block_id"))
        else:
            raise ValueError(f"Unsupported parent type: {parent_type}")


class DatabaseObject:
    def __init__(self, api: NotionAPI):
        self.api = api

    def query(self, database_id: str, query: Optional[Dict[str, Any]] = None) -> 'DatabaseQuery':
        url = f"{self.api.base_url}/databases/{database_id}/query"
        headers = self.api._get_headers()

        response = requests.post(url, headers=headers, json=query or {})
        response.raise_for_status()

        dbq = DatabaseQuery.from_dict(response.json())

        return dbq


class DatabaseQuery(BaseModel):
    object: str
    results: List[PageObject]
    next_cursor: Optional[str]
    has_more: bool
    type: str
    page_or_database: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseQuery':

        results = [PageObject.from_dict(page_data) for page_data in data.get('results', [])]

        return cls(
            object=data['object'],
            results=results,
            next_cursor=data.get('next_cursor'),
            has_more=data['has_more'],
            type=data['type'],
            page_or_database=data['page_or_database']
        )

