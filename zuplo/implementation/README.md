# Supabase Events API

This is a proof of concept API that fetches event data from a Supabase database. The API is built using Zuplo and provides the following features:

- Fetch events from a Supabase table
- API key authentication
- Pagination support
- Filtering on the `time` column

## Project Structure

```
zuplo/implementation/
├── README.md                   # Setup and usage instructions
├── environment.json            # Environment variables configuration
├── package.json                # Project dependencies
├── policies.json               # API key authentication policy
├── routes.json                 # API route configuration
├── supabase-setup.sql          # SQL setup script for Supabase
├── tsconfig.json               # TypeScript configuration
└── modules/
    └── events-handler.ts       # API endpoint implementation
```

## Key Components

1. **Supabase Integration**
   - SQL setup script for creating the events table and sample data
   - Integration with the Supabase JavaScript client for data fetching
   - Uses Supabase anon key with Row Level Security for secure data access

2. **Zuplo API Configuration**
   - API key authentication using Zuplo's built-in policies
   - Route configuration for the `/api/events` endpoint
   - Environment variable setup for Supabase credentials

3. **API Features**
   - Pagination using `limit` and `offset` parameters
   - Filtering on the `time` column using `start_time` and `end_time` parameters
   - Proper error handling and response formatting

## Setup Instructions

### 1. Supabase Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Navigate to the SQL Editor in your Supabase dashboard
3. Run the SQL commands in `supabase-setup.sql` to create the necessary table and sample data
4. From your Supabase dashboard, get your:
   - Project URL (e.g., `https://abcdefghijklm.supabase.co`)
   - Anon/Public Key (from API settings)

### 2. Zuplo Setup

1. Create a Zuplo account at [zuplo.com](https://zuplo.com)
2. Create a new project
3. Upload the files from this implementation to your Zuplo project
4. Update the `environment.json` file with your Supabase URL and Anon Key
5. Deploy your API

### 3. Create API Keys

1. In your Zuplo dashboard, navigate to the API Keys section
2. Create a new API key for testing
3. Note the API key for use in API requests

## Using the API

### Endpoint

```
GET /api/events
```

### Query Parameters

- `limit` (optional): Number of records to return (default: 10, max: 100)
- `offset` (optional): Number of records to skip (default: 0)
- `start_time` (optional): Filter events after this time (ISO format)
- `end_time` (optional): Filter events before this time (ISO format)

### Authentication

Include your API key in the request header:

```
x-api-key: YOUR_API_KEY
```

Alternatively, you can include it as a query parameter:

```
?api_key=YOUR_API_KEY
```

### Example Requests

#### Basic Request

```bash
curl -X GET "https://your-project.zuplo.app/api/events" \
  -H "x-api-key: your-api-key"
```

#### With Pagination

```bash
curl -X GET "https://your-project.zuplo.app/api/events?limit=5&offset=10" \
  -H "x-api-key: your-api-key"
```

#### With Time Filtering

```bash
curl -X GET "https://your-project.zuplo.app/api/events?start_time=2025-01-01&end_time=2025-01-02" \
  -H "x-api-key: your-api-key"
```

### Response Format

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "events": [
      {
        "time": "2025-01-01 10:00:00",
        "event_id": "123"
      },
      {
        "time": "2025-01-01 11:00:00",
        "event_id": "124"
      }
      // more events...
    ]
  }
}
```

## Error Handling

The API returns appropriate error responses with the following format:

```json
{
  "status": "error",
  "code": 400, // HTTP status code
  "message": "Error message"
}
```

Common error codes:
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid API key)
- 500: Internal Server Error
