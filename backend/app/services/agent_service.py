import json
import logging
import os
from typing import AsyncGenerator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.core.config import settings
from app.schemas import KnowledgeBaseToolInput, ResumeEmailToolInput
from app.services.contact_service import send_email_tool
from app.services.rag_service import get_retriever, is_retriever_ready

logger = logging.getLogger(__name__)

TOOL_DISPLAY_NAMES = {
    "PortfolioKnowledgeBase": "Searching knowledge base",
    "SendResumeEmail": "Sending resume email"
}

AGENT_SYSTEM_PROMPT = f"""You are the Virtual Assistant for {settings.PORTFOLIO_OWNER}, a Software Engineer, Full-Stack Developer, and third-year Computer Engineering student at ESTIN.

Your purpose is to answer visitor questions about {settings.PORTFOLIO_OWNER}'s education, professional experience, technical skills, projects, certifications, interests, and career goals.

Use ONLY information available in the provided portfolio knowledge base via the `PortfolioKnowledgeBase` tool.

NEVER invent or assume:
- Employers
- Clients
- Job titles
- Dates
- Projects
- Technologies
- Certifications
- Achievements
- Responsibilities
- Education
- Professional experience
- Statistics
- Revenue
- Business results

{settings.PORTFOLIO_OWNER} has hands-on experience in full-stack development, AI/ML, ERP systems, databases, network and systems administration, and freelance video editing/content creation.

When discussing experience, clearly distinguish between:
- Professional/internship experience
- Freelance experience
- AI/ML training/project experience
- Independent/personal projects
- Academic experience

Do not describe personal projects as professional employment.

Do not claim that {settings.PORTFOLIO_OWNER} has senior-level experience.

Present him as an ambitious Software Engineer / Full-Stack Developer and AI Engineering student with practical hands-on experience.

His main technical areas include:
- Full-stack Web Development
- Next.js
- React
- TypeScript
- Node.js
- Express
- Python
- Machine Learning
- Speech Recognition
- Whisper
- Hugging Face
- PyTorch
- PostgreSQL
- MongoDB
- Prisma
- Docker

If asked about his AI experience, mention his work with Whisper fine-tuning, Quran recitation speech recognition, Hugging Face datasets, PyTorch, LoRA, and machine learning when relevant.

If asked about his professional experience, mention the relevant internships and freelance experience from the knowledge base.

If asked what type of work {settings.PORTFOLIO_OWNER} is looking for, mention:
- Full-stack development
- AI/ML engineering
- AI-powered applications
- SaaS development
- Backend/frontend development
- Automation
- Freelance development
- Software engineering internships
- Junior software engineering roles
- AI/ML opportunities

Respond in the same language used by the visitor.

Supported languages:
- English
- French
- Arabic

For English:
Use clear, professional English.

For French:
Use natural professional French.

For Arabic:
Use clear, natural Arabic. Algerian expressions may be used when appropriate, but maintain professionalism.

Be:
- Professional
- Friendly
- Concise
- Confident
- Accurate

Do not sound like a generic AI assistant.

If information is not available, say:
'That information is not currently included in {settings.PORTFOLIO_OWNER}'s portfolio, so I don't want to speculate.'

Never guess.

Your primary objective is to help visitors understand {settings.PORTFOLIO_OWNER}'s technical capabilities, practical experience, projects, and professional direction.

**TOOL USAGE:**
1. For questions about skills, projects, experience, education, certifications, or background — search `PortfolioKnowledgeBase` first.
2. Never mention "retrieving documents" or "database". Say "Let me check Noureddine's portfolio..." or similar.
3. For resume requests: search the knowledge base first, then offer to email a PDF if appropriate.
4. For resume email: use `SendResumeEmail` only when the visitor explicitly requests it and provides an email address.
5. For contact questions: share GitHub (github.com/nxr-dine), LinkedIn (linkedin.com/in/nxr-dine), phone (+213540194210), location (Bouira, Algeria), and the on-site contact form.
6. Refuse off-topic requests (general trivia, unrelated creative writing, unrelated advice) and pivot back to portfolio topics.

**TOPIC GUARDRAILS:**
Your ONLY purpose is to discuss {settings.PORTFOLIO_OWNER}, his projects, skills, experience, and professional background.
"""


# Tools

async def rag_tool_wrapper(question: str) -> str:
    """Retrieves portfolio information from the vector database."""
    if not is_retriever_ready():
        return "I am currently waking up from a cold start and loading my knowledge base. Please ask me again in about 10 seconds."

    try:
        retriever = get_retriever()
        docs = await retriever.ainvoke(question)

        if not docs:
            return "No relevant information found in the portfolio documents."

        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        logger.error(f"RAG Tool Error: {e}", exc_info=True)
        return "Error retrieving information. Please try again."


async def send_resume_email(recipient: str) -> str:
    """Sends the resume email via the configured mail service."""
    subject = f"{settings.PORTFOLIO_OWNER}'s Resume"
    body = f"""
            <p>Hello,</p>
            <p>Thank you for your interest in {settings.PORTFOLIO_OWNER}'s profile.</p>
            <p>You can view and download the resume here:</p>
            <p>
                <a href="{settings.RESUME_LINK}" 
                   style="background-color:#4F46E5; color:white; padding:12px 24px; text-decoration:none; border-radius:6px; font-weight:bold; display:inline-block;">
                   View Resume PDF
                </a>
            </p>
            <br>
            <p>Best regards,</p>
            <p>{settings.PORTFOLIO_OWNER}'s AI Assistant</p>
        """

    try:
        send_email_tool(recipient=recipient, subject=subject, body=body)
        logger.info(f"Resume sent to {recipient}")
        return f"Successfully sent email to {recipient}."
    except Exception as e:
        logger.error(f"Email Tool Error: {e}", exc_info=True)
        return f"Error sending email: {str(e)}"


# Agent

rag_tool = Tool(
    name="PortfolioKnowledgeBase",
    func=None,
    coroutine=rag_tool_wrapper,
    description=(
        f"Use this tool to search {settings.PORTFOLIO_OWNER}'s portfolio. "
        "CRITICAL: Do not just pass the user's raw message. "
        f"1. Replace pronouns (he/him/his) with '{settings.PORTFOLIO_OWNER}'. "
        "2. Focus on keywords (skills, projects, education, experience). "
        f"Example: If user asks 'What is his tech stack?', input should be '{settings.PORTFOLIO_OWNER} technical skills and tech stack'."
    ),
    args_schema=KnowledgeBaseToolInput
)

resume_email_tool = Tool(
    name="SendResumeEmail",
    func=None,
    coroutine=send_resume_email,
    description=f"Use this tool only when a user explicitly asks for a copy of {settings.PORTFOLIO_OWNER}'s resume.",
    args_schema=ResumeEmailToolInput
)

tools = [rag_tool, resume_email_tool]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", AGENT_SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

def _create_agent_with_chat_history() -> RunnableWithMessageHistory:
    """Builds the Gemini agent only when a chat request is received."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.3
    )
    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )


# Streaming

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=settings.REDIS_URL)


def format_sse_event(event_type: str, data: dict) -> str:
    """Formats data into Server-Sent Events (SSE) protocol string."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


async def stream_agent_response(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Orchestrates agent interaction and streams SSE events to the client."""
    config = {"configurable": {"session_id": session_id}}

    try:
        agent_with_chat_history = _create_agent_with_chat_history()
        async for event in agent_with_chat_history.astream_events(
                {"input": message},
                config=config,
                version="v2"
        ):
            kind = event["event"]
            name = event.get("name", "")
            data = event.get("data", {})

            if kind == "on_tool_start" and name in TOOL_DISPLAY_NAMES:
                display_name = TOOL_DISPLAY_NAMES.get(name, name)
                yield format_sse_event("tool_start", {"tool": name, "message": f"🔍 {display_name}..."})

            elif kind == "on_tool_end" and name in TOOL_DISPLAY_NAMES:
                output = str(data.get("output", ""))
                is_error = not output or "Error" in output
                status_msg = "⚠️ Could not find specific details." if is_error else "✅ Found relevant information"

                yield format_sse_event("tool_end", {"tool": name, "message": status_msg})

            elif kind == "on_chat_model_stream":
                chunk = data.get("chunk")
                if chunk and getattr(chunk, "content", ""):
                    yield format_sse_event("token", {"content": chunk.content})

    except Exception as e:
        logger.error(f"Stream Agent Error: {e}", exc_info=True)
        yield format_sse_event("error", {"message": "❌ Sorry, an unexpected system error occurred."})

    finally:
        yield format_sse_event("done", {"message": "[DONE]"})
