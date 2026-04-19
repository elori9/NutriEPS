# NutriEPS - Fitness & Nutrition Tracker

A web application developed with Django for calories tracking and complete weight goals.

---
### A. Data Model Implementation
The application implements a relational PostgreSQL database because is better for production and docker. 
PostgreSQL runs in its own container so Docker Compose make it easier to run both. The model includes:
* **User:** Django's built-in authentication model.
* **UserProfile:** Extends the user with physical metrics (height, weight, age, gender, activity level, and goals).
* **FoodItem:** An independent entity that stores foods, with it information, searched for users.
* **ConsumptionLog:** A relationship bridging a `User` and a `FoodItem`, storing the exact quantity consumed on a specific date.
* **WeightLog:** Tracks user weight progression over time.

### B. 12-Factor App Guidelines
We tryed to stick for 12-factor application principles, there are some examples of it:
* **Codebase (Factor I):** Used git on the same repo.
* **Dependencies (Factor II):** Explicitly declared in `pyproject.toml` and managed using `uv` for exceptionally fast and deterministic builds.
* **Config (Factor III):** Sensitive configuration, such as database credentials, is managed via environment variables (`vars.env`).
* **Dev/Prod Parity (Factor X):** The application relies entirely on Docker and Docker Compose.

### C. API AND PERFORMANCE
* **External Integration:** Integrated the Open Food Facts API to allow users to search foods, this API is free and don't need an API key.
* **Local Caching:** To optimize performance and reduce external API dependency, when a user adds an item from the API, it is automatically saved into the local `FoodItem` table.

### D. User Interface (UI)
Developed a clean and usable UI with visual consistency.
Includes interactive progress bars and macro rings to allow users to easily browse and understand their application data.

---

## How to Run / Deploy
To run it:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/elori9/NutriEPS.git
   cd NutriEPS
   ```
   
2. Rename `vars.env.example` to `vars.env` and set your preferred PostgreSQL credentials.

3. Build and start the containers using Docker Compose:
   ```bash
   docker compose up --build
   ```
   
4. Apply the migrations (not necessary because dockerfile does them)
   ```bash
   docker compose exec web uv run python manage.py makemigrations
   docker compose exec web uv run python manage.py migrate
   ```
   
5. Create an admin user: This is required to access the Django Admin panel:
   ```bash
   docker compose exec web uv run python manage.py createsuperuser
   ```

6. You can access to it on: 
- Web: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Deployed on: https://nutrieps.onrender.com/ 
(may take some time to load if the instance is off, because we are using the free plan)