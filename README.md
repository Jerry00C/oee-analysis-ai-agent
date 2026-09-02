# OEE Analysis AI Agent

This project is a small Python business-intelligence agent for manufacturing data. It combines:

- a LangChain/OpenAI agent that answers natural-language questions
- SQL-backed tools for daily shift, OEE trend, and scrap analysis
- preprocessing scripts that normalize raw CSV exports before they are loaded into a database

The goal is to let a user ask operational questions like:

- What was the OEE on a specific shift date?
- How did OEE trend over a date range?
- Which day had the highest scrap rate?

## Project structure

```text
.
├── agent/
│   ├── agent.py
│   ├── db.py
│   ├── helper.py
│   ├── main.py
│   ├── requirements.txt
│   ├── skills.py
│   └── tools.py
├── preprocess/
│   ├── asset/
│   ├── daliy-shift-schema.json
│   ├── fix_double_divided_percent_columns.py
│   ├── fix_primary_headers.py
│   ├── normalize_daily_shift_numbers.py
│   ├── preprocess.py
│   └── scrap-by-log-schema.json
├── README.md
└── .env (local, not committed)
```

## How it works

### 1. Data preparation
The scripts in `preprocess/` clean and normalize raw CSV exports for daily-shift data so they match the expected database schema.

Typical flow:

- read raw CSVs
- normalize column names and values
- fix malformed percent values
- write cleaned outputs to processed directories

### 2. Database access
The agent reads manufacturing data from a PostgreSQL/Supabase database using the connection code in `agent/db.py`.

It expects an environment variable named `SUPERBASE_URL` in a `.env` file.

### 3. Agent tooling
The agent uses tools defined in `agent/tools.py` to query:

- `daily_shift_metric_tool`
- `oee_trend_tool`
- `top_scrap_day_tool`

Those tools call SQL query functions in `agent/skills.py`.

### 4. User interaction
`agent/main.py` starts a prompt loop and sends the user question to the LangChain agent.

## Setup

### Prerequisites

- Python 3.10+
- Access to a PostgreSQL/Supabase database
- OpenAI API key configured for the LangChain model

### Install dependencies

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r agent/requirements.txt
```

### Configure environment variables
Create a `.env` file in the project root with at least:

```env
SUPERBASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
OPENAI_API_KEY=your_api_key_here
```

The project uses `python-dotenv` to load `.env`, and the database layer reads `SUPERBASE_URL`.

## Running the app

From the project root:

```bash
python agent/main.py
```

The app will prompt:

```text
Ask your business analytics question: 
```

Example questions:

```text
What was the OEE trend from 2021-03-09 to 2021-03-16 for 108 DC 800?
Which day had the highest scrap rate in that range?
What were the daily shift details for 2021-03-16?
```

## Preprocessing scripts

You can run the cleaning scripts individually from the `preprocess` directory or by calling them from Python.

Examples:

```bash
cd preprocess
python preprocess.py
python fix_primary_headers.py
python normalize_daily_shift_numbers.py
python fix_double_divided_percent_columns.py
```

## Notes and caveats

- The database access and agent tools assume the dataset is already loaded into the target table, typically `daily_shift`.
- Some scripts are historical cleanup utilities and may be run only when needed.
- This project is still a prototype and may need runtime validation depending on your database schema and data export format.
- The agent prompt includes a note to use tools when actual OEE data is requested and to avoid inventing numbers.

## Suggested next improvements

- add a real project README with screenshots or example output
- add tests for the query builders and preprocessing logic
- create a proper database migration or schema definition
- add logging and error handling around DB and API failures
- centralize config and avoid hardcoded assumptions in scripts

## License

This project does not currently include a license file. Add one if you intend to share or distribute it publicly.
