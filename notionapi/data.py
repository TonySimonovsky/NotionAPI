from typing import Dict, Any, List, Optional, Union, get_origin, get_args
from pydantic import BaseModel, Field
import json


class User(BaseModel):
    object: str
    id: str


class External(BaseModel):
    url: str


class Cover(BaseModel):
    type: str
    external: External


class Emoji(BaseModel):
    type: str
    emoji: str


class Parent(BaseModel):
    type: str
    database_id: str


class MultiSelectOption(BaseModel):
    id: str = None
    name: str = None
    color: str = None


class SelectOption(BaseModel):
    id: str = None
    name: str = None
    color: str = None


class Person(BaseModel):
    email: str


class People(BaseModel):
    object: str
    id: str
    name: str
    avatar_url: Optional[str]
    type: str
    person: Person


class Date(BaseModel):
    id: str = None
    type: str = "date"
    date: Optional[dict] = {
        "start": None,
        "end": None,
        "time_zone": None
    }

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data.pop('id', None)
        data.pop('type', None)
        return data

    @property
    def default(self) -> str:
        return self.date['start']
    @default.setter
    def default(self, value: str) -> None:
        self.date['start'] = value


class Formula(BaseModel):
    type: str
    number: Optional[float]


class Relation(BaseModel):
    id: str


class Annotations(BaseModel):
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    strikethrough: Optional[bool] = False
    underline: Optional[bool] =False
    code: Optional[bool] = False
    color: Optional[str] = "default"

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        # Remove fields that are None
        return {k: v for k, v in data.items() if v is not None}


class Text(BaseModel):
    type: str = "text"
    text: dict = {
        "content": "",
        "link": ""
    }
    annotations: Annotations = Annotations()
    plain_text: str = ""
    href: Optional[str] = None

    @property
    def default(self) -> str:
        return self.text["content"]
    @default.setter
    def default(self, value: str) -> None:
        self.text["content"] = value

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data.pop('type', None)  # Remove the 'type' attribute
        return data


class RichText(BaseModel):
    id: str = None
    type: str = "rich_text"
    rich_text: List[Text] = []

    @property
    def default(self) -> str:
        return self.rich_text[0].text["content"]
    @default.setter
    def default(self, value: str) -> None:
        if self.rich_text:
            self.rich_text[0].text["content"] = value
        else:
            self.rich_text = [ Text(text={ "content": value }) ]

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data.pop('id', None)  # Remove the 'type' attribute
        data.pop('type', None)  # Remove the 'type' attribute
        if 'text' in data and isinstance(data['text'], dict):
            data['text'].pop('type', None)  # Remove the 'type' attribute from 'text'
        return data


class Title(BaseModel):
    id: str = None
    type: str = "title"
    title: List[Text] = []

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data.pop('id', None)  # Remove the 'type' attribute
        data.pop('type', None)  # Remove the 'type' attribute
        if 'text' in data and isinstance(data['text'], dict):
            data['text'].pop('type', None)  # Remove the 'type' attribute from 'text'
        return data


class Rollup(BaseModel):
    type: str
    number: Optional[float]
    function: str


def initialize_type(type_name: str, **kwargs) -> Any:
    type_mapping = {
        "multi_select": MultiSelectOption,
        "select": SelectOption,
        "number": float,
        "people": List[People],
        "date": Date,
        "formula": Formula,
        "relation": List[Relation],
        "text": Text,
        "rich_text": RichText,
        "checkbox": bool,
        "rollup": Rollup,
        "url": str,
        "title": Title
    }
    cls = type_mapping.get(type_name, None)
    if cls is None:
        raise ValueError(f"Unsupported type: {type_name}")
    
    origin = get_origin(cls)
    args = get_args(cls)

    if origin is list and args:
        inty = [ args[0](**item) for item in kwargs.get(type_name, []) ]

        if type_name in kwargs:
            kwargs.pop(type_name)

        if not inty:
            dflt = { k: args[0].__fields__[k].default for k in args[0].__fields__.keys() }
            dflt["type"] = type_name
            inty = [ args[0](**dflt) ]
        return inty

    elif isinstance(cls, type) and issubclass(cls, BaseModel):
        if type_name in kwargs and kwargs[type_name]:
            inty = cls(**kwargs)
            return inty
        else:
            inty = cls()
            return inty


class Page(BaseModel):
    object: str
    id: str
    created_time: str
    last_edited_time: str
    created_by: User
    last_edited_by: User
    cover: Optional[Cover] = None
    icon: Optional[Emoji] = None
    parent: Parent
    archived: bool
    properties: Dict[str, Any]
    url: str


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Page':
        properties = {}

        # print(f"___data['properties']: {data['properties']}")

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
            created_time=data['created_time'],
            last_edited_time=data['last_edited_time'],
            created_by=User(**data['created_by']),
            last_edited_by=User(**data['last_edited_by']),
            cover=Cover(**data['cover']) if data.get('cover') else None,
            icon=Emoji(**data.get('icon')) if data.get('icon') else None,
            parent=Parent(**data['parent']),
            archived=data['archived'],
            properties=properties,
            url=data['url']
        )


class DatabaseQuery(BaseModel):
    object: str
    results: List[Page]
    next_cursor: Optional[str]
    has_more: bool
    type: str
    page_or_database: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatabaseQuery':

        results = [Page.from_dict(page_data) for page_data in data.get('results', [])]

        return cls(
            object=data['object'],
            results=results,
            next_cursor=data.get('next_cursor'),
            has_more=data['has_more'],
            type=data['type'],
            page_or_database=data['page_or_database']
        )

