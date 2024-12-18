from firebase_admin import auth
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from functools import wraps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token')
        try:
            decoded_token = auth.verify_id_token(token)
            user = auth.get_user(decoded_token['uid'])
            if not user.custom_claims or not user.custom_claims.get('admin'):
                raise HTTPException(status_code=403, detail="Admin access required")
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")
    return wrapper

@router.get("/users", dependencies=[Depends(admin_required)])
async def list_users():
    try:
        users = auth.list_users()
        return {"users": [user.to_dict() for user in users.iterate_all()]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
