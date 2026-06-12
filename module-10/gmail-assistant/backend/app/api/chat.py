# from fastapi import APIRouter

# from app.schemas.chat import ChatRequest
# from app.agent.graph import run_agent

# router = APIRouter()


# @router.post("/chat")
# async def chat(request: ChatRequest):
#     response = await run_agent(request.message)

#     return {
#         "response": response
#     }


# from app.gmail.service import get_latest_email

# router = APIRouter()


# # @router.get("/latest-email")
# # def latest_email():

# #     return get_latest_email()