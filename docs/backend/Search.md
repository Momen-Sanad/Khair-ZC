#                                               Search API Documentation

## Base URL
`/search`

### **Search Charities**
- **Endpoint:** `GET /search/charity`
- **Description:** Search for charities by name and optionally filter by category.

#### **Request Parameters**
| Parameter   | Type     | Required | Description                          |
|-------------|----------|----------|--------------------------------------|
| `name`      | String   | Yes      | The name (or partial name) of the charity to search for. |
| `category`  | String   | No       | The category to filter the search results. |

#### **Responses**
- **200:** Success, returns a list of charities matching the criteria.
- **400:** Error, missing required data (`name`).
- **404:** Error, no charities found.

#### **Example Request**
```json
{
    "name": "Health",
    "category": "Medical"
}
