from typing import List, Dict, Annotated
import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, Header, Depends, HTTPException, status
# from models.schemas.schemas import CompletionResponse, RouteRequest
from app.repositories.myapi_repo import get_user_id_by_myapi
from app.api.deps import get_db
from app.services import myapi, router as litellm_router
from app.schemas import RouteRequest

router = APIRouter()

@router.post('/completion')  # response_model=CompletionResponse)
def chat_completion(
    data: RouteRequest, 
    myapi_key: str = Header(None), 
    db: Session = Depends(get_db)
    ):
    # grab the API key from the auth header of the request
    # if authorization is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, 
    #         detail="API key not provided. Can not access router."
    #     )
    # else:
    # api_key = "9624737a2087331b78c0fea213a926f1ebbb78d5a36e11deac674c82451ab577"
    # api_key = "gAAAAABmth5XFAMH6QEd-w4EIncdcuQYoa35IJWj7MSqTxUAdW-Zj3RJw6WYg8fdMKtpbqU5WhbRTBXV55RO3iw-WmXfsK6zmPIB-wA8IUsKqSk571dacM92zNILr9-NP2R6hH7LrhBLvHc43nk5cNAgJFxNdricZEOUxj-f2xzzZtiXlUDWE44="
    # api_key = "gAAAAABmtVSSItJmiSV7GZx2LlCrM0CVRRwN6z2lZ5Kxr5aULrXEoSFYkC7KRYT17AA339Kxdofi-jWj9QMafrxZJVAOkTVs_B5WZmx_01m5r6REFHti-L0CB3L01Gzko3WuT3n4xQeebLXR4aL124x1UZ_8fTSN1WmOFLWM8PkZH5_Hx2pJmoU="
    api_key = myapi_key

    # verify API key -> will need to wait on the merge
    verified_rout3_key = myapi.verify_api_key(db=db, api_key_string=api_key)
    if verified_rout3_key:
        # make GET request to the endpoint 'api/v1/configuration' and grab the user settings
        # and to make that call, we'd need to query by user_id. How would we grab the user_id?
        # We could just grab the id based on the Rout3 API Key passed in

        # 1) FETCH user_id USING API KEY -> GET 'api/v1/myapi/userid'
        user_id = get_user_id_by_myapi(db=db, myapi_key=api_key)
        # 2) get user_settings using user_id -> from config
        user_settings = [
            {
                "model_name": "router",  # model alias for routing/load balancing
                "litellm_params": {
                    "model": "command",
                    "api_key": os.getenv("COHERE_API_KEY"), # PUT SECRET HERE
                    "timeout": 1,
                    "max_tokens": 200,
                    "temperature": 0.98
                }
            },
            {
                "model_name": "router",
                "litellm_params": {
                    "model": "command-nightly",
                    "api_key": os.getenv("COHERE_API_KEY"),
                    "timeout": 1,
                    "max_tokens": 200,
                    "temperature": 0.98
                    
                }
            },
            {
                "model_name": "router", 
                "litellm_params": { 
                    "model": "command-r", 
                    "api_key": os.getenv("COHERE_API_KEY"),
                    "timeout": 1,
                    "max_tokens": 200,
                    "temperature": 0.98
                }
            },
            {
                "model_name": "router",
                "litellm_params": {
                    "model": "command-r-plus",
                    "api_key": os.getenv("COHERE_API_KEY"),
                    "timeout": 1,
                    "max_tokens": 200,
                    "temperature": 0.98
                }
            }
        ]
        analytics_data = litellm_router.get_completion(user_settings, data, user_id)
        print(analytics_data)
        # make any API calls to grab data like: user_id, 
        
        # make a POST request to 'api/v1/analytics/record' to send the data in 'body' and pass in the API key into the header for auth
                
        # if data was successfully sent to 'record' endpoint
            # return the CompletionResponse

        # if request to 'record' endpoint errored out
            # raise the error
    else:
        # raise invalid API key exception with error code 401 and message "Invalid API key. Ensure the correct API key and requesting 
        # organization are being used."
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
