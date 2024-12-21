#                                            Registration API documentation

registration_md_content = """
# Registration API Documentation

## Base URL
`/registration`

### **Register User for Event**
- **Endpoint:** `POST /register`
- **Description:** Register an authenticated user for an event.

- **Request Body:** JSON object with the following fields:

| Field          | Type    | Required | Description                          |
|----------------|---------|----------|--------------------------------------|
| `event_id`     | Integer | Yes      | ID of the event to register for.     |
| `current_id`   | Integer | Yes      | ID of the current user.              |

- **Responses:**
  - **201:** Success, user registered for the event.
  - **400:** Error, missing event ID, user already registered, or event capacity reached.
  - **404:** Error, event not found.

- **Authorization:** Requires user authentication (via token).

Example Request:
```json
{
    "event_id": 123,
    "current_id": 456
}
