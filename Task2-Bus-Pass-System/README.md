# Task 3 - Cloud-Based Bus Pass System

 **Objective**

A cloud-based bus pass booking system that allows users to book bus passes online while providing reliable cloud storage and preventing duplicate bookings and incorrect pricing.

 **AWS Services Used**

- AWS Lambda
- Amazon DynamoDB
- Amazon API Gateway

 **Architecture**

Client → API Gateway → AWS Lambda → DynamoDB

 **How It Works**

1. The user sends bus pass booking details through the API.
2. API Gateway receives the request and forwards it to AWS Lambda.
3. Lambda validates the booking information.
4. The system calculates the bus pass price based on the selected pass type.
5. A unique BookingId is generated using SHA-256.
6. DynamoDB stores the confirmed booking.
7. Duplicate bookings are detected and rejected.
8. GET requests can retrieve stored bookings.

 **Pass Types and Pricing**

| Pass Type | Price |
|-----------|-------|
| Daily | ₹50 |
| Weekly | ₹250 |
| Monthly | ₹800 |

 **Features**

- Online bus pass booking
- Cloud-based database storage
- Automatic price calculation
- Duplicate booking prevention
- Unique booking identification
- Booking status tracking
- REST API access
- GET API for retrieving bookings
- Serverless AWS Lambda architecture

 **Testing**

 **Successful Booking**

Response:

`201 Created`

The bus pass is successfully booked and stored in DynamoDB.

 **Duplicate Booking**

Response:

`409 Conflict`

The duplicate booking is rejected.

 **Invalid Pass Type**

Response:

`400 Bad Request`

The request is rejected when an unsupported pass type is provided.

 **GET Bookings**

Response:

`200 OK`

Returns the stored bus pass bookings.

 **Technologies**

Python, AWS Lambda, Amazon DynamoDB, Amazon API Gateway

 **Scalability**

The system uses AWS Lambda and API Gateway as a serverless architecture, allowing the application to handle varying levels of incoming requests without manually managing servers.

 **Internship**

Developed as part of the CodeAlpha Cloud Computing Internship.
