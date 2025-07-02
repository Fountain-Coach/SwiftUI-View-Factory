import json
from click.testing import CliRunner
from cli.vi import cli


def test_generate_parses_options(monkeypatch):
    runner = CliRunner()
    recorded = {}

    def fake_post(url, json=None, timeout=30):
        recorded['url'] = url
        recorded['json'] = json
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return {"swift": ""}
        return Resp()

    monkeypatch.setattr('cli.vi.requests.post', fake_post)
    with runner.isolated_filesystem():
        layout_path = 'layout.json'
        with open(layout_path, 'w') as f:
            json.dump({"type": "Text", "text": "Hello"}, f)
        result = runner.invoke(
            cli,
            [
                '--server', 'http://localhost',
                'generate', layout_path,
                '--name', 'HomeView',
                '--backend-hooks',
                '--font', 'title',
                '--color', 'blue',
                '--spacing', '8',
                '--indent', '4',
                '--no-header',
            ]
        )
        assert result.exit_code == 0
        assert recorded['url'].endswith('/factory/generate')
        assert recorded['json']['name'] == 'HomeView'
        assert recorded['json']['backend_hooks'] is True
        assert recorded['json']['style'] == {
            'font': 'title',
            'color': 'blue',
            'spacing': 8,
            'indent': 4,
            'header_comment': False,
        }


def test_generate_verify_build(monkeypatch):
    runner = CliRunner()
    calls = []

    def fake_post(url, json=None, timeout=30):
        calls.append(url)

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                if url.endswith('/factory/generate'):
                    return {"swift": "code"}
                return {"success": True, "log": ""}

        return Resp()

    monkeypatch.setattr('cli.vi.requests.post', fake_post)
    with runner.isolated_filesystem():
        layout_path = 'layout.json'
        with open(layout_path, 'w') as f:
            json.dump({"type": "Text"}, f)
        result = runner.invoke(cli, ['generate', layout_path, '--verify-build'])

        assert result.exit_code == 0
        assert calls[0].endswith('/factory/generate')
        assert calls[1].endswith('/factory/test-build')
