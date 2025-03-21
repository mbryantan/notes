# Project Brief

## Overview
Proof of concept to build an API that will return data from a supabase table or function in this format:

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
      // more events...
    ]
  }
}
```

## Core Features
- Fetch data from a supabase tables or function via Supabase Data API
- API key authentication using Zuplo
- API supports pagination
- API supports filtering on `time` column

## Target Users
- User will run fetch data from API

## Technical Preferences
- Technologies: Supabase, Zuplo, Buildship (if required)
- Constraints: I don't have Zuplo and Builship knowledge

## Implementation

The implementation for this project is available in the `zuplo/implementation` directory. It includes:

### Supabase Integration
- Uses the Supabase JavaScript client to fetch data from a Supabase table
- SQL setup script for creating the necessary table and sample data
- Uses Supabase anon key with Row Level Security for secure data access
- Proper error handling for database queries

### Zuplo API Configuration
- API key authentication using Zuplo's built-in policies
- Route configuration for the `/api/events` endpoint
- Environment variable setup for Supabase credentials

### API Features
- Pagination using `limit` and `offset` parameters
- Filtering on the `time` column using `start_time` and `end_time` parameters
- Proper error handling and response formatting

### Documentation
- Comprehensive README with setup instructions
- Example API requests and response formats
- Error handling documentation

## Getting Started

See the `zuplo/implementation/README.md` file for detailed setup and usage instructions.
