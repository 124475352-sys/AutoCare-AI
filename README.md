# AutoCare AI

## Project Overview

AutoCare AI is an intelligent vehicle maintenance assistant developed for IS3329.

The application allows users to select a supported vehicle, choose a maintenance task and receive a maintenance overview alongside verified technical specifications where available.

## Current Features

- Vehicle selection using dependent dropdown menus.
- Vehicle validation against a SQLite database.
- Vehicle-specific maintenance task selection.
- Mock AI-generated maintenance guidance.
- Display of verified technical specifications.
- Safety warnings when specifications are unavailable.
- Automated unit and integration testing.

## Technologies Used

- Python 3.14
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- pytest
- Git and GitHub

## Project Architecture

The application follows a layered modular monolith architecture.

| Component | Responsibility |
|---|---|
| app.py | Flask routes and application controller |
| database.py | Database operations and data storage |
| vehicle_validation.py | Vehicle validation and identification |
| maintenance_data.py | Maintenance tasks and specifications |
| ai_guide.py | AI interface and mock implementation |
| seed_specifications.py | Technical specification data setup |
| templates/ | HTML user interface |
| static/ | CSS styling and JavaScript |
| tests/ | Automated unit and integration tests |

## Installation

Clone the repository:

```bash
git clone https://github.com/124475352-sys/AutoCare-AI.git
cd AutoCare-AI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## Database Setup

Create the database and populate the supported vehicle and maintenance tasks:

```bash
python database.py
```

Populate the technical specifications:

```bash
python seed_specifications.py
```

## Running the Application

```bash
python app.py
```

Open the following address in a web browser:

http://127.0.0.1:5000

## Running the Tests

```bash
python -m pytest -v
```

At the Deliverable 2 development stage, all 48 automated
tests passed, achieving 87% statement coverage across
the five core Python modules.

The Flask application component achieved 98% coverage.

### Code Coverage

To generate a detailed coverage report:

```bash
python -m pytest --cov=app --cov=database --cov=vehicle_validation --cov=maintenance_data --cov=ai_guide --cov-report=term-missing
```

| Component | Coverage |
|---|---:|
| Application | 98% |
| Database | 87% |
| Vehicle validation | 81% |
| AI guide | 74% |
| Maintenance data | 72% |
| Overall | 87% |

Database initialisation and application startup were also
tested manually using a fresh installation from GitHub.


## Supported Vehicle

- Make: Opel
- Model: Astra
- Year: 2015
- Engine: 1.3 CDTI (A13DTE)

Supported maintenance tasks:

- Engine Oil Change
- Air Filter Replacement

## Current Limitations

- The AI component currently uses a mock implementation.
- Vehicle coverage is limited to one vehicle configuration.
- Technical specification coverage is limited.
- The application is intended for local prototype demonstration rather than production use.

## Safety and Data Accuracy

Technical specifications are stored separately from AI-generated guidance. Only specifications marked as verified are displayed.

The application does not replace official manufacturer documentation or professional mechanical advice.

Technical specification references are recorded in sources.md.

## Version Control

Initial development was completed locally in PyCharm. Git version control was introduced during the final stages of Deliverable 2. Earlier development changes were recorded through PyCharm Local History.

## Academic Information

Module: IS3329 Application Architectures and Emerging Technologies

Institution: University College Cork

Academic Year: 2026/2027

Deliverable: 2 - Component Implementation
