import os
from typing import Dict, Generator, List, Optional, Tuple, Union

from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool

from src.config.settings import GEMINI_API_KEY, MODEL_ID, MODEL_TEMPERATURE, SYSTEM_INSTRUCTION


def _get_api_key() -> Optional[str]:
    return GEMINI_API_KEY or os.getenv("GOOGLE_API_KEY")


ChatMessage = Dict[str, str]
ChatLog = List[Union[ChatMessage, Tuple[str, str]]]


def _build_prompt(question: str, chat_log: ChatLog) -> str:
    if not chat_log:
        return question

    lines = ["Conversation so far:"]
    for item in chat_log:
        if isinstance(item, dict):
            role = item.get("role", "assistant")
            message = item.get("content", "")
        else:
            role, message = item
        if role.lower().startswith("user") or role.lower().startswith("you"):
            label = "User"
        elif role.lower().startswith("assistant") or role.lower().startswith("ai"):
            label = "Assistant"
        else:
            label = role
        lines.append(f"{label}: {message}")
    lines.append(f"User: {question}")
    return "\n".join(lines)


def _create_client() -> genai.Client:
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY.")
    return genai.Client(api_key=api_key)


def _build_config(
    use_web_search: bool,
    temperature: float,
    system_instruction: str,
) -> GenerateContentConfig:
    tools = [Tool(google_search=GoogleSearch())] if use_web_search else []
    return GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        tools=tools,
    )


def google_search_query(
    question: str,
    use_web_search: bool,
    chat_log: Optional[ChatLog] = None,
    model_id: str = MODEL_ID,
    temperature: float = MODEL_TEMPERATURE,
    system_instruction: str = SYSTEM_INSTRUCTION,
) -> Tuple[str, str]:
    chat_log = chat_log or []
    try:
        client = _create_client()
        prompt = _build_prompt(question, chat_log)
        config = _build_config(use_web_search, temperature, system_instruction)
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=config,
        )
        ai_response = response.text or ""
        search_results = "Web search not used."
        if use_web_search:
            search_results = (
                response.candidates[0]
                .grounding_metadata.search_entry_point.rendered_content
            )
        return ai_response, search_results
    except Exception as exc:
        return f"Error: {exc}", ""


def google_search_query_stream(
    question: str,
    use_web_search: bool,
    chat_log: Optional[ChatLog] = None,
    model_id: str = MODEL_ID,
    temperature: float = MODEL_TEMPERATURE,
    system_instruction: str = SYSTEM_INSTRUCTION,
) -> Generator[Tuple[str, str], None, None]:
    chat_log = chat_log or []
    try:
        client = _create_client()
        prompt = _build_prompt(question, chat_log)
        config = _build_config(use_web_search, temperature, system_instruction)
        response_stream = client.models.generate_content_stream(
            model=model_id,
            contents=prompt,
            config=config,
        )
        collected = []
        for chunk in response_stream:
            if chunk.text:
                collected.append(chunk.text)
                yield "".join(collected), ""
        final_text = "".join(collected)
        search_results = "Web search not used."
        if use_web_search:
            # Fetch search results metadata in a follow-up call.
            final_response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=config,
            )
            search_results = (
                final_response.candidates[0]
                .grounding_metadata.search_entry_point.rendered_content
            )
        yield final_text, search_results
    except Exception as exc:
        yield f"Error: {exc}", ""


def update_chatbot(
    question: str,
    use_web_search: bool,
    chat_log: Optional[List[ChatMessage]],
    model_id: str,
    temperature: float,
    stream: bool,
) -> Generator[List[ChatMessage], None, None] | List[ChatMessage]:
    if chat_log is None:
        chat_log = []
    if not question:
        return chat_log

    chat_log.append({"role": "user", "content": question})
    if stream:
        for partial, search_results in google_search_query_stream(
            question,
            use_web_search,
            chat_log,
            model_id,
            temperature,
        ):
            if chat_log and chat_log[-1].get("role") == "assistant":
                chat_log[-1] = {"role": "assistant", "content": partial}
            else:
                chat_log.append({"role": "assistant", "content": partial})
            yield chat_log
        if use_web_search and search_results:
            chat_log.append(
                {
                    "role": "assistant",
                    "content": f"Web Search Results:\n{search_results}",
                }
            )
        yield chat_log
    else:
        ai_response, search_results = google_search_query(
            question,
            use_web_search,
            chat_log,
            model_id,
            temperature,
        )
        chat_log.append({"role": "assistant", "content": ai_response})
        if use_web_search:
            chat_log.append(
                {
                    "role": "assistant",
                    "content": f"Web Search Results:\n{search_results}",
                }
            )
        return chat_log
