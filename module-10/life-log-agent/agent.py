from openai import OpenAI

from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    MODEL_NAME,
)

from memory.episodic import (
    get_recent_conversations,
    save_conversation,
    get_conversation_count
)
from memory.semantic import save_fact, get_fact_by_id

from memory.vector_store import VectorStore
from memory.reflection import get_latest_reflections, save_reflection



class LifeLogAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
        )
        self.vector_store = VectorStore()

    def chat(self, user_message: str):

        # 1. Get recent conversations
        history = get_recent_conversations(5)

        # 2. Get relevant semantic memories
        semantic_memories = self.retrieve_semantic_memory(
            user_message
        )

        reflections = get_latest_reflections()

        reflection_text = "\n".join(reflections)

        # 3. Build system prompt
        system_prompt = f"""
You are a helpful assistant.

Long-term reflections:

{reflection_text}

Relevant semantic memories:

{chr(10).join(semantic_memories)}

Use these memories only when they help answer the user's question.
"""

        # 4. Build messages
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # 5. Add episodic memory
        for user, assistant in history:

            messages.append({
                "role": "user",
                "content": user
            })

            messages.append({
                "role": "assistant",
                "content": assistant
            })

        # 6. Add current question
        messages.append({
            "role": "user",
            "content": user_message
        })

        # 7. Call LLM
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )

        answer = response.choices[0].message.content

        # 8. Save episodic memory
        save_conversation(
            user_message,
            answer
        )

        # 9. Extract semantic memory
        facts = self.extract_facts(user_message)

        for fact in facts:
            save_fact(fact)
            self.vector_store.add(fact)

        count = get_conversation_count()

        if count % 10 == 0:

            reflection = self.generate_reflection()

            save_reflection(reflection)

        return answer
    
    def extract_facts(self, user_message):

        prompt = f"""
    Extract permanent user facts.

    Rules:
    - Return one fact per line.
    - Ignore temporary requests.
    - Ignore greetings.
    - Only return facts worth remembering.

    User message:
    {user_message}
    """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You extract user facts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        return [
            line.strip()
            for line in content.split("\n")
            if line.strip()
        ]
    
    def retrieve_semantic_memory(self, question):

        indexes = self.vector_store.search(question)

        memories = []

        for idx in indexes:

            fact = get_fact_by_id(idx)

            if fact:

                memories.append(fact)

        return memories
    

    def generate_reflection(self):

        history = get_recent_conversations(10)

        conversation_text = ""

        for user, assistant in history:

            conversation_text += f"""
    User: {user}
    Assistant: {assistant}

    """

        prompt = f"""
    Summarize the user's long-term interests and goals.

    Return 3-5 concise bullet points.

    Conversation:

    {conversation_text}
    """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize long-term memory."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content