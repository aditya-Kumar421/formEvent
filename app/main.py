from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from .database.database import registration_collection
from .services.email_utils import send_email
import httpx
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from .models.models import Registration
from .config.settings import settings

app = FastAPI(title="FastAPI Registration Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "2 per minute"]
)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY

#Recaptcha verification function
async def verify_recaptcha(recaptcha_response: str) -> bool:
    url = "https://www.google.com/recaptcha/api/siteverify"
    
    params = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=params)
        result = response.json()
    
    return result.get("success", False)


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    registration: Registration, 
    background_tasks: BackgroundTasks
):
    is_valid = await verify_recaptcha(registration.recaptcha_response)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid reCAPTCHA. Please try again.")
    

    existing_user = await registration_collection.find_one(
        {"$or": [{"participants.email": registration.participants[0].email},
                 {"participants.student_no": registration.participants[0].student_no},
                 {"participants.email": registration.participants[1].email},
                 {"participants.student_no": registration.participants[1].student_no}]}
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student number or email already registered."
        )

    registration_dict = registration.model_dump(exclude={"recaptcha_response"})

    await registration_collection.insert_one(registration_dict)

    # Send a background email task
    background_tasks.add_task(send_email, registration.participants[0].email, registration.team_name)

    return {"message": "Registration successful"}