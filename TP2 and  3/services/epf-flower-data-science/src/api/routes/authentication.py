
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from firebase_admin import auth, credentials, initialize_app
from typing import List
from pathlib import Path
import firebase_admin

router = APIRouter()

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred_path = Path(__file__).parent.parent.parent / "config" / "serviceAccountKey.json"
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred, {
    'projectId': 'myproject-0412025',
    'authDomain': 'myproject-0412025-94c7f.firebaseapp.com',
})


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="https://myproject-0412025-94c7f.firebaseapp.com/__/auth/action"
)


@router.post("/register")
async def register_user(email: str, password: str):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=False,
            disabled=False
        )
        # Send email verification
        verification_link = auth.generate_email_verification_link(email)
        # You'll need to implement email sending here
        return {
            "message": f"User {email} created successfully. Please check your email for verification.",
            "uid": user.uid
        }
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to register user. Please contact support.")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = auth.get_user_by_email(form_data.username)
        custom_token = auth.create_custom_token(user.uid)
        return {
            "access_token": custom_token,
            "token_type": "bearer",
            "uid": user.uid
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = auth.verify_id_token(token)
        auth.revoke_refresh_tokens(decoded_token['uid'])
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


