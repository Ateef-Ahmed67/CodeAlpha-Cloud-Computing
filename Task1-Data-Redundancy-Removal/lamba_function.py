import json
import boto3
import hashlib
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("BusPassBookings")

PRICES = {
    "daily": 50,
    "weekly": 250,
    "monthly": 800
}


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body, default=float)
    }


def lambda_handler(event, context):

    try:
        method = event.get("httpMethod", "POST")

        if method == "GET":
            result = table.scan()

            return response(200, {
                "message": "Bookings retrieved successfully",
                "bookings": result.get("Items", [])
            })

        if method != "POST":
            return response(405, {
                "message": "Method not allowed"
            })

        body = event.get("body") or event

        if isinstance(body, str):
            body = json.loads(body)

        required_fields = [
            "name",
            "email",
            "route",
            "travel_date",
            "pass_type"
        ]

        missing = [
            field
            for field in required_fields
            if not body.get(field)
        ]

        if missing:
            return response(400, {
                "message": "Missing required fields",
                "fields": missing
            })

        name = body["name"].strip()
        email = body["email"].strip().lower()
        route = body["route"].strip()
        travel_date = body["travel_date"].strip()
        pass_type = body["pass_type"].strip().lower()

        if pass_type not in PRICES:
            return response(400, {
                "message": "Invalid pass type",
                "allowed_pass_types": list(PRICES.keys())
            })

        try:
            quantity = int(body.get("quantity", 1))
        except (TypeError, ValueError):
            return response(400, {
                "message": "Quantity must be a number"
            })

        if quantity < 1 or quantity > 10:
            return response(400, {
                "message": "Quantity must be between 1 and 10"
            })

        unit_price = PRICES[pass_type]
        total_price = unit_price * quantity

        booking_data = (
            f"{email}|"
            f"{route.lower()}|"
            f"{travel_date}|"
            f"{pass_type}|"
            f"{quantity}"
        )

        booking_id = hashlib.sha256(
            booking_data.encode("utf-8")
        ).hexdigest()

        item = {
            "BookingId": booking_id,
            "name": name,
            "email": email,
            "route": route,
            "travel_date": travel_date,
            "pass_type": pass_type,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price,
            "status": "CONFIRMED",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        try:
            table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(BookingId)"
            )

        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return response(409, {
                "message": "Duplicate booking detected",
                "BookingId": booking_id
            })

        return response(201, {
            "message": "Bus pass booked successfully",
            "booking": item
        })

    except Exception as e:
        return response(500, {
            "message": "Internal server error",
            "error": str(e)
        })
