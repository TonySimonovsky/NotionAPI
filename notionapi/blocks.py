from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .types import *


#
# Bookmark
#

class BookmarkContent(BaseModel):
    caption: List[RichTextObject]
    url: str

class BookmarkBlock(BaseModel):
    type: str = "bookmark"
    bookmark: BookmarkContent


#
# Breadcrumb
#

class BreadcrumbBlock(BaseModel):
    type: str = "breadcrumb"
    breadcrumb: str = ""


#
# Bulleted List Item
#

class BulletedListItemContent(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    children: Optional[List[Dict[str, Any]]] = None

class BulletedListItemBlock(BaseModel):
    type: str = "bulleted_list_item"
    bulleted_list_item: BulletedListItemContent


#
# Callout
#

class CalloutContent(BaseModel):
    rich_text: List[RichTextObject]
    icon: Optional[Dict[str, Any]] = None
    color: str

class CalloutBlock(BaseModel):
    type: str = "callout"
    callout: CalloutContent


#
# Child Database (?junk from AI)
#

class ChildDatabaseContent(BaseModel):
    title: str

class ChildDatabaseBlock(BaseModel):
    type: str = "child_database"
    child_database: ChildDatabaseContent


#
# Child Page (?junk from AI)
#

class ChildPageContent(BaseModel):
    title: str

class ChildPageBlock(BaseModel):
    type: str = "child_page"
    child_page: ChildPageContent


#
# Code
#

class CodeContent(BaseModel):
    caption: List[RichTextObject]
    rich_text: List[RichTextObject]
    language: str

class CodeBlock(BaseModel):
    type: str = "code"
    code: CodeContent


#
# Column
#

class ColumnListContent(BaseModel):
    pass

class ColumnListBlock(BaseModel):
    type: str = "column_list"
    column_list: ColumnListContent = ColumnListContent()

class ColumnContent(BaseModel):
    pass

class ColumnBlock(BaseModel):
    type: str = "column"
    column: ColumnContent = ColumnContent()


#
# Divider
#

class DividerContent(BaseModel):
    pass

class DividerBlock(BaseModel):
    type: str = "divider"
    divider: DividerContent = DividerContent()


#
# Embed
#

class EmbedContent(BaseModel):
    url: str

class EmbedBlock(BaseModel):
    type: str = "embed"
    embed: EmbedContent


#
# Equation
#

class EquationContent(BaseModel):
    expression: str

class EquationBlock(BaseModel):
    type: str = "equation"
    equation: EquationContent


#
# File
#

class FileContent(BaseModel):
    caption: List[RichTextObject]
    file_type: str
    file: Dict[str, Any]
    name: str

class FileBlock(BaseModel):
    type: str = "file"
    file: FileContent


#
# Headings
#

class Heading1Content(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    is_toggleable: bool

class Heading1Block(BaseModel):
    type: str = "heading_1"
    heading_1: Heading1Content

class Heading2Content(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    is_toggleable: bool

class Heading2Block(BaseModel):
    type: str = "heading_2"
    heading_2: Heading2Content

class Heading3Content(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    is_toggleable: bool

class Heading3Block(BaseModel):
    type: str = "heading_3"
    heading_3: Heading3Content


#
# Image
#

class ImageContent(BaseModel):
    image_type: str = "external"
    external: Dict[str, Any] = {"url": ""}

class ImageBlock(BaseModel):
    type: str = "image"
    image: ImageContent = ImageContent()

    def dict(self, **kwargs) -> Dict[str, Any]:
        # print(f"kwargs: {kwargs}")
        data = super().dict(**kwargs)
        # print(f"data: {data}")
        data.pop('type', None)
        data['image'].pop('image_type', None)
        return data



#
# Link Preview
#

class LinkPreviewContent(BaseModel):
    url: str

class LinkPreviewBlock(BaseModel):
    type: str = "link_preview"
    link_preview: LinkPreviewContent


#
# Mention
#

class MentionContent(BaseModel):
    mention: Dict[str, Any]

class MentionBlock(BaseModel):
    type: str = "mention"
    mention: MentionContent


#
# Numbered List
#

class NumberedListItemContent(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    children: Optional[List[Dict[str, Any]]] = None

class NumberedListItemBlock(BaseModel):
    type: str = "numbered_list_item"
    numbered_list_item: NumberedListItemContent


#
# Paragraph
#

class ParagraphContent(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    children: Optional[List[Dict[str, Any]]] = None

class ParagraphBlock(BaseModel):
    type: str = "paragraph"
    paragraph: ParagraphContent


#
# PDF
#

class PDFContent(BaseModel):
    caption: List[RichTextObject]
    pdf_type: str
    external: Dict[str, Any]

class PDFBlock(BaseModel):
    type: str = "pdf"
    pdf: PDFContent


#
# Quote
#

class QuoteContent(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    children: Optional[List[Dict[str, Any]]] = None

class QuoteBlock(BaseModel):
    type: str = "quote"
    quote: QuoteContent


#
# Synced Block
#

class SyncedBlockContent(BaseModel):
    synced_from: Optional[Dict[str, Any]] = None
    children: Optional[List[Dict[str, Any]]] = None

class SyncedBlock(BaseModel):
    type: str = "synced_block"
    synced_block: SyncedBlockContent


#
# Table
#

class TableContent(BaseModel):
    table_width: int
    has_column_header: bool
    has_row_header: bool

class TableBlock(BaseModel):
    type: str = "table"
    table: TableContent

class TableRowContent(BaseModel):
    cells: List[List[RichTextObject]]

class TableRowBlock(BaseModel):
    type: str = "table_row"
    table_row: TableRowContent

class TableOfContentsContent(BaseModel):
    color: str

class TableOfContentsBlock(BaseModel):
    type: str = "table_of_contents"
    table_of_contents: TableOfContentsContent


#
# Template
#

class TemplateContent(BaseModel):
    rich_text: List[RichTextObject]
    children: Optional[List[Dict[str, Any]]] = None

class TemplateBlock(BaseModel):
    type: str = "template"
    template: TemplateContent


#
# Todo
#

class ToDoContent(BaseModel):
    rich_text: List[RichTextObject]
    checked: Optional[bool] = None
    color: str
    children: Optional[List[Dict[str, Any]]] = None

class ToDoBlock(BaseModel):
    type: str = "to_do"
    to_do: ToDoContent


#
# Toggle
#

class ToggleContent(BaseModel):
    rich_text: List[RichTextObject]
    color: str
    children: Optional[List[Any]] = None

