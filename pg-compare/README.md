# pg-compare-cline

A Python tool for PostgreSQL database operations.

1. enums
2. extensions
3. roles
4. policies

## Features

- Connect to PostgreSQL databases using service connections defined in pg_service.conf
- List non-system tables from PostgreSQL databases
- Compare database objects between two PostgreSQL databases to identify mismatches:
  - Tables
  - Views
  - Functions
  - Indices
  - Triggers
  - Row Level Security Policies
  - Table Columns (data types, descriptions, constraints, foreign keys)
  - Table Privileges (grants to users)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pg-compare-cline.git
cd pg-compare-cline

# Install using Poetry
poetry install
```

## Usage

### List Non-System Tables

To list all non-system tables in a PostgreSQL database:

```bash
# Using the installed script
poetry run list-tables <service_name>

# Or run the script directly
./pg_compare_cline/list_tables.py <service_name>
```

Where `<service_name>` is the name of a service defined in your pg_service.conf file.

### Compare Tables Between Databases

To compare tables between two PostgreSQL databases and find mismatches:

```bash
# Using the installed script
poetry run compare-tables <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_tables.py <service_name1> <service_name2>
```

This will:
1. Connect to both databases using the specified service names
2. Retrieve the list of non-system tables from each database
3. Compare the lists to find tables that exist in one database but not in the other
4. Display the results in a formatted table

### Compare Views Between Databases

To compare views between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-views <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_views.py <service_name1> <service_name2>
```

### Compare Functions Between Databases

To compare functions between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-functions <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_functions.py <service_name1> <service_name2>
```

The function comparison includes function names and their argument types to properly identify functions with the same name but different signatures.

### Compare Indices Between Databases

To compare indices between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-indices <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_indices.py <service_name1> <service_name2>
```

The output includes the full index definition to help understand differences between indices.

### Compare Triggers Between Databases

To compare triggers between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-triggers <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_triggers.py <service_name1> <service_name2>
```

### Compare Row Level Security Policies Between Databases

To compare row level security policies between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-policies <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_policies.py <service_name1> <service_name2>
```

The output includes the policy definitions with USING and WITH CHECK clauses.

### Compare Table Columns Between Databases

To compare table columns between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-columns <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_columns.py <service_name1> <service_name2>
```

This script identifies mismatches in:
- Missing columns (columns that exist in one database but not the other)
- Data type differences
- Column descriptions/comments
- NOT NULL constraints
- Default values
- Foreign key references

### Compare Table Privileges Between Databases

To compare table privileges (grants) between two PostgreSQL databases:

```bash
# Using the installed script
poetry run compare-privileges <service_name1> <service_name2>

# Or run the script directly
./pg_compare_cline/compare_privileges.py <service_name1> <service_name2>
```

This script identifies:
- Privileges that exist in one database but not in the other
- Privileges that exist in both databases but with different settings

## PostgreSQL Service Configuration

This tool uses the PostgreSQL service configuration file (`pg_service.conf`) to connect to databases. This file allows you to define connection parameters under a service name.

### Location of pg_service.conf

The file can be located in:
- `~/.pg_service.conf` (user's home directory)
- The location specified by the `PGSERVICEFILE` environment variable
- `/etc/pg_service.conf` (system-wide configuration)

### Example pg_service.conf

```
[my_database]
host=localhost
port=5432
dbname=my_database_name
user=my_username
password=my_password
```

Then you can use:

```bash
poetry run list-tables my_database
```

## License

[MIT](LICENSE)