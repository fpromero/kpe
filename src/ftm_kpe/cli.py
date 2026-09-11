"""Command-line access to the imported research prototype."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract keyphrases with the imported FTM-KPE research prototype."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--text", help="Text to process directly.")
    input_group.add_argument("--input-file", type=Path, help="UTF-8 text file to process.")
    parser.add_argument("--language", choices=("en", "es"), default="en")
    parser.add_argument("--top-k", type=int, default=15)
    parser.add_argument("--top-topic", type=float, default=0.75)
    parser.add_argument("--clustering", choices=("fcm", "dbs", "hac", "ms"), default="fcm")
    parser.add_argument("--quantifier", choices=("pasi", "feng", "alh"), default="pasi")
    parser.add_argument(
        "--selection",
        choices=("1", "2", "3", "4"),
        default="2",
        help="1=first, 2=frequency, 3=centroid, 4=combined.",
    )
    parser.add_argument("--bert-model", default="bert-base-uncased")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = args.text
    if args.input_file is not None:
        text = args.input_file.read_text(encoding="utf-8")

    from transformers import BertModel

    from .legacy.kpe_control import key_phrases_extraction

    bert_model = BertModel.from_pretrained(args.bert_model, output_hidden_states=True)
    sentences, topics, keyphrases, relevance = key_phrases_extraction(
        text,
        language=args.language,
        clustering_option=args.clustering,
        top_topic=args.top_topic,
        top_kp=args.top_k,
        quantifier=args.quantifier,
        select_option=args.selection,
        bert_model=bert_model,
    )
    output = {
        "keyphrases": list(keyphrases),
        "relevance": relevance,
        "topics": topics,
        "sentence_count": len(sentences),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
