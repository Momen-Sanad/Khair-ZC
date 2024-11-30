
# Auth API Documentation

## Base URL
`/auth`

### **Register User**
- **Endpoint:** `POST /register`
- **Description:** Register a new user.
- **Request Body:** JSON object with the following fields:

| Field         | Type    | Required | Description                        |
|---------------|---------|----------|------------------------------------|
| `id`          | String  | Yes      | Unique ID for the user.            |
| `fname`       | String  | Yes      | First name of the user.            |
| `lname`       | String  | Yes      | Last name of the user.             |
| `userPass`    | String  | Yes      | User's password.                   |
| `email`       | String  | Yes      | User's email address.              |

- **Responses:**
  - **201:** Success, user registered (as Zewailian or Guest).
  - **400:** Error, missing data or email already registered.

Example Request:
```json
{
    "id": "123",
    "fname": "momen",
    "lname": "mahmoud",
    "userPass": "S3cUr3pa$$w0rd",
    "email": "s-xyz.abc@zewailcity.edu.eg"
}
```

### **Login User**
- **Endpoint:** `POST /login`
- **Description:** Log in an existing user.
- **Request Body:** JSON object with the following fields:

| Field         | Type    | Required | Description                        |
|---------------|---------|----------|------------------------------------|
| `email`       | String  | Yes      | User's email address.              |
| `userPass`    | String  | Yes      | User's password.                   |

- **Responses:**
  - **200:** Success, login successful with a token.
  - **404:** Error, user not found.
  - **401:** Error, invalid credentials.

Example Request:
```json
{
    "email": "s-xyz.abc@zewailcity.edu.eg",
    "userPass": "S3cUr3pa$$w0rd"
}
```
  
### **Token Required Middleware**
- **Description:** Middleware to verify user tokens.

- **Header:** `x-access-token`

- **Responses:**
  - **403:** Token is missing or invalid.
