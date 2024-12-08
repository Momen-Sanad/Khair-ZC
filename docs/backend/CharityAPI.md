
# Charity API Documentation

## Base URL
`/charity`

### **Create Charities**
- **Endpoint:** `POST /create`
- **Description:** Create multiple charities.
- **Request Body:** JSON array of charities with the following fields:

| Field        | Type   | Required | Description               |
|--------------|--------|----------|---------------------------|
| `charId`     | String | No       | Unique ID (optional).     |
| `charName`   | String | Yes      | Name of the charity.      |
| `charAdd`    | String | Yes      | Address of the charity.   |
| `charDesc`   | String | Yes      | Description.              |
| `charCat`    | String | Yes      | Category.                 |

- **Responses:**
  - **201:** Success, returns created charities.
  - **400:** Error, with message.

Example Request:
```json
[
    {
        "charId": "1",
        "charName": "Helping Hands",
        "charAdd": "Cairo",
        "charDesc": "Assists the needy.",
        "charCat": "Community"
    }
]
```
