import SparkApi
import json
#以下密钥信息从控制台获取
appid = "f2d5e626"     #填写控制台中获取的 APPID 信息
api_secret = "NzI2ZWZhNWQ1ZDU0M2U0NzJlNzgwYTAw"   #填写控制台中获取的 APISecret 信息
api_key ="7795760a804419dac26a9133f318c0bf"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
def AIanswer(Input):
    question = checklen(getText("user",Input+",20字节以内回答我"))
    SparkApi.answer =""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    getText("assistant",SparkApi.answer)
    ans = SparkApi.answer
    return ans


