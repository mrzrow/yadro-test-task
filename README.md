# Yadro AI Hub Test Task

This API provides functionality for creating short aliases for URLs with an expiration time. Additionally, the API allows retrieving statistics on user clicks for the shortened URLs.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mrzrow/o-complex-test-task.git
   cd yadro-test-task

2. Configure .env file:

   + Rename `.env-template` to `.env`
   + Set the PostgreSQL database URL in the `.env` file under the DB_URL variable. Example:
   ```
   DB_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<db_name>
   ```

3. Setup and run:

   Install dependencies and run the application:
   ```
   make install
   make run
   ```
   **Note**: This Makefile is designed to work on Unix-like systems

The API will be available at: [http://0.0.0.0:8000/](http://0.0.0.0:8000/)

Swagger OpenAPI documentation is available at: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

## Endpoints

### Redirect Endpoints
- **GET /{alias}**  
  Redirects to the original URL using the provided short alias.  
  **Response**: Redirect to the original URL or `404 Not Found` if the alias is invalid or expired.

### URL Management Endpoints
- **GET /url/**  
  Retrieves a list of all shortened URLs. Supports pagination with `offset` and `limit` query parameters.  
  **Response**: List of URLs.

- **POST /url/**  
  Creates a new short URL alias.  
  **Request Body**: `UrlCreateDto` (original URL).  
  **Response**: The created short URL.

- **GET /url/statistics**  
  Retrieves statistics on user clicks for all shortened URLs.  
  **Response**: Sorted list of URLs with click statistics.

- **GET /url/{id}**  
  Retrieves details of a specific URL by its ID.  
  **Response**: URL details or `404 Not Found` if the ID is invalid.

- **GET /url/{id}/short**  
  Retrieves the short alias for a specific URL by its ID.  
  **Response**: Short URL or `404 Not Found` if the ID is invalid.

- **DELETE /url/{id}**  
  Deletes a specific URL by its ID.  
  **Response**: `204 No Content`.
