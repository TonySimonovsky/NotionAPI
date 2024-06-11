import requests, json, os
from notionapi import *
from notionapi.blocks import *

notion = NotionAPI(token=os.environ["NOTION_TOKEN"])

page_id = "e6629dea583c42f3ac32625013620c7f"


"""
Getting Notion page.
"""
page = notion.page.get(page_id=page_id)
print("\n\n")
print("type(page):",type(page))
print("page:",page)


"""
Updating Notion page.
"""
notion.page.update(
    page_id=page_id,
    properties={
        "last update": "2024-06-18",
        "description": "...sdsdsds"
    }
)


"""
Getting Notion page blocks.
"""
page_api = PageAPI(api=notion, page_id="e6629dea583c42f3ac32625013620c7f")
blocks = page_api.block.get()
print("\n\n")
print(blocks)


"""
Appending Notion page blocks.
"""
block_api = BlockAPI(api=notion)
children_blocks = [
    # you can use a simplified version to set the main value
    ImageBlock(image_url="https://storage.screenshotapi.net/github_com_sugarforever_chat_ollama_6abbd1d190b7.png")
    # or you can use more complex version to have more control
    # ImageBlock(
    #     image=ImageContent(
    #         external = { "url": "https://storage.screenshotapi.net/github_com_sugarforever_chat_ollama_6abbd1d190b7.png" }
    #     )
    # )
]
appended_blocks = block_api.append(block_id=page_id, children=children_blocks)
