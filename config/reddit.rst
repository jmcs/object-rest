URL:http://api.reddit.com

POST /api/login
    Log into an account.
    *rem* specifies whether or not the session cookie returned should last beyond the current
    browser session (that is, if rem is True the cookie will have an explicit expiration far in the
    future indicating that it is not a session cookie).

    +----------+---------------------+
    | api_type | the string json     |
    +----------+---------------------+
    | passwd   | the user's password |
    +----------+---------------------+
    | rem      | boolean value       |
    +----------+---------------------+
    | user     | a username          |
    +----------+---------------------+

GET /api/me.json
    Get info about the currently authenticated user.
    Response includes a modhash, karma, and new mail status.

GET /hot
    +----------+---------------------+
    | after    | fullname of a thing |
    +----------+---------------------+
    | before   | fullname of a thing |
    +----------+---------------------+
    | count    |                     |
    +----------+---------------------+
    | limit    | the maximum number  |
    |          | of items desired    |
    +----------+---------------------+
    | target   |                     |
    +----------+---------------------+
