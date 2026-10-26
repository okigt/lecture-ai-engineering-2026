from app.ask import ask
from app.config import MODEL


class FakeUsageMetadata:
    prompt_token_count = 12
    candidates_token_count = 34


class FakeResponse:
    usage_metadata = FakeUsageMetadata()
    text = "こんにちは、AIです。"


class FakeModels:
    @staticmethod
    def generate_content(model, contents):
        assert model == MODEL
        assert contents == "テスト質問"
        return FakeResponse()


class FakeClient:
    def __init__(self, api_key):
        assert api_key == "test-api-key"

    models = FakeModels


def test_ask_prints_usage_and_response_time(monkeypatch, capsys):
    monkeypatch.setattr("app.ask.get_api_key", lambda: "test-api-key")
    monkeypatch.setattr("app.ask.genai.Client", FakeClient)
    timings = iter([100.0, 100.75])
    monkeypatch.setattr("app.ask.time.perf_counter", lambda: next(timings))

    result = ask("テスト質問")

    captured = capsys.readouterr().out
    assert result == "こんにちは、AIです。"
    assert "[入力トークン数] 12" in captured
    assert "[出力トークン数] 34" in captured
    assert "[API応答時間] 0.75 秒" in captured
