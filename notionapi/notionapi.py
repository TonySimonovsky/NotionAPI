import requests
import json
from typing import Dict, Any, Optional, get_origin, get_args
from .data import *


class NotionAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.database = DatabaseObject(self)
        self.page = PageObject(self)
        self.page_property = PageProperty(self)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }


class DatabaseObject:
    def __init__(self, api: NotionAPI):
        self.api = api

    def query(self, database_id: str, query: Optional[Dict[str, Any]] = None) -> DatabaseQuery:
        url = f"{self.api.base_url}/databases/{database_id}/query"
        headers = self.api._get_headers()

        response = requests.post(url, headers=headers, json=query or {})
        response.raise_for_status()

        dbq = DatabaseQuery.from_dict(response.json())

        return dbq



class PageObject:
    def __init__(self, api: NotionAPI):
        self.api = api


    def get(self, page_id) -> Page:
        endpoint_url = f"{self.api.base_url}/pages/{page_id}"
        headers = self.api._get_headers()
        response = requests.get(endpoint_url, headers=headers)
        response.raise_for_status()

        # with open('page_example.json', 'w') as file:
        #     json.dump(response.json(), file, indent=4)
        
        # print(f"\n\nresponse.json(): {response.json()}\n\n")
        page = Page.from_dict(response.json())
        # print(f"\n\npage: {page}\n\n")

        return page



    def update(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        page = self.get(page_id=page_id)


        # Update page properties

        for k, v in properties.items():
            # print(f"k, v: {k}, (type: {type(v)}) {v}")


            # if a string value was passed (a way to pass values without complex dict definition)

            if isinstance(v, str):

                # # check the structure required for the property k

                # # print(f"PageObject.update:")
                # # print(f"k: {k}")
                # # print(f"v: {v}")
                # # print(f"-- if isinstance(v, str):")
                # # print(f"---- page.properties[k]: {page.properties[k]}")
                # # print(f"---- type(page.properties[k]): {type(page.properties[k])}")
                # # print(f"---- page.properties[k].default: {page.properties[k].default}")
                # # print(f"---- type(page.properties[k].data): {type(page.properties[k].data)}")


                # print("___111")

                # if the property is a list of values
                if isinstance(page.properties[k], list):
                    # print(f"...isinstance(page.properties[{k}], list): {page.properties[k]}")
                    # print(f"...isinstance(page.properties[{k}].type, list): {page.properties[k].type}\n")
                    if len(page.properties[k]) > 0:
                        for elem in page.properties[k]:
                            # print(f"...elem...: {elem}, {type(elem)}\n")
                            elem.default = v
                            # print(f"...elem...: {elem}, {type(elem)}\n")
                            # print(f"...v...: {v}, {type(v)}\n")
                    else:
                        print(f"...no data in... {k} {page.properties[k]}\n")
                        # setattr(page.properties[k], page.properties[k].type, [page.properties[k].initialize_type(default=v)])
                        # # page.properties[k][page.properties[k].type] = #
                        # print(f"...no data in... {page.properties[k]}\n")
                    
                    # print(f"...page.properties[{k}][0].type: {page.properties[k][0].type}")
                    # print(f"--- k: {k}")
                    # print(f"--- v: {v}")
                    # print(f"--- page.properties[{k}][0]: {page.properties[k][0]}")
                    # print("\n\n")
                    # a = initialize_type(page.properties[k][0].type, default=v)
                    # print(f"\n\n...a: {a}\n\n")

                    # properties[k] = { page.properties[k].type: page.properties[k].dict() }


                # if the property is a single value
                else:
                    try:
                        # print(f"...page.properties[{k}] before: {page.properties[k]}")
                        # print(f"v: {v}")
                        # if page.properties[k].data is None:# and page.properties[k].type == "date":
                        #     page.properties[k] = page.properties[k].initialize_type(default=v)
                        page.properties[k].default = v
                        # print(f"...page.properties[{k}] after: {page.properties[k]}")
                        # print(f"444 ...{k}: {page.properties[k]}")
                    except Exception as e:
                        print(f"Error updating page properties...: {k}, {page.properties[k].data}")
                        return None

                    properties[k] = page.properties[k].dict()


                # print(f"page.properties[k]: {page.properties[k]}")
                # if isinstance(page.properties[k], list):
                #     properties[k] = [elem.dict() for elem in page.properties[k]]
                # else:
                #     properties[k] = page.properties[k].dict()

                # print(f"type(page.properties[k]): {type(page.properties[k])}")
                # print(f"get_origin(page.properties[k]): {get_origin(page.properties[k])}")
                # print(f"get_args(page.properties[k]): {get_args(page.properties[k])}")
                # if isinstance(page.properties[k], list):
                # # if get_origin(page.properties[k]) is list:
                #     print(f"isinstance list... {page.properties[k]}\n")
                #     for elem in page.properties[k]:
                #         print(f".elem:", elem)
                #         elem.default = v
                #         print(f".elem:", elem)
                #         properties[k] = elem.dict()
                # else:
                #     properties[k] = page.properties[k].dict()

                # print(f"...page.properties[k]: {page.properties[k]}")
                # properties[k] = { page.properties[k].type: page.properties[k].dict() }


            # if the property is passed as a properly structured dict

            elif isinstance(v, dict):
                # print(f"PageObject.update:")
                # print(f"-- k: {k}")
                # print(f"-- properties[k]: {properties[k]}")
                # print(f"-- v: {v}")
                # print(f"-- type(v): {type(v)}")
                properties[k] = v


        print(f"properties to pass to update: {properties}")

        # response = requests.patch(url, headers=headers, json=data)
#

        return self.api.page_property.update(page_id, properties)
    






class PageProperty:
    def __init__(self, api: NotionAPI):
        self.api = api

    def update(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:

        print(f"trying to update page {page_id} with properties {properties}")

        url = f"{self.api.base_url}/pages/{page_id}"
        headers = self.api._get_headers()
        data = {
            "properties": {}
        }

        # print(f"properties 1: {properties}\n\n")

        for k,v in properties.items():
            data["properties"][k] = v
            # print(f"...k: {k}")
            # print(f"...v: {v}\n")
            # if isinstance(v, PageProperty):
            #     print(f"...isinstance...: {v}, {type(v)}\n")
            #     data["properties"][k] = v
            # else:
            #     print("kkk\n")
            #     data["properties"][k] = v
            #     # data["properties"][k] = { "rich_text": [ { "text": { "content": v } } ] }

        # print(f"\n...data['properties'] to pass to update: {data['properties']}\n")

        try:
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"updated page {page_id} with properties {properties}\n\n")
            return response.json()

        except Exception as e:
            # print("\n\n",json.dumps(data,indent=4))
            print(f"...Error updating page properties: {e}, {vars(response)}")
            return None

