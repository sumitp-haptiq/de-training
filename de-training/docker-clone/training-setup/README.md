# 🧩 DBT Local Setup (with Docker)

This guide helps you set up a local **DBT environment** using Docker.  
You’ll get a running Postgres database and a DBT container to build and test your models.

---

## ⚙️ Step 1: Update Your Project Path

Open the `docker-compose.yml` file and **update the local path** under the `dbt` service.

Example — replace this line:
```yaml
- /path/to/project_dir:/usr/app
```

with your own local project path:
```yaml
- /absolute/path/to/your/project:/usr/app
```

💡 Tip: You can find your absolute path by running:
```bash
pwd
```
inside your project folder.

---

## 🐳 Step 2: Start Containers

From your project directory, run:
```bash
docker-compose up -d
```

This will start:
- **Postgres** database (port 5432)
- **DBT** container (with dbt-postgres preinstalled)

To verify:
```bash
docker ps
```
You should see both `dbt_postgres` and `dbt_container` running.

---

## 🧠 Step 3: Login to DBT Container

Access the DBT shell:
```bash
docker exec -it dbt_container bash
```

You’ll now be inside the DBT environment.

---

## 🏗️ Step 4: Initialize a DBT Project

Inside the container:
```bash
dbt init training_dbt
```

Follow the prompts (choose “postgres” as the adapter).

This will create a folder structure like:
```
training_dbt/
├── dbt_project.yml
├── models/
│   └── example/
└── ...
```

---

## 🗂️ Step 5: Configure Profiles

Inside your project directory (not inside the DBT project folder), create a file called `profiles.yml` with this content:

```yaml
training_dbt:
  target: dev
  outputs:
    dev:
      type: postgres
      host: db
      user: dbt_user
      password: dbt_pass
      port: 5432
      dbname: dbt_demo
      schema: public
```

Make sure it’s accessible at `/usr/app/profiles.yml` inside the container.

You can test:
```bash
echo $DBT_PROFILES_DIR
```
It should point to `/usr/app`.

---

## 🧪 Step 6: Run DBT Commands

Now try running:

```bash
dbt debug       # Check connection and environment
dbt run         # Run models
dbt test        # Run data tests
dbt docs generate && dbt docs serve  # View documentation site
```

---

## ✅ Step 7: Verify Setup

After running `dbt run`, connect to the Postgres database:

```bash
psql -h localhost -U dbt_user -d dbt_demo
```

You should see your model outputs (e.g., `example_model` table).

---

## 🧹 Step 8: Stop Containers (When Done)

```bash
docker-compose down
```

---

### 💬 Notes
- DBT project files live on your local machine and sync into the container.
- You can edit `.sql` or `.yml` files locally and rerun DBT commands inside the container.
- If anything breaks, restart with:
  ```bash
  docker-compose down && docker-compose up -d
  ```

Happy building with DBT! 🚀
