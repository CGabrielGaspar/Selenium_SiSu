import requests
import json

url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicoes'

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.content)
    print(data)
    vagas = data['vagas']
    for vaga in vagas:
        print(f"Campus: {vaga['campus']}")
        print(f"Curso: {vaga['curso']}")
        print(f"Turno: {vaga['turno']}")
        print(f"Vagas totais: {vaga['totalVagas']}")
        print(f"Vagas ocupadas: {vaga['vagasOcupadas']}")
        print(f"Vagas disponíveis: {vaga['vagasDisponiveis']}")
        print("----")
else:
    print("Erro ao consultar API do SiSU.")