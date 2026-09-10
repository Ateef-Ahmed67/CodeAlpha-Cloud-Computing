# Task 1 - Data Redundancy Removal System

 **Objective**
A cloud-based system designed to identify and prevent duplicate records from being stored in a cloud database.

**AWS Services Used**
- AWS Lambda
- Amazon DynamoDB
- Amazon API Gateway

**Architecture**
Client → API Gateway → AWS Lambda → DynamoDB

 **How It Works**
1. The client sends a record through the API.
2. API Gateway forwards the request to AWS Lambda.
3. Lambda generates a SHA-256 fingerprint using the record details.
4. DynamoDB checks whether the record already exists.
5. If the record is unique, it is stored in DynamoDB.
6. If the record already exists, the system rejects it as a duplicate.
7. A GET request can retrieve the stored records.

 **Features**
- Duplicate record detection
- SHA-256 based record identification
- Conditional database insertion
- Cloud-based database storage
- REST API access
- HTTP status responses for success and duplicate records
## Testing

 **Unique Record**
Response:
`201 Created`
The record is successfully added.
 **Duplicate Record**
Response:
`409 Conflict`
The duplicate record is rejected and not added to the database.

 **Missing Fields**
Response:
`400 Bad Request`
The request is rejected when required fields are missing.

 **Technologies**
Python, AWS Lambda, Amazon DynamoDB, Amazon API Gateway

 **Internship**
Developed as part of the CodeAlpha Cloud Computing Internship.
