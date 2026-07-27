## Project scope

This project demonstrates local HTML parsing using synthetic test files.

It does not:
- access live onion services
- use Tor
- authenticate to dark-web platforms
- collect real personal information
- make external network requests

## Features

- Parses local HTML files
- Filters pages containing `NV` or `702`
- Extracts synthetic email, username, and phone patterns
- Removes duplicate values
- Exports results to JSONL
- Includes automated tests

## Installation

```bash
python -m pip install -r requirements.txt