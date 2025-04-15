# BeanThere
App to review and track Coffees bought at Cafes, like Vivino and TripAdvisor combined


  ## Project Outliner and Intended Features

- Basic API
  - Coffee Review Creation (Complete)
  - Basic User Account Creation (Complete)
  - Creation and allocation of user tokens
  - Review ownership based on use token

- Other Backend
  - Cafe Scraping

- Frontend
  - Login and Account Creation Page
  - Recent Reviews Page

  ## Technology Stack and Features

-  [**FastAPI**](https://fastapi.tiangolo.com) Python backend API.
    -  [SQLAlchemy](https://www.sqlalchemy.org/) Python SQL database interactions (ORM).
    -  [Pydantic](https://docs.pydantic.dev), for the data validation.
    -  [MySQL](https://www.mysql.com/) as the SQL database.
-  [Kotlin](https://kotlinlang.org/) for the Android frontend.
    -  Might migrate to flutter to allow simultaneous development for Android and IOS
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default. (bcrypt)
- 🔑 JWT (JSON Web Token) authentication. OR 
-  Tests with [Pytest](https://pytest.org).