import time
from idlelib.iomenu import encoding

import requests
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, UnstructuredMarkdownLoader


# 加载docx
# docs = UnstructuredWordDocumentLoader(file_path="./assets/sample.docx", mode="single").load()
# print(docs.__sizeof__())
#
# for doc in docs[0:10]:
#     print(doc.page_content)
#     print(doc.metadata)

# 加载markdown
# docs2 = UnstructuredMarkdownLoader(file_path="./assets/sample.md", mode="elements", encoding="utf-8").load()
#
# for doc in docs2:
#     print(doc.page_content)
#     print(doc.metadata)


# 加载pdf

def mineru_upload_file_demo():

    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI5MzAwMDExNSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3OTYyMjY5NSwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNjY5ZTU4ZGEtYzZkYi00ZjExLTlmYmEtNzBmMzNkMDRjN2JmIiwiZW1haWwiOiIiLCJleHAiOjE3ODczOTg2OTV9.BSFCvembducGDULBjR7GhJqb7huw_svrzKWLYxSR9ev7q77k5gSdQ_3tdwjpyjceji0CpsCZjlL-7RT2Y1Bacg"
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name": "sample.pdf", "data_id": "abcd"}
        ],
        "model_version": "vlm"
    }
    file_path = [r"/Users/wangbowei/PycharmProjects/langchain_study/retrieval/assets/sample.pdf"]
    try:
        response = requests.post(url, headers=header, json=data)
        if response.status_code == 200:
            result = response.json()
            print('response success. result:{}'.format(result))
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):
                    with open(file_path[i], 'rb') as f:
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} upload success")
                        else:
                            print(f"{urls[i]} upload failed")
            else:
                print('apply upload url failed,reason:{}'.format(result["msg"]))
        else:
            print('response not success. status:{} ,result:{}'.format(response.status_code, response))
        return batch_id
    except Exception as err:
        print(err)

def mineru_check_result_demo(batch_id:str)->str:
    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI5MzAwMDExNSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3OTYyMjY5NSwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiNjY5ZTU4ZGEtYzZkYi00ZjExLTlmYmEtNzBmMzNkMDRjN2JmIiwiZW1haWwiOiIiLCJleHAiOjE3ODczOTg2OTV9.BSFCvembducGDULBjR7GhJqb7huw_svrzKWLYxSR9ev7q77k5gSdQ_3tdwjpyjceji0CpsCZjlL-7RT2Y1Bacg"
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(url, headers=header)
    print(res.json())
    print(res.status_code)
    while res.json()["data"]['extract_result'][0]['state'] != 'done':
        print('当前状态为running，等待3秒后重试')
        time.sleep(3)
        res = requests.get(url, headers=header)
        print(res.status_code)
        print(res.json()["data"]['extract_result'][0]['state'], end="\n\n=========\n\n")
        print('提取结果为:', res.json()["data"]['extract_result'][0]['full_zip_url'])


if __name__ == '__main__':
    batch_id = mineru_upload_file_demo()
    mineru_check_result_demo(batch_id)
