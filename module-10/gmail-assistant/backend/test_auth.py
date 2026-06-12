# from google_auth_oauthlib.flow import InstalledAppFlow

# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.readonly"
# ]

# flow = InstalledAppFlow.from_client_secrets_file(
#     "credentials.json",
#     SCOPES
# )

# creds = flow.run_local_server(port=0)

# print("Success")

# from app.gmail.service import summarize_latest_email

# summary = summarize_latest_email()
# print(summary)

# from app.agent.graph import graph

# result = graph.invoke({
#     "message": "summarize latest email"
# })

# print(result)


from app.agent.graph import graph

# print(
#     graph.invoke(
#         {"message": "hello"}
#     )
# )

# print(
#     graph.invoke(
#         {"message": "summarize latest email"}
#     )
# )

# print(graph.invoke({
#     "message": "show latest email"
# }))

# print(graph.invoke({
#     "message": "reply professionally"
# }))

# import app.store.draft_store as draft_store

# graph.invoke({
#     "message": "reply professionally"
# })

# print(draft_store.current_draft)

# print(graph.invoke({
#     "message": "reply professionally"
# }))

print(
    graph.invoke({
        "message": "reply professionally"
    })
)

print(
    graph.invoke({
        "message": "send it"
    })
)

print(graph.invoke({"message": "approve"}))

# from app.gmail.service import send_email

# send_email(
#     to="vinayakpsannaik@gmail.com",
#     subject="Test Email",
#     body="Hello from AI Email Assistant"
# )