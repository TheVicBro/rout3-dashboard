from typing import Coroutine, List, Dict, Any
import asyncio
from datetime import datetime
from litellm import Router, cost_per_token, ModelResponse
from app.schemas import RouteRequest, CompletionResponse


async def get_completion(
    user_settings: List[Dict[str, Any]], data: RouteRequest, user_id
) -> CompletionResponse:

    llm_router = Router(model_list=user_settings, routing_strategy="cost-based-routing")
    response = await async_route_completion(
        llm_router, data.chat_history, data.router_name
    )
    return process_response(response, data, user_id)


async def async_route_completion(
    llm_router: Router, chat_history: List[Dict[str, str]], router_name: str
) -> ModelResponse:
    response = await llm_router.acompletion(model=router_name, messages=chat_history)
    return response


def process_response(
    response: ModelResponse, data: RouteRequest, user_id: str
) -> Dict[str, Any]:
    model = response.model
    prompt_content = data.chat_history[-1]["content"]
    response_content = response.choices[0].message.content
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    prompt_tokens_cost_usd_dollar, completion_tokens_cost_usd_dollar = cost_per_token(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=response_tokens,
    )
    date_time = datetime.now()
    data.chat_history.append({"role": "assistant", "content": response_content})

    body = {
        "model": response.model,
        "prompt": prompt_content,
        "response": response_content,
        "chat_history": data.chat_history,
        "prompt_cost": prompt_tokens_cost_usd_dollar,
        "response_cost": completion_tokens_cost_usd_dollar,
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "date_time": date_time,
        "user_id": user_id,
    }
    return body
