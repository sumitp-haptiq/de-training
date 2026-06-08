# Prefect Demo Flows

This repository contains two Prefect flows demonstrating how to orchestrate data pipelines and verify a working Prefect setup.

---

## Overview

### **1. demo.py**

A simple ETL (Extract–Transform–Load) pipeline built using Prefect, Pandas, and SQLAlchemy.

#### **Flow Structure**

| Step | Task | Description |
|------|------|--------------|
| 1 | **Extract** | Fetches user data from a public API (`https://jsonplaceholder.typicode.com/users`) and converts it into a Pandas DataFrame. |
| 2 | **Transform** | Cleans the data by removing unnecessary columns (`address`, `company`). |
| 3 | **Load to Postgres** | Writes the transformed data into a PostgreSQL table named `users_api`. |

This flow demonstrates how Prefect can be used to build reliable, observable data workflows that integrate with APIs and databases.

---

### **2. hello.py**

A minimal Prefect flow designed to test a working setup.  
It simply logs a “Hello World” message and confirms that Prefect runs successfully.

---

## Setup

The flows assume the following:
- Python environment with Prefect, Pandas, SQLAlchemy, and Requests installed.  
- A PostgreSQL database accessible using the connection string defined in the flow.  
- Optional Docker setup for local testing of Prefect and Postgres.

---

## Improvement Challenge

The `transform()` task currently removes a fixed set of columns.  
To make it more flexible and reusable, consider extending it with additional functionality such as:

- Accepting a list of columns to drop dynamically.  
- Allowing column renaming through a mapping dictionary.  
- Adding transformations such as filtering, type conversion, or data enrichment.

**Question:**  
*How can you modify the `transform()` task so that it can accept parameters (for example, `drop_columns` or `rename_columns`) and handle different API responses without changing the core flow code? You can create and add your own scenarios too.*
