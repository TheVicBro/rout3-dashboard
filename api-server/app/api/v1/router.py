from typing import Annotated
import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, Header, Depends, HTTPException, status

# from models.schemas.schemas import CompletionResponse, RouteRequest
from app.repositories.myapi_repo import get_user_id_by_myapi

# from app.repositories.usages_repo import create_usage_entry
from app.api.deps import get_db
from app.services import myapi, router as litellm_router
from app.schemas import RouteRequest, CompletionResponse
from openai import (
    APIConnectionError,
    UnprocessableEntityError,
    APIStatusError,
    APITimeoutError,
)

router = APIRouter()


@router.post("/completion")
async def chat_completion(
    data: RouteRequest,
    myapi_key: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
) -> CompletionResponse:
    # grab the API key from the auth header of the request
    if myapi_key is None:
        raise HTTPException(
            detail="API key not provided. Can not access router.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # verify API key
    verified_rout3_key = myapi.verify_api_key(db=db, api_key_string=myapi_key)

    if verified_rout3_key:
        # We grab the user id based on the Rout3 API Key passed in and then grab the user_settings
        user_id = get_user_id_by_myapi(db=db, myapi_key=myapi_key)
        user_settings = get_user_settings(db, user_id)
        # user_settings = [
        #     {
        #         "model_name": "router",  # model alias for routing/load balancing
        #         "litellm_params": {
        #             "model": "command",
        #             "api_key": os.getenv("COHERE_API_KEY"),  # PUT SECRET HERE
        #             "timeout": 1,
        #             "max_tokens": 200,
        #             "temperature": 0.98,
        #         },
        #     },
        #     {
        #         "model_name": "router",
        #         "litellm_params": {
        #             "model": "command-nightly",
        #             "api_key": os.getenv("COHERE_API_KEY"),
        #             "timeout": 1,
        #             "max_tokens": 200,
        #             "temperature": 0.98,
        #         },
        #     },
        #     {
        #         "model_name": "router",
        #         "litellm_params": {
        #             "model": "command-r",
        #             "api_key": os.getenv("COHERE_API_KEY"),
        #             "timeout": 1,
        #             "max_tokens": 200,
        #             "temperature": 0.98,
        #         },
        #     },
        #     {
        #         "model_name": "router",
        #         "litellm_params": {
        #             "model": "command-r-plus",
        #             "api_key": os.getenv("COHERE_API_KEY"),
        #             "timeout": 1,
        #             "max_tokens": 200,
        #             "temperature": 0.98,
        #         },
        #     },
        # ]
        try:
            completion_response = await litellm_router.get_completion(
                user_settings, data, user_id
            )
            # Store data to analytics table
            create_usage_entry(db=db, usage=completion_response)
            return completion_response
        except APITimeoutError as e:
            raise HTTPException(
                detail=e.message, status_code=status.HTTP_504_GATEWAY_TIMEOUT
            ) from e

        except APIConnectionError as e:
            raise HTTPException(
                detail=e.message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            ) from e

        except UnprocessableEntityError as e:
            raise HTTPException(detail=e.message, status_code=e.status_code) from e

        except APIStatusError as e:
            raise HTTPException(detail=e.message, status_code=e.status_code) from e

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_user_settings(db: Session, user_id: int):
    # Query DB for the config entry based on user_id AND GRAB the config_id, route_type, time_out and router_name
    configuration = get_configuration_by_user_id(db, user_id)
    # Query DB for the models associated with the config entry based on its id AND GRAB models, secret_key, max_tokens and temperature
    model_configuration = get_configuration_models_by_config_id(
        db, config_id=configuration.id
    )
    # set up the settings into the format that LiteLLM needs:

    user_settings = []
    for model_entry in model_configuration:
        user_settings.append(
            {
                "model_name": configuration.router_name,
                "litellm_params": {
                    "model": model_entry.models,
                    "api_key": model_entry.secret_key,
                    "timeout": configuration.time_out,
                    "max_tokens": model_entry.max_tokens,
                    "temperature": model_entry.temperature,
                },
            }
        )
    return user_settings
