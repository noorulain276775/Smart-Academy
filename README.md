# Smart Academy – Django ORM Complex Queries Optimization Playground

Smart Academy is a lightweight Django project built to simulate an educational platform with a focus on **query optimization** using Django ORM. It serves as a practice ground to write clean, efficient, and scalable database queries.

> "Instead of just making things work, I wanted to make them fast and elegant. So I built this!"

---

## Purpose

This project helps in learning and applying:

- Optimized querying using `select_related` and `prefetch_related`
- Aggregations like `Avg`, `Count`, `Sum`, and custom annotations
- Handling `OneToOne`, `ManyToMany`, and `ForeignKey` relationships
- Real-world filtering and business logic queries

The goal is to master Django ORM techniques and **avoid the N+1 problem** through practical, real-life scenarios.

---

## Project Structure

The app is modeled around an online learning platform with:

- `Student` – learners who enroll in courses
- `Teacher` – instructors handling multiple courses
- `Course` – main offering, related to teachers and students
- `Lesson` – child unit of a course with optional materials
- `Rating` – student feedback, used to calculate average scores

---

## Features to Practice

- View all students with their enrolled courses (ManyToMany + prefetch)
- Get all courses with their teacher and lesson count (select_related + annotate)
- Calculate average course rating (aggregate)
- Filter courses by rating threshold, price, or popularity
- See materials for lessons using reverse relationships
- Use `values()` and `only()` to optimize data selection

---

## Setup Instructions

```bash
git clone https://github.com/noorulain276775/Smart-Academy.git
cd smart-academy-django


python -m venv venv
source env/bin/activate
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
