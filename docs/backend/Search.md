# API Documentation: Search Endpoints

## Overview

This documentation covers the **Search API**, which provides endpoints for retrieving data about charities and events based on user-provided search criteria. Both endpoints support partial matches via SQL's `LIKE` operator.

## Base URL

The base route for this API is `/search`.

---

## Endpoints

### 1. **Search Charities**
- **Route**: `/search/charity`
- **Method**: `GET`
- **Description**: Retrieves a list of charities based on a partial name match. Optionally, you can filter results by category.

#### Request Parameters
| Parameter  | Type   | Required | Description                                |
|------------|--------|----------|--------------------------------------------|
| `name`     | string | Yes      | Partial or full name of the charity to search for. |
| `category` | string | No       | Filter results by category of the charity. |

#### Request Body Example
```json
{
  "name": "help",
  "category": "education"
}


Response

    Success (200): A list of charities matching the search criteria.
    Error (404): No charities found matching the criteria.
    Error (400): Missing name parameter.

Response Body Example (Success):

[
  {
    "id": 1,
    "name": "Helping Hands",
    "address": "123 Charity Lane",
    "description": "A charity for underprivileged children.",
    "category": "education"
  },
  {
    "id": 2,
    "name": "Help the Helpless",
    "address": "456 Kindness Road",
    "description": "Providing aid to those in need.",
    "category": "education"
  }
]


Response Body Example (Error):

{
  "error": "No charities found"
}


2. Search Events

    Route: /search/event
    Method: GET
    Description: Retrieves a list of events based on a partial title match.


#### Request Parameters

| Parameter  | Type   | Required | Description                                |
|------------|--------|----------|--------------------------------------------|
| `title`     | string | Yes      | Partial or full title of the event to search for. |

Request Body Example:

{
  "title": "marathon"
}

Response

-    Success (200): A list of events matching the search criteria.
-    Error (404): No events found matching the criteria.
-    Error (400): Missing title parameter.

Response Body Example (Success)

[
  {
    "id": 1,
    "title": "Charity Marathon",
    "description": "A marathon to raise funds for local charities.",
    "date": "2024-12-15",
    "reward": "Participation medal",
    "charity_id": 101,
    "capacity": 500
  },
  {
    "id": 2,
    "title": "Marathon for Education",
    "description": "Run for a cause and support education for all.",
    "date": "2024-11-20",
    "reward": "Certificate of appreciation",
    "charity_id": 102,
    "capacity": 300
  }
]


Response Body Example (Error)
{
  "error": "No events found"
}


Error Handling
Common Errors

   HTTP             Code	Description
    400	    Missing required request body parameter.
    404	    No results found for the search criteria.



Notes:

    Partial matches for names and titles are case-insensitive.
    Future enhancements (low priority) may include string-matching algorithms to rank results by relevance.