# Solar Website Factory ☀️🏭

A simple, robust, and highly scalable website compilation system designed to generate hundreds of personalized outreach websites for local Indian solar businesses daily with **0 AI token cost** during generation.

---

## Architecture Overview

The system compiles website configurations deterministically using a single-page, highly optimized HTML/CSS template and a date-based workflow:

```
Lead (CSV) -> Research & Enrichment -> business.json -> Website Compiler -> index.html
```

- **Unique Directory Isolation**: Each business is assigned a unique ID `SLR-YYYYMMDD-XXX` and gets a dedicated directory containing:
  - `business.json`: Enriched business configurations (copywriting, custom branding, solar statistics).
  - `index.html`: Compiled static landing page (ready for clean static web hosting).
  - `metadata.json`: Lifecycle metadata and audit logs.
- **Global Search Index**: Maintains a lightweight, flat key-value dictionary (`data/index.json`) for instant business lookups and search matching.

---

## Installation

1. Clone or download the repository to your environment.
2. Install Python 3.9+ (if not already installed).
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Batch Pipeline

Every day's outreach is treated as a separate batch. 

### 1. Place the Lead CSV
Create a date directory in the `data/` folder and place a `leads.csv` in a subfolder named `leads`. For example:
`data/2026-06-03/leads/leads.csv`

### 2. CSV Schema Format
Ensure your `leads.csv` has the following column headers:
- `Business Name` (Required - e.g. `Sharma Solar Solutions`)
- `Owner Name` (e.g. `Rajesh Sharma`)
- `Phone` (e.g. `+91 98765 43210`)
- `Email` (e.g. `contact@sharmasolar.in`)
- `City` (e.g. `Jaipur`)
- `State` (e.g. `Rajasthan`)
- `Address` (e.g. `12, Malviya Nagar, Jaipur, Rajasthan 302017`)
- `WhatsApp` (Optional - defaults to `Phone` if empty)
- `Average Monthly Bill INR` (Optional - defaults to `6000` if empty)
- `Primary Color` (Optional - hex code for primary brand color, e.g. `#0284c7`)
- `Secondary Color` (Optional - hex code for secondary color, e.g. `#ea580c`)
- `Accent Color` (Optional - hex code for accent color, e.g. `#16a34a`)

### 3. Run the Orchestrator
Execute the pipeline script specifying the target batch date:
```bash
python src/pipeline.py --date 2026-06-03
```
If you omit the `--date` parameter, the system will automatically run for today's date.

---

## Administrative CLI (`src/manage.py`)

A management utility tool is provided to search the global registry and trigger website regenerations.

### 1. Search the Index
Search for any business ID, name, city, state, or status:
```bash
python src/manage.py search "Jaipur"
```

### 2. Regenerate a Single Website
Rebuild the static HTML website for a specific business ID using its existing `business.json` (e.g. if the master HTML template or CSS files change):
```bash
python src/manage.py compile --id SLR-20260603-001
```

### 3. Regenerate an Entire Batch
Re-compile all static HTML websites for all business records registered under a specific batch date:
```bash
python src/manage.py compile --date 2026-06-03
```

All compilation actions performed through the CLI are automatically appended to the target business's audit logs inside its `metadata.json` history trail.
