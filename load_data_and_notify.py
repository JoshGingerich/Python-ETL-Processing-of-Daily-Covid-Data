import json
import pandas as pd
import extract
import boto3
import os

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table(os.environ['dbtab'])

sns = boto3.resource("sns")
topic = sns.Topic(arn=os.environ['topic'])

def lambda_handler(event, context):
    #grabs the df using the extraction function and the urls containing the data
    try:
        df = extract.extract_and_merge(os.environ['nyurl'],os.environ['jhurl'])
        dflength = len(df)
    except:
        alert(topic,'Error: Data did not Load')
        
    
    
    #Grabs the list of items that may already be in the dynamodb table
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    #grabs the lengths and the difference to determine what should be done to the table
    dflength = len(df)
    tablelength = len(data)
    diff = dflength - tablelength
    print(f"old data had {tablelength} rows of data")
    print(f"new data has {dflength} rows of data")
    
    if tablelength == 0:
        #Adds data to the table for the first time if it is empty
        for index, row in df.iterrows():
            items = {'date':row[0],'cases':row[1],'deaths':row[2],'Recovered':row[3]}
            table.put_item(Item=items)
        mess1 = f"The table has added data for the first time. {dflength} rows inserted."
        alert(topic,mess1)
    elif diff >= 1:
        #If table already has data, updates all missing rows of data so that it is current
        ndf = df[df.index >= tablelength]
        for index, row in ndf.iterrows():
            items = {'date':row[0],'cases':row[1],'deaths':row[2],'Recovered':row[3]}
            table.put_item(Item=items)
        mess2 = f"{diff} row(s) of data added. \n Last Row Added: {items}"
        alert(topic,mess2)
    else:
        #The table already has the most up to date data
        mess3 = 'Already up to date!'
        alert(topic,mess3)
        
def alert(top, message):
    response = top.publish(Message=message)
    m = response['MessageId']
    return m
