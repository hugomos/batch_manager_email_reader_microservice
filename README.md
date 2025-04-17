### Batch Manager Email Reader

Batch Manager Email Reader is a Python microservice that reads emails from an IMAP server and returns the emails in a JSON format.

## Usage

To use Batch Manager Email Reader, you need to set the following environment variables:

- `IMAP_SERVER`: The IMAP server to connect to.
- `IMAP_PORT`: The port to connect to the IMAP server on.
- `IMAP_USER`: The username to use to connect to the IMAP server.
- `IMAP_PASSWORD`: The password to use to connect to the IMAP server.
- `AUTH_API_URL`: The URL of the authentication API.

Once the environment variables are set, you can run the microservice using the following command:

```bash
docker-compose up --build
```

The microservice will run on port 5000 and will return the emails in a JSON format.

## Example

```json
[
  {
    "code": "1234",
    "received_at": "2021-01-01 00:00:00"
  },
  ...
]
```

## Authentication

The microservice uses the authentication API to check if the user is authenticated. If the user is not authenticated, the microservice will return a 401 status code.

## Author

[Vitor Hugo Oliveira](https://github.com/hugomos)
