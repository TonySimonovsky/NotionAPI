from typing import List, Optional, Union, Dict, Any, get_origin, get_args
from pydantic import BaseModel



def initialize_type(type_name: str, **kwargs) -> Any:
    type_mapping = {
        "multi_select": MultiSelectObject,
        "select": SelectObject,
        "number": float,
        # "people": List[People],
        "date": DateObject,
        "formula": FormulaObject,
        # "relation": List[Relation],
        # "text": Text,
        "last_edited_time": LastEditedTimeObject,
        "created_time": CreatedTimeObject,
        "rich_text": RichTextObject,
        "checkbox": CheckboxObject,
        "rollup": RollupObject,
        "url": URLObject,
        "title": TitleObject
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
        # print(f"cls: {cls} ; type_name: {type_name} ; kwargs: {kwargs}")
        # inty = cls(**kwargs)
        # return inty
        # print(f"cls: {cls} ; type_name: {type_name} ; kwargs: {kwargs}")
        if type_name in kwargs and kwargs[type_name]:
            inty = cls(**kwargs)
            return inty
        else:
            inty = cls()
            return inty



#
# Base Object containing default properties and methods
#

class BaseObject(BaseModel):
    id: str = ""

    def dict(self, **kwargs) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data.pop('id', None)
        data.pop('type', None)
        data.pop('updatable', None)
        return data


#
# Checkbox
#

class CheckboxType(BaseModel):
    checkbox: Optional[bool] = None

class CheckboxObject(BaseObject):
    checkbox: CheckboxType
    updatable: bool = True


#
# Created
#

class CreatedByType(BaseModel):
    object: Optional[str] = None
    id: Optional[str] = None

class CreatedByObject(BaseObject):
    id: str
    type: str
    created_by: CreatedByType
    updatable: bool = False

class CreatedTimeObject(BaseObject):
    type: str = "created_time"
    created_time: Optional[str] = ""
    updatable: bool = False


#
# Date
#

class DateType(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    time_zone: Optional[str] = None

class DateObject(BaseObject):
    type: str = "date"
    date: DateType = DateType()
    updatable: bool = True

    @property
    def default(self) -> str:
        return self.date.start
    @default.setter
    def default(self, value: str) -> None:
        self.date.start = value


#
# Email
#

class EmailType(BaseModel):
    email: Optional[str] = None

class EmailObject(BaseObject):
    type: str = "email"
    email: EmailType
    updatable: bool = True


#
# File
#

class FileObject(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    external: Optional[dict] = None

class FilesType(BaseModel):
    files: Optional[List[FileObject]] = None

class FilesObject(BaseObject):
    type: str
    files: FilesType
    updatable: bool = True


#
# Formula
#

class FormulaType(BaseModel):
    type: Optional[str] = None
    boolean: Optional[bool] = None
    date: Optional[str] = None
    number: Optional[float] = None
    string: Optional[str] = None

class FormulaObject(BaseObject):
    type: str
    formula: FormulaType
    updatable: bool = False


#
# Last Edited
#

class LastEditedByType(BaseModel):
    object: Optional[str] = None
    id: Optional[str] = None

class LastEditedByObject(BaseObject):
    type: str
    last_edited_by: LastEditedByType
    updatable: bool = False

class LastEditedTimeObject(BaseObject):
    type: str = "last_edited_time"
    last_edited_time: Optional[str] = None
    updatable: bool = False


#
# Multi Select
#

class MultiSelectOptionType(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

class MultiSelectObject(BaseObject):
    type: str = "multi_select"
    multi_select: Optional[List[MultiSelectOptionType]] = [MultiSelectOptionType()]
    updatable: bool = True


#
# Number
#

class NumberType(BaseModel):
    number: Optional[float] = None

class NumberObject(BaseObject):
    type: str
    number: NumberType
    updatable: bool = True


#
# People
#

class PeopleType(BaseModel):
    people: Optional[List[CreatedByType]] = None

class PeopleObject(BaseObject):
    type: str
    people: PeopleType
    updatable: bool = True


#
# Phone Number
#

class PhoneNumberType(BaseModel):
    phone_number: Optional[str] = None

class PhoneNumberObject(BaseObject):
    type: str
    phone_number: PhoneNumberType
    updatable: bool = True


#
# Relation
#

class RelationType(BaseModel):
    relation: Optional[List[dict]] = None
    has_more: Optional[bool] = None

class RelationObject(BaseObject):
    type: str
    relation: RelationType
    updatable: bool = True


#
# Rollup
#

class RollupType(BaseModel):
    type: Optional[str] = None
    number: Optional[float] = None
    function: Optional[str] = None

class RollupObject(BaseObject):
    type: str
    rollup: RollupType
    updatable: bool = False


#
# Text
#

class AnnotationsType(BaseModel):
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    strikethrough: Optional[bool] = False
    underline: Optional[bool] = False
    code: Optional[bool] = False
    color: Optional[str] = "default"

class TextType(BaseModel):
    type: Optional[str] = "text"
    text: Optional[dict] = { "content" : "", "link" : None }
    annotations: Optional[dict] = AnnotationsType()
    plain_text: Optional[str] = ""
    href: Optional[str] = ""

class RichTextObject(BaseObject):
    type: str = "rich_text"
    rich_text: List[TextType] = [TextType()]
    updatable: bool = True
    
    @property
    def default(self) -> str:
        return self.rich_text[0].text['content']
    @default.setter
    def default(self, value: str) -> None:
        self.rich_text[0].text['content'] = value


#
# Select
#

class SelectOptionType(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

class SelectType(BaseModel):
    select: Optional[SelectOptionType] = None

class SelectObject(BaseObject):
    type: str
    select: SelectType
    updatable: bool = True


#
# Status
#

class StatusType(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

class StatusObject(BaseObject):
    type: str
    status: StatusType
    updatable: bool = True


#
# Title
#

class TitleObject(BaseObject):
    type: str = "title"
    title: Optional[List[TextType]] = [TextType()]
    updatable: bool = True


#
# URL
#

class URLObject(BaseObject):
    type: str = "url"
    url: str = ""
    updatable: bool = True


#
# Unique ID
#

class UniqueIDType(BaseModel):
    number: Optional[int] = None
    prefix: Optional[str] = None

class UniqueIDObject(BaseObject):
    type: str
    unique_id: UniqueIDType
    updatable: bool = False


#
# Verification
#

class VerificationType(BaseModel):
    state: Optional[str] = None
    verified_by: Optional[CreatedByType] = None
    date: Optional[DateType] = None

class VerificationObject(BaseObject):
    type: str
    verification: VerificationType
    updatable: bool = False
