import json


def SendJsonResponse(resultDict):
    print("Convert Python dictionary into JSON formatted String")
    developer_str = json.dumps(resultDict)
    print(developer_str)


# sample developer dict
developer_Dict = {
    "name": "Jane Doe",
    "salary": 9000,
    "skills": ["Python", "Machine Learning", "Web Development"],
    "email": "jane.doe@pynative.com",
}
SendJsonResponse(developer_Dict)
