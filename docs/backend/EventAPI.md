#                                            **Event Management API**

This API allows administrators to manage events for a charity platform. It includes endpoints for creating, updating, and deleting events.

## **Base URL**
The base URL for all endpoints in this documentation is determined by the application where this `Blueprint` is registered.

---

## **Endpoints**

### 1. **Create Events**

**Endpoint**: `/create`  
**Method**: `POST`

**Description**: Allows admins to create new events associated with charities.

#### **Request**

**Headers**:
- Content-Type: `application/json`

**Body**:
```json
[
  {
    "userId": "int",
    "eventId": "int",
    "eventName": "string",
    "eventRe": "string",
    "eventDesc": "string",
    "eventDate": "string (YYYY-MM-DD format)",
    "eventCap": "int",
    "charId": "int"
  }
]
\`\`\`

**Response**
- **201 Created**:
```json
  {
    "message": "Events created successfully",
    "events": [
      {
        "eventId": "int",
        "eventName": "string"
      }
    ]
  }
  \`\`\`
- **400 Bad Request**:
  - Invalid input or missing required fields.
- **403 Forbidden**:
  - Only admins can create events.
- **400 Bad Request**:
  - Event already exists or charity ID not found.

---

### 2. **Update Events**

**Endpoint**: `/update`  
**Method**: `PUT`

**Description**: Allows admins to update existing event details.

#### **Request**

**Headers**:
- Content-Type: `application/json`

**Body**:
```json
{
  "userId": "int",
  "eventId": "int",
  "eventName": "string (optional)",
  "eventRe": "string (optional)",
  "eventDesc": "string (optional)",
  "eventDate": "string (YYYY-MM-DD, optional)",
  "eventCap": "int (optional)",
  "charId": "int (optional)"
}
\`\`\`

**Response**
- **200 OK**:
  \`\`\`json
  {
    "message": "Event updated successfully"
  }
  \`\`\`
- **400 Bad Request**:
  - Missing event ID.
- **403 Forbidden**:
  - Only admins can update events.
- **404 Not Found**:
  - Event or charity not found.

---

### 3. **Delete Events**

**Endpoint**: `/delete`  
**Method**: `DELETE`

**Description**: Allows admins to delete events.

#### **Request**

**Headers**:
- Content-Type: `application/json`

**Body**:
\`\`\`json
{
  "userId": "int",
  "eventId": "int"
}
\`\`\`

**Response**
- **200 OK**:
  \`\`\`json
  {
    "message": "Event deleted successfully"
  }
  \`\`\`
- **400 Bad Request**:
  - Missing event ID.
- **403 Forbidden**:
  - Only admins can delete events.
- **404 Not Found**:
  - Event not found.

---

## **Models**

### **Event**
- `id`: `int` (Primary key, unique identifier for the event)
- `title`: `string` (Name of the event)
- `reward`: `string` (Description of the reward for participation)
- `description`: `string` (Details of the event)
- `charity_id`: `int` (Foreign key linked to a charity)
- `date`: `string` (Date of the event)
- `capacity`: `int` (Maximum number of participants)

---

### **Charity**
- `id`: `int` (Primary key, unique identifier for the charity)

---

### **User**
- `id`: `int` (Primary key, unique identifier for the user)
- `is_admin`: `boolean` (Indicates if the user is an admin)

---

### **Notes**
- Ensure the user calling the endpoints has admin privileges.
- The `eventName` should be unique to prevent duplicate event creation.
- Use the proper JSON format for requests to avoid `400 Bad Request` responses.
