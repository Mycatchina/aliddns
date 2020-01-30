#!/usr/bin/python3
import json
from json import load
from urllib.request import urlopen
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import datetime
i = str(datetime.datetime.now())
newip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
AccessKey_ID = '#必填#'
Access_Key_Secret = '#必填#'
region_id = "cn-shenzhenI#看情况#"
DomainName = '域名'
RR = '二级域名头部，如：www'
DomainType = 'A'
UpdateDomain = 'Auto_Lines'
def AliAccessKey(id,Secret,region):
        client = AcsClient(id, Secret, region)
        return client
def GetDNSRecordId(client,DomainName):
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        for RecordId in json_data['DomainRecords']['Record']:
            if RR == RecordId['RR']:
                return RecordId['RecordId']
def UpdateDomainRecord(client,RecordId):
    try:
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_Value(newip)
        request.set_Type(DomainType)
        request.set_RR(RR)
        request.set_RecordId(RecordId)
        client.do_action_with_exception(request)
        print("域名:" + DomainName + " 主机:" + RR + " 记录类型:" +  DomainType + " 记录值:" +  newip)
    except Exception as e:
        print(i + '    DNS已经更新')
def main():
    client = AliAccessKey(AccessKey_ID,Access_Key_Secret,region_id)
    RecordId = GetDNSRecordId(client,DomainName)
    UpdateDomainRecord(client,RecordId)
if __name__ == "__main__" :
    main()
