# my-phase-3-project
# Health Simplified CLI Application

This is a command-line interface (CLI) application designed to help users track daily food intake, set nutrition goals, and plan weekly meals efficiently.

## Features

- User management: create and list users
- Food entry tracking: add, list, update, and delete food entries
- Nutrition goals: set and list daily and weekly calorie goals
- Reporting: generate reports on progress against goals
- Meal planning: create and update weekly meal plans

## Installation

Install the package using pip:

```
pip install .
```

This will install the `myapp` CLI command.

## Usage

Initialize the database:

```
myapp init
```

Create a user:

```
myapp user create --name "Alice"
```

List users:

```
myapp user list
```

More commands will be added as development progresses.

## Development

- Python 3.x
- SQLAlchemy ORM for database modeling
- Click for CLI parsing
- SQLite backend by default (can be changed to PostgreSQL)

## Testing

Tests are located in the `tests/` directory and can be run with pytest.
