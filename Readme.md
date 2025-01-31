    # FastAPI Project Setup

1. **Install FastAPI and Dependencies**:
   ```bash
   pip install fastapi[all] python-jose bcrypt
   ```

2. **Directory Structure**:
   ```
   fastapi_auth_project/
   |-- app/
       |-- __init__.py
       |-- main.py
   |-- requirements.txt
   |-- README.md
   ```

3. **Create `main.py`**:
   Place the provided code in `app/main.py`.

4. **Add Dependencies to `requirements.txt`**:
   ```
   fastapi
   uvicorn
   python-jose
   bcrypt
   ```

5. **Run the Application**:
   Navigate to the `fastapi_auth_project` directory and run:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Endpoints Available**:
   - `POST /register`: Register a new user.
   - `POST /login`: Login and obtain a JWT token.
   - `POST /forgot-password`: Request a reset token for password reset.
   - `POST /reset-password`: Reset the password using the reset token.
   - `POST /change-password`: Change password (requires valid JWT token).

7. **Testing**:
   Use a tool like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to test the endpoints.

8. **Example Commands**:
   - Register a user:
     ```bash
     curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}' \
     http://127.0.0.1:8000/register
     ```
   - Login:
     ```bash
     curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=password123" \
     http://127.0.0.1:8000/login
     ```
