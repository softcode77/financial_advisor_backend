# Financial Adviser Backend

This is the FastAPI backend for the Financial Adviser project.



##  Getting Started

Follow these steps to set up and run the backend server locally.



### 1. Clone the Repository

```bash
git clone https://github.com/yourname/financial-adviser-backend.git
cd financial-adviser-backend
```



### 2. Create a Virtual Environment

```bash
python -m venv venv



### 3. Activate the Virtual Environment

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**

  ```bash
  source venv/bin/activate


### 4. Install Dependencies

```bash
pip install -r requirements.txt
```


### 5. Run the FastAPI Server

```bash
uvicorn main:app --reload
```



---

##  Project Structure

```
.
├── main.py
├── requirements.txt
├── app/
│   ├── migrations/
│   ├── services/
│   └── ...
```

---

##  Notes

- Requires **Python 3.9+**
- Place any environment variables in a `.env` file if needed
- Server will run at: `http://127.0.0.1:8000`

---
