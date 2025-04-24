# BeanThere

Welcome to **BeanThere**, your personal coffee companion! Inspired by platforms like Vivino and TripAdvisor, BeanThere lets users review, track, and discover coffees at local cafes. Whether you're a casual sipper or a seasoned aficionado, BeanThere helps you build your taste profile and find the brews you'll love most.

## Project Overview

BeanThere is a full-stack application designed to help users log and rate their coffee experiences. It features a modern API backend built with FastAPI and an admittedly incomplete mobile frontend developed in Kotlin (with plans for Flutter), offering smooth and secure interactions. From tracking flavor preferences to discovering the best-rated cafes nearby, BeanThere puts your coffee journey front and center.

## Features

### ✅ Backend Features

- **Review System**: Create, update, and manage coffee reviews.
- **User Accounts**: Sign-up and login functionality with secure authentication.
- **Token-Based Ownership**: Assign reviews to users via JWTs.
- **Cafe Data**: Future integration for automatic scraping of local cafe listings.

### 📊 Data Analytics (Planned)

- **Taste Profiling**: Use regression analysis to suggest coffees based on user preferences.
- **Aggregate Metrics**: Visual insights like average coffee prices and cafe ratings.

### 🎨 Frontend Features (Planned)

- **Login & Registration**: Intuitive account creation and authentication.
- **Review Feed**: Explore the latest user reviews in a dedicated feed.

## Technology Stack

### 🔧 Backend

- [**FastAPI**](https://fastapi.tiangolo.com): High-performance web framework for the API.
- [**SQLAlchemy**](https://www.sqlalchemy.org/): ORM for database interactions.
- [**Pydantic**](https://docs.pydantic.dev): Data parsing and validation.
- [**MySQL**](https://www.mysql.com/): Relational database.
- --[**Alembic**](https://alembic.sqlalchemy.org/): Database migrations.--
- [**Pytest**](https://pytest.org): For automated backend testing.
- 🔐 **Authentication**: Secure password hashing via bcrypt and JWT for user authentication.

### 📱 Frontend

- [**Kotlin**](https://kotlinlang.org/): For Android app development.
- _Planned_: Migration to **Flutter** for cross-platform Android and iOS support.

### 🐳 DevOps

- [**Docker Compose**](https://docs.docker.com/compose/): Containerized development and deployment.

## TODO

- 🧠 **Analytics**: Implement taste profiling and recommendation engine.
- 🌍 **Scraping**: Automate the collection of local cafe data.
- 🔧 **Frontend**: Complete development of UI components.
- 🧪 **Testing**: Expand test coverage for edge cases and performance.
- 🧳 **Migrations**: Integrate Alembic for scalable DB changes.

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL database setup
- Docker (optional but recommended)
