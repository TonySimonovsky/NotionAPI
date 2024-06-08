from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

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
    id: str
    name: str
    color: str

class SelectOption(BaseModel):
    id: str
    name: str
    color: str

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
    start: str
    end: Optional[str]
    time_zone: Optional[str]

class Formula(BaseModel):
    type: str
    number: Optional[float]

class Relation(BaseModel):
    id: str

class Annotations(BaseModel):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: str

class Text(BaseModel):
    content: str
    link: Optional[str]

class RichText(BaseModel):
    type: str
    text: Text
    annotations: Annotations
    plain_text: str
    href: Optional[str]

class Rollup(BaseModel):
    type: str
    number: Optional[float]
    function: str

class PageProperty(BaseModel):
    id: str
    type: str
    multi_select: Optional[List[MultiSelectOption]]
    select: Optional[SelectOption]
    number: Optional[float]
    people: Optional[List[People]]
    date: Optional[Date]
    formula: Optional[Formula]
    relation: Optional[List[Relation]]
    rich_text: Optional[List[RichText]]
    checkbox: Optional[bool]
    rollup: Optional[Rollup]
    url: Optional[str]
    title: Optional[List[RichText]]

class Page(BaseModel):
    object: str
    id: str
    created_time: str
    last_edited_time: str
    created_by: User
    last_edited_by: User
    cover: Optional[Cover]
    icon: Optional[Emoji]
    parent: Parent
    archived: bool
    properties: dict
    url: str

class DatabaseQuery(BaseModel):
    object: str
    results: List[Page]
    next_cursor: Optional[str]
    has_more: bool
    type: str
    page_or_database: Dict[str, Any]
