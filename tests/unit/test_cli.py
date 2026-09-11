from ftm_kpe.cli import build_parser


def test_cli_defaults_match_the_legacy_configuration() -> None:
    args = build_parser().parse_args(["--text", "example document"])

    assert args.language == "en"
    assert args.top_k == 15
    assert args.clustering == "fcm"
    assert args.quantifier == "pasi"
    assert args.selection == "2"
