# Todo App — 2 Tier Web Application with CI/CD Pipeline

A full-stack Todo List application built with Flask and MySQL, containerized with Docker, and deployed to AWS EC2 via an automated Jenkins CI/CD pipeline.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [Deployment](#deployment)

---

## Overview

This project demonstrates a complete DevOps workflow for a 2-tier web application. It covers containerization with Docker, automated testing with pytest, continuous integration and delivery with Jenkins, and cloud deployment to AWS EC2.

The application allows users to manage daily tasks with scheduling, featuring input validation on both frontend and backend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend & Backend | Python, Flask |
| Database | MySQL 8.0 |
| Containerization | Docker, Docker Compose |
| CI/CD | Jenkins |
| Version Control | Git, GitHub |
| Cloud | AWS EC2 (Ubuntu 22.04) |
| Testing | pytest, unittest.mock |

---

## Architecture

```
Developer (VS Code)
        │
        │ git push
        ▼
    GitHub Repo
        │
        │ webhook trigger
        ▼
  Jenkins (local)
        │
   ┌────┴────┐
   │ Pipeline │
   │  Build   │──► Test (pytest) ──► Deploy via SSH
   └─────────┘
        │
        │ SSH + git pull + docker-compose up
        ▼
   AWS EC2 Instance
   ┌─────────────────────────────┐
   │   Docker Compose Network    │
   │                             │
   │  ┌──────────┐  ┌─────────┐ │
   │  │  Flask   │◄─►│ MySQL  │ │
   │  │  :5000   │  │  :3306 │ │
   │  └──────────┘  └─────────┘ │
   └─────────────────────────────┘
        │
        │ http://EC2_IP:5001
        ▼
     End User
```

**Tier 1 — Web Layer:** Flask handles HTTP requests, renders HTML templates, and performs input validation.

**Tier 2 — Data Layer:** MySQL stores and retrieves task data with persistent Docker volume.

---

## Features

- Add, view, and delete tasks
- Schedule tasks with time input (HH:MM format)
- Input validation — rejects empty tasks and invalid time format
- Dark mode minimalist UI
- Automated CI/CD — every `git push` triggers build, test, and deploy
- Email notifications on pipeline success or failure
- Unit tests with database mocking (no real DB needed for tests)

---

## Project Structure

```
to-do-app/
├── app.py                  # Flask application & routes
├── requirements.txt        # Python dependencies
├── Dockerfile              # Flask container image
├── docker-compose.yml      # Multi-container orchestration
├── Jenkinsfile             # CI/CD pipeline definition
├── init.sql                # MySQL table initialization
├── test_app.py             # Unit tests
├── .env                    # Environment variables (not committed)
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker build ignore rules
└── templates/
    └── index.html          # Frontend template
```

---

## CI/CD Pipeline

The Jenkins pipeline consists of three stages:

```
git push
    │
    ▼
┌─────────┐     ┌─────────┐     ┌──────────────┐
│  Build  │────►│  Test   │────►│ Deploy to EC2│
└─────────┘     └─────────┘     └──────────────┘
     │               │                  │
docker-compose   pytest runs       SSH to EC2
   build         5 unit tests      git pull +
                                docker-compose up
```

If any stage fails, the pipeline stops and an email notification is sent. The app is only updated when all tests pass.

**Test coverage:**
- `test_homepage_loads` — verifies the homepage returns HTTP 200
- `test_add_task` — verifies task submission redirects correctly
- `test_format_jadwal` — verifies datetime format conversion
- `test_add_task_invalid_jadwal` — verifies invalid time input is rejected
- `test_add_task_empty` — verifies empty task name is rejected

---

## Getting Started

### Prerequisites

- Docker Desktop
- Git

### Clone the repository

```bash
git clone https://github.com/cycwag/to-do-app.git
cd to-do-app
```

### Create environment file

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=tododb
MYSQL_PASSWORD=your_password
```

### Run the application

```bash
docker-compose up --build
```

Open your browser and navigate to:

```
http://localhost:5001
```

### Stop the application

```bash
docker-compose down
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `MYSQL_ROOT_PASSWORD` | MySQL root password |
| `MYSQL_DATABASE` | Database name |
| `MYSQL_PASSWORD` | MySQL user password |

These variables are loaded from the `.env` file locally and from Jenkins Global Environment Variables in the CI/CD pipeline.

---

## Running Tests

Run all unit tests inside Docker:

```bash
docker-compose run --rm --no-deps web pytest test_app.py -v
```

Run a specific test:

```bash
docker-compose run --rm --no-deps web pytest test_app.py::test_homepage_loads -v
```

---

## Deployment

The application is deployed to AWS EC2 automatically via Jenkins after every successful push to the `main` branch.

**Manual deployment to EC2:**

```bash
ssh -i "your-key.pem" ubuntu@YOUR_EC2_IP
cd /home/ubuntu/to-do-app
git pull origin main
docker-compose down -v
docker-compose up -d --build
```

The app is accessible at:

```
http://YOUR_EC2_IP:5001
```

---

## Author

 [@cycwag](https://github.com/cycwag)
