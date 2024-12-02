#                                           Event API Documentation

## Base URL
`/event`

### **Create Events**
- **Endpoint:** `POST /create`
- **Description:** Create multiple events.
- **Request Body:** JSON array of events with the following fields:

| Field         | Type   | Required | Description                   |
|---------------|--------|----------|-------------------------------|
| `eventId`     | String | No       | Unique ID (optional).         |
| `eventName`   | String | Yes      | Name of the event.            |
| `eventRe`     | String | Yes      | Reward for participation.     |
| `eventDesc`   | String | Yes      | Description of the event.     |
| `eventDate`   | String | No       | Date of the event.            |
| `eventCap`    | Int    | Yes      | Capacity of participants.     |
| `charId`      | String | Yes      | Associated charity ID.        |

### **Update Event**
- **Endpoint:** `PUT /update`
- **Description:** Update an event's details.
- **Request Body:** JSON object with the fields:

| Field         | Type   | Required | Description                   |
|---------------|--------|----------|-------------------------------|
| `eventId`     | String | Yes      | Event ID to update.           |
| `eventName`   | String | No       | New name of the event.        |
| `eventRe`     | String | No       | New reward.                   |
| `eventDesc`   | String | No       | New description.              |
| `eventDate`   | String | No       | New date.                     |
| `eventCap`    | Int    | No       | New capacity.                 |
| `charId`      | String | No       | New associated charity ID.    |

### **Delete Event**
- **Endpoint:** `DELETE /delete`
- **Description:** Delete an event.
- **Request Body:** JSON object with the field:

| Field         | Type   | Required | Description                   |
|---------------|--------|----------|-------------------------------|
| `eventId`     | String | Yes      | Event ID to delete.           |
