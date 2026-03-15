# Mini Sponsors Feed App 🇬🇧

A production-ready FastAPI application designed to automate the tracking of UK Home Office licensed sponsors. 
The system fetches official datasets daily, parses them, and synchronizes them into a local database to provide a high-performance search API.



## 📂 Project Architecture

The application is organised into a modular structure to ensure a clean separation of concerns:

```text
sponsor-tracker/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── sponsors_route.py  # Fast API Endpoints
│   ├── core/
│   │   └── fetch_parse_csv.py     # CSV parsing logic
│   ├── models/
│   │   └── sqlachemy_model.py     # Database table blueprints
│   ├── repositories/
│   │   └── database_conn.py       # DB connection & Session management
│   ├── services/
│   │   ├── fetch_data_gov.py      # HTTP request logic for gov.uk
│   │   ├── save_to_db.py          # "Upsert" logic (Syncing data)
│   │   └── sponsors_services.py   # Business logic coordination
│   └── main.py                    # Entry point & automated tasks
├── .gitignore                     # Git exclusion rules
├── requirements.txt               # Project dependencies
└── sponsors.db                    # Local SQLite database
```

## ⚖️ Data License & Source
This application utilises public sector information licensed under the Open Government Licence v3.0.<br>
Source: UK Home Office - [Register of licensed sponsors](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers)<br>
Update Frequency: The system is designed to sync daily to stay aligned with the official Home Office update cycle.

## 🛠️ Installation & Setup
1. Environment Configuration<br>
Ensure you are using a virtual environment to manage dependencies correctly:
```Bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```
2. Database Model (Fixing Pylance Errors)<br>
To avoid the reportUndefinedVariable errors in VS Code, ensure your sqlachemy_model.py uses Python objects rather than raw SQL strings:

```Python
from sqlalchemy import Column, Integer, Text, DateTime, UniqueConstraint
from datetime import datetime
from app.repositories.database_conn import Base

class Sponsor(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    organisation_name = Column(Text, nullable=False)
    town_city = Column(Text)
    county = Column(Text)
    type_rating = Column(Text)
    route = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Ensures data integrity across daily syncs
    __table_args__ = (
        UniqueConstraint('organisation_name', 'route', name='_org_route_uc'),
    )
```
3. Running the App<br>
```Bash
uvicorn app.main:app --reload
```
## 👥 Contributors<br>
| Name            | Role               | Responsibility                                                      |
|-----------------|--------------------|---------------------------------------------------------------------|
| SY (SY223)      | Backend Engineer   | FastAPI implementation, SQLAlchemy models, and CSV sync services.   |
| BigJoe (JAE5IVE)| Frontend Engineer  | UI design, search interface, and API consumption logic.             |

## 📜 Credits<br>
We would like to acknowledge the following individuals, organisations, and tools that made this project possible:

- UK Home Office Data Team: For maintaining and providing the public "Register of Licensed Sponsors" dataset.<br>
- The FastAPI Community: For providing an exceptional framework and comprehensive documentation.<br>
- SQLAlchemy Core Team: For the powerful ORM that simplifies database management.<br>
- The Open Source Community: For the libraries and tools that power the internet.<br>
- Project Mentors: For guidance on system architecture and clean code practices.<br>

## 📝 License<br>
© 2026 SY223.<br>
This project is for educational purposes only.<br>
Commercial use, redistribution, or resale is prohibited without written permission to the [Home Office](https://www.gov.uk/)






