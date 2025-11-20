# Smart Academy – Django ORM Complex Queries Playground

Smart Academy simulates a lean LMS so you can practice writing efficient Django ORM queries, annotations, and admin dashboards without worrying about front-end scaffolding.

## Why this project exists

- Explore `select_related`, `prefetch_related`, `annotate`, and window functions on realistic models.
- Experiment with performance techniques that prevent N+1 issues.
- Prototype advanced Django admin reports backed by the same query logic used in API views.

## Domain model

| Model | Highlights |
| --- | --- |
| `Teacher` | Instructors with bios; one-to-many with `Course` |
| `Student` | Learners, ManyToMany with `Course` |
| `Course` | Tracks teacher, enrolled students, price |
| `Lesson` | Belongs to a course, stores duration |
| `CourseMaterial` | Linked to lessons, stores resource metadata |
| `Rating` | Student feedback for courses |

## Local setup

```bash
git clone https://github.com/noorulain276775/Smart-Academy.git
cd Smart-Academy

python -m venv .venv
. .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## Run with Docker

```bash
docker compose up --build
```

Stop the stack with:

```bash
docker compose down
```

## Seed rich demo data

Populate the database with teachers, students, courses, lessons, materials, and ratings:

```bash
python manage.py seed_demo_data
```

From Docker:

```bash
docker compose run --rm web python manage.py seed_demo_data
```

Use `--append` to keep existing rows:

```bash
python manage.py seed_demo_data --append
```