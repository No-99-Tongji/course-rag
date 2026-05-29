import os
from typing import Iterable

from .corpus import Document


def build_context(results: Iterable[tuple[Document, float]]) -> str:
    blocks = []
    for index, (doc, score) in enumerate(results, 1):
        meta = f"来源：{doc.source}"
        if doc.lesson:
            meta += f"；章节：{doc.lesson}"
        if doc.topic:
            meta += f"；主题：{doc.topic}"
        blocks.append(
            f"[资料{index}] {doc.title}\n{meta}\n相关度：{score:.4f}\n{doc.content}"
        )
    return "\n\n".join(blocks)


def answer_without_llm(query: str, results: list[tuple[Document, float]]) -> str:
    if not results:
        return "没有在课程语料中检索到相关内容。"

    parts = ["我在课程语料中找到以下相关内容："]
    for index, (doc, _) in enumerate(results[:4], 1):
        summary = doc.content.strip().replace("\n", " ")[:260]
        source = doc.source
        lesson = f"，章节 {doc.lesson}" if doc.lesson else ""
        parts.append(f"{index}. {doc.title}（来源：{source}{lesson}）：{summary}")
    parts.append("如果需要生成更自然的综合回答，请配置 OPENAI_API_KEY 或兼容 OpenAI 的模型服务。")
    return "\n".join(parts)


async def answer_with_optional_llm(query: str, results: list[tuple[Document, float]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        return answer_without_llm(query, results)

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    context = build_context(results)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是软件工程经济学课程助手。只能基于给定资料回答；如果资料不足，要明确说明。回答使用中文，并在关键结论后标注资料编号。",
            },
            {
                "role": "user",
                "content": f"问题：{query}\n\n课程资料：\n{context}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or "模型没有返回答案。"
