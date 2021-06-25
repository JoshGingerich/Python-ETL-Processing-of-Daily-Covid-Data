# Python-ETL-Processing-of-Daily-Covid-Data
Event-Driven processing pipeline utilizing python and AWS services such as Lambda, CloudWatch events, SNS, DynamoDB, and Quicksight.

Data was gathered from two sources:
NYT: https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv
John Hopkins: https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv

![githubetlviz](https://user-images.githubusercontent.com/61246608/123479651-de9cf000-d5c6-11eb-9951-349c7db18f5a.jpg)

Simple data visualization with AWS Quicksight:

![Screen Shot 2021-06-25 at 3 12 23 PM](https://user-images.githubusercontent.com/61246608/123480378-e4470580-d5c7-11eb-9c71-a850fc1d4686.png)


Improvements:

The primary way I plan on improving this project is to implement IaC by using CloudFormation to coordinate all of these services together and deploy them at the same time.

Reflecting on the architecture of this project, it is clear to me that while DynamoDB is very simple to use and low cost (which was certainly a consideration for this project), it should primarly be used as a transactional database rather than for data visualization. I realized this the hard way because there is no native DynamoDB support in Quicksight and I had to implement a time consuming workaround by importing the DynamoDB table as JSON to an S3 bucket first.
