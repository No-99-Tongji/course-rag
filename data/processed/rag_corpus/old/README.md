# 问题-答案型 RAG 语料

本目录由 `data/raw/video_transcripts/cleaned/` 中的网课转录生成。

## 生成策略

- 先把原始 txt 中被空格和换行打断的句子合并为连续文本。
- 优先提取转录中显式出现的问题句，并把问题后续的解释总结为答案。
- 对没有显式问题的核心概念、定义、公式、指标和报表，生成“X 是什么？”形式的问题，并从原文附近内容提取答案。
- 不引入外部知识，只使用原始转录内容。

## 统计

- 输入文件数：37
- QA chunk 数：432
- 失败文件数：0

## 字段

`index.jsonl` 每行一个 QA chunk，主要字段包括 `chunk_id`、`source_file`、`lesson`、`topic`、`title`、`questions`、`keywords`、`answer`、`content`、`summary`、`extraction_type`。
