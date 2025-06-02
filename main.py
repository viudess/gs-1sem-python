"""
Nome dos integrantes:
Eduardo Viudes Chorro - RM: 564075
Victor Tadashi Saito Barra - RM: 563582
Frederico de Paula Dias - RM: 562109
"""
# Biblioteca para fazer requisições HTTP

import requests  

# Chave da API do OpenWeatherMap
API_KEY = "72c43e45c8bace32e93b148333e30e7d"

# Dicionário com alguns estados brasileiros, contendo cidade, latitude e longitude
ESTADOS = {
    "AC": {"cidade": "Rio Branco", "lat": -9.9754, "lon": -67.8243},
    "AL": {"cidade": "Maceió", "lat": -9.6658, "lon": -35.7350},
    "AM": {"cidade": "Manaus", "lat": -3.1190, "lon": -60.0217},
    "AP": {"cidade": "Macapá", "lat": 0.0349, "lon": -51.0694},
    "BA": {"cidade": "Salvador", "lat": -12.9714, "lon": -38.5014},
    "CE": {"cidade": "Fortaleza", "lat": -3.7172, "lon": -38.5433},
    "DF": {"cidade": "Brasília", "lat": -15.7939, "lon": -47.8828},
    "ES": {"cidade": "Vitória", "lat": -20.3155, "lon": -40.3128},
    "GO": {"cidade": "Goiânia", "lat": -16.6869, "lon": -49.2648},
    "MA": {"cidade": "São Luís", "lat": -2.5307, "lon": -44.3068},
    "MG": {"cidade": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
    "MS": {"cidade": "Campo Grande", "lat": -20.4697, "lon": -54.6201},
    "MT": {"cidade": "Cuiabá", "lat": -15.6010, "lon": -56.0974},
    "PA": {"cidade": "Belém", "lat": -1.4558, "lon": -48.4902},
    "PB": {"cidade": "João Pessoa", "lat": -7.1195, "lon": -34.8450},
    "PE": {"cidade": "Recife", "lat": -8.0476, "lon": -34.8770},
    "PI": {"cidade": "Teresina", "lat": -5.0892, "lon": -42.8016},
    "PR": {"cidade": "Curitiba", "lat": -25.4284, "lon": -49.2733},
    "RJ": {"cidade": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    "RN": {"cidade": "Natal", "lat": -5.7945, "lon": -35.2110},
    "RO": {"cidade": "Porto Velho", "lat": -8.7608, "lon": -63.8999},
    "RR": {"cidade": "Boa Vista", "lat": 2.8235, "lon": -60.6753},
    "RS": {"cidade": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
    "SC": {"cidade": "Florianópolis", "lat": -27.5954, "lon": -48.5480},
    "SE": {"cidade": "Aracaju", "lat": -10.9472, "lon": -37.0731},
    "SP": {"cidade": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    "TO": {"cidade": "Palmas", "lat": -10.1830, "lon": -48.3336}
}

def exibir_estados_disponiveis():
    """Exibe os estados disponíveis para consulta."""
    print("=== Estados disponíveis ===")
    for sigla in ESTADOS:
        print(f"- {sigla}")

def obter_estado_usuario():
    """Pede para o usuário digitar uma sigla de estado e valida se é válida."""
    sigla = input("Digite a sigla do estado (ex: SP): ").strip().upper()
    if sigla not in ESTADOS:
        print("Estado inválido. Encerrando.")
        exit()
    return sigla

def montar_url(lat, lon):
    """
    Monta a URL da API do OpenWeatherMap com base na latitude e longitude do estado.
    """
    return (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    )

def buscar_previsao(url):
    """
    Faz a requisição à API e retorna os dados de previsão do tempo.
    Se houver erro, encerra o programa com mensagem.
    """
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Levanta erro caso o status da resposta não seja 200
        return resposta.json()       # Retorna os dados da API no formato JSON
    except requests.RequestException as erro:
        print(f"Erro na requisição: {erro}")
        exit()

def calcular_chuva_total(dados):
    """
    Percorre a previsão para os próximos dias e soma a quantidade total de chuva.
    A API retorna previsão a cada 3h, e o campo de chuva pode não estar presente sempre.
    """
    chuva_total = 0.0
    for previsao in dados.get("list", []):  # Percorre todas as previsões de 3h
        chuva = previsao.get("rain", {}).get("3h", 0.0)  # Pega a chuva em mm ou 0.0 se não houver
        chuva_total += chuva
    return round(chuva_total, 1)

def determinar_risco(chuva):
    """
    Determina o nível de risco com base na quantidade total de chuva:
    - Baixo: até 50 mm
    - Moderado: entre 50 e 100 mm
    - Alto: acima de 100 mm
    """
    if chuva > 100:
        return "Alto"
    elif chuva > 50:
        return "Moderado"
    return "Baixo"

def sugerir_prevencao(risco):
    """
    Retorna uma recomendação com base no nível de risco identificado.
    """
    sugestoes = {
        "Alto": "Evite áreas de risco. Fique atento a alertas da defesa civil.",
        "Moderado": "Mantenha atenção ao clima e evite deslocamentos desnecessários.",
        "Baixo": "Nenhuma ação urgente necessária, mas continue acompanhando a previsão."
    }
    return sugestoes.get(risco, "")

def main():
    """
    Função principal que coordena a execução do programa.
    """
    print("=== Consulta Climática e Análise de Risco ===")
    exibir_estados_disponiveis()  # Lista os estados disponíveis

    sigla = obter_estado_usuario()      # Recebe a sigla digitada pelo usuário
    estado = ESTADOS[sigla]             # Obtém os dados da cidade escolhida

    print(f"\nBuscando previsão para {estado['cidade']}...\n")

    url = montar_url(estado["lat"], estado["lon"])  # Monta a URL da requisição
    dados = buscar_previsao(url)                    # Faz a chamada à API e obtém os dados

    chuva_total = calcular_chuva_total(dados)       # Calcula a chuva total prevista
    risco = determinar_risco(chuva_total)           # Determina o nível de risco
    recomendacao = sugerir_prevencao(risco)         # Gera uma recomendação com base no risco

    # Exibe os resultados ao usuário
    print(f"Total de chuva prevista: {chuva_total} mm")
    print(f"Nível de risco: {risco}")
    print(f"Recomendação: {recomendacao}")

# Verifica se este arquivo está sendo executado diretamente
if __name__ == "__main__":
    main()
