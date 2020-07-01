import program.download_agents as script
import urllib.request
from io import BytesIO
import json

# test1 que get_agents() renvoie la liste des agents demandés

def test_http_result(tmpdir, monkeypatch):
    results = [{"age": 84, "agreeableness": 0.74}]

    def mockreturn (request):
        return BytesIO(json.dumps(results).encode())

    monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

    assert script.get_agents(1) == results
    
# test2 que main() a bien pour effet d'ecrire la liste des agents dans un fichier json séparé

    p = tmpdir.mkdir("program").join("agents.json")
    # run script
    script.main(["--dest", str(p), "--count", "1"])

    with open(str(p), 'r') as f:
        local_res = json.load(f)

    assert local_res == script.get_agents(1)