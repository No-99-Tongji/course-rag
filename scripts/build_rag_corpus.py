import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "data" / "raw" / "video_transcripts" / "cleaned"
OUT_DIR = ROOT / "data" / "processed" / "rag_corpus"
INDEX_PATH = OUT_DIR / "index.jsonl"

NOISE_PATTERNS = [
    r"^各位同学[，,]大家好[。！!]?$",
    r"^同学们[，,]?$",
    r"^本节到此结束[，,。谢谢]*$",
    r"^谢谢[。！!]?$",
]

CONCEPT_PATTERNS = [
    r"(?:所谓)?([一-龥A-Za-z0-9《》（）()·]{2,28})(?:定义|是指|是：|指的是|称作|称为)([^。！？；\n]{4,160})",
    r"([一-龥A-Za-z0-9《》（）()·]{2,28})(?:包括|分为|由.+?构成|分别是)([^。！？；\n]{4,180})",
    r"([一-龥A-Za-z0-9《》（）()·]{2,28})(?:等于|计算公式|公式为)([^。！？；\n]{3,160})",
]

KEY_TERMS = [
    "软件工程经济学", "软件工程", "经济学", "经济主体", "软件质量", "软件特性", "决策模型",
    "成本估算", "软件规模估算", "工作量估算", "功能点", "COCOMO", "资金时间价值", "现值", "终值",
    "净现值", "内部收益率", "投资回收期", "独立方案", "互斥方案", "相关方案", "融资方式", "资金成本",
    "折旧", "摊销", "所得税", "费用", "效益", "供求", "定价", "财务分析", "盈亏平衡法",
    "期望净现值法", "敏感性分析", "决策树", "不确定性决策方法", "利息备付率", "偿债备付率",
    "项目投资现金流量表", "项目资本金现金流量表", "利润与利润分配表", "财务计划现金流量表",
]


def normalize_text(text: str) -> str:
    text = text.replace("﻿", "")
    lines = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            continue
        if any(re.match(pattern, line) for pattern in NOISE_PATTERNS):
            continue
        lines.append(line)
    joined = "".join(lines)
    joined = re.sub(r"\s+", " ", joined)
    joined = re.sub(r"([。！？；?])\s*", r"\1\n", joined)
    return joined.strip()


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[。！？；?])\n?", text) if s.strip()]


def parse_name(path: Path) -> tuple[str, str, str]:
    match = re.match(r"(?P<num>\d+)_(?P<lesson>[\d.]+)_(?P<topic>.+)", path.stem)
    if not match:
        return path.stem, "", path.stem
    return match.group("num"), match.group("lesson"), match.group("topic")


def compact_answer(sentences: list[str], max_chars: int = 900) -> str:
    answer = "".join(sentences).strip()
    if len(answer) <= max_chars:
        return answer
    cut = answer[:max_chars]
    last = max(cut.rfind("。"), cut.rfind("；"), cut.rfind("！"), cut.rfind("？"), cut.rfind("?"))
    return cut[: last + 1] if last > 200 else cut


def explicit_question_items(sentences: list[str], prefix: str) -> list[dict]:
    items = []
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        if "？" not in sentence and "?" not in sentence:
            i += 1
            continue

        question_part = re.split(r"[？?]", sentence, maxsplit=1)[0].strip() + "？"
        after = re.split(r"[？?]", sentence, maxsplit=1)[1].strip() if re.search(r"[？?]", sentence) else ""
        answer_sentences = []
        if after:
            answer_sentences.append(after)
        j = i + 1
        while j < len(sentences) and len("".join(answer_sentences)) < 700:
            if "？" in sentences[j] or "?" in sentences[j]:
                break
            answer_sentences.append(sentences[j])
            if len(answer_sentences) >= 5:
                break
            j += 1
        if answer_sentences:
            items.append({"question": question_part, "answer": compact_answer(answer_sentences), "kind": "explicit_question"})
        i = max(j, i + 1)
    return items


def concept_items(sentences: list[str]) -> list[dict]:
    items = []
    seen = set()
    text = "".join(sentences)

    for pattern in CONCEPT_PATTERNS:
        for match in re.finditer(pattern, text):
            term = re.sub(r"^(所谓|这里|这个|这一行|那|好|再接下来是|接下来是)", "", match.group(1)).strip("，。：: ")
            if not (2 <= len(term) <= 28):
                continue
            if re.search(r"[？?]|大家|老师|我们|你|这个|那个|一下|可以看到|有了|来源于哪里|给出|掌握|介绍|认为|看到|基于", term):
                continue
            if term.startswith(("程", "与", "和", "的", "是", "为", "了", "那", "这")):
                continue
            span_start = match.start()
            prefix_text = text[:span_start]
            sentence_idx = max(0, sum(1 for _ in re.finditer(r"[。！？；?]", prefix_text)) - 1)
            answer = compact_answer(sentences[sentence_idx : min(len(sentences), sentence_idx + 3)])
            question = f"{term}是什么？"
            key = (question, answer[:80])
            if len(answer) >= 30 and key not in seen:
                items.append({"question": question, "answer": answer, "kind": "concept_answer", "term": term})
                seen.add(key)

    for term in KEY_TERMS:
        candidates = [
            idx for idx, sentence in enumerate(sentences)
            if term in sentence and re.search(r"定义|是指|是：|指的是|称作|称为|包括|分为|等于|公式|指标|方法", sentence)
        ]
        if not candidates:
            continue
        idx = candidates[0]
        window = sentences[idx : min(len(sentences), idx + 4)]
        answer = compact_answer(window)
        if len(answer) < 30:
            continue
        question = f"{term}是什么？"
        key = (question, answer[:80])
        if key not in seen:
            items.append({"question": question, "answer": answer, "kind": "concept_answer", "term": term})
            seen.add(key)

    return items


def keywords_for(question: str, answer: str, topic: str) -> list[str]:
    text = question + answer
    keywords = [topic]
    for term in KEY_TERMS:
        if term in text and term not in keywords:
            keywords.append(term)
    for token in re.findall(r"[A-Za-z][A-Za-z0-9.\-]{1,20}", text):
        if token not in keywords:
            keywords.append(token)
    return keywords[:10]


def question_variants(question: str, term: str | None = None) -> list[str]:
    variants = [question]
    if term:
        variants.extend([f"请解释{term}", f"{term}有哪些要点？"])
    if question.startswith("为什么"):
        variants.append(question.replace("为什么", "原因是什么：", 1).rstrip("？") + "？")
    if question.startswith("如何") or "怎么" in question:
        variants.append(question.replace("如何", "怎样", 1))
    return list(dict.fromkeys(variants))[:4]


def build_file(path: Path) -> list[dict]:
    num, lesson, topic = parse_name(path)
    sentences = split_sentences(normalize_text(path.read_text(encoding="utf-8")))
    raw_items = explicit_question_items(sentences, num) + concept_items(sentences)

    unique = []
    seen_questions = set()
    for item in raw_items:
        q = re.sub(r"\s+", "", item["question"])
        if q in seen_questions:
            continue
        seen_questions.add(q)
        unique.append(item)

    chunks = []
    md = [
        "---",
        f'source_file: "{path.name}"',
        f'lesson: "{lesson}"',
        f'topic: "{topic}"',
        f'qa_count: {len(unique)}',
        'language: "zh-CN"',
        'corpus_type: "question_answer"',
        "---\n",
        f"# {lesson} {topic}\n",
    ]

    for idx, item in enumerate(unique, 1):
        term = item.get("term")
        chunk_id = f"{num}-{idx:03d}"
        title = item["question"].rstrip("？?")
        keywords = keywords_for(item["question"], item["answer"], topic)
        questions = question_variants(item["question"], term)
        content = f"问题：{item['question']}\n\n答案：{item['answer']}"
        summary = item["answer"][:180]
        chunk = {
            "chunk_id": chunk_id,
            "source_file": path.name,
            "lesson": lesson,
            "topic": topic,
            "title": title,
            "keywords": keywords,
            "questions": questions,
            "content": content,
            "summary": summary,
            "answer": item["answer"],
            "corpus_type": "question_answer",
            "extraction_type": item["kind"],
        }
        chunks.append(chunk)
        md.extend([
            f"## QA {idx:03d}: {title}\n",
            f"**chunk_id**: `{chunk_id}`  ",
            f"\n**source**: `{path.name}`  ",
            f"\n**lesson**: `{lesson}`  ",
            f"\n**topic**: {topic}  ",
            f"\n**extraction_type**: `{item['kind']}`\n",
            "\n**questions**",
            *[f"- {q}" for q in questions],
            "\n**keywords**",
            *[f"- {kw}" for kw in keywords],
            "\n**answer**\n",
            item["answer"],
            "\n**content**\n",
            content,
            "",
        ])

    (OUT_DIR / f"{path.stem}.md").write_text("\n".join(md), encoding="utf-8")
    return chunks


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()
    if INDEX_PATH.exists():
        INDEX_PATH.unlink()

    all_chunks = []
    failures = []
    for path in sorted(INPUT_DIR.glob("*.txt"), key=lambda p: p.name):
        try:
            all_chunks.extend(build_file(path))
        except Exception as exc:
            failures.append({"file": path.name, "error": repr(exc)})

    with INDEX_PATH.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    readme = f"""# 问题-答案型 RAG 语料

本目录由 `data/raw/video_transcripts/cleaned/` 中的网课转录生成。

## 生成策略

- 先把原始 txt 中被空格和换行打断的句子合并为连续文本。
- 优先提取转录中显式出现的问题句，并把问题后续的解释总结为答案。
- 对没有显式问题的核心概念、定义、公式、指标和报表，生成“X 是什么？”形式的问题，并从原文附近内容提取答案。
- 不引入外部知识，只使用原始转录内容。

## 统计

- 输入文件数：{len(list(INPUT_DIR.glob('*.txt')))}
- QA chunk 数：{len(all_chunks)}
- 失败文件数：{len(failures)}

## 字段

`index.jsonl` 每行一个 QA chunk，主要字段包括 `chunk_id`、`source_file`、`lesson`、`topic`、`title`、`questions`、`keywords`、`answer`、`content`、`summary`、`extraction_type`。
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")
    stats = {"input_files": len(list(INPUT_DIR.glob("*.txt"))), "qa_chunks": len(all_chunks), "failures": failures}
    (OUT_DIR / "_generation_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
