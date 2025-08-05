''' Verificador de IP (IPv4) desenvolvido por Mathias Petry '''

# Biblioteca padrão do Python para trabalhar com endereços IP
import ipaddress

# Essa biblioteca foi instalada no ambiente virtual para acessar páginas/APIs a partir do código
import requests

# Transforma a string do input em um IP analisável, ou a invalida
def validar_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv6Address):
            print(f"Você inseriu um endereço IPv6: {ip}")
            print("Infelizmente, este programa analisa apenas endereços IPv4. Por favor, digite um IPv4 válido.")
            return None
        return ip_obj
    except ValueError:
        print(f"IP inválido: {ip}")
        return None


# Verifica se o IP é privado
def verificar_privado(ip_obj):
    return ip_obj.is_private

''' O primeiro octeto do IP (exemplo: 192.xxx.x.x) é analisado e separado por classe,
só com isso, já é possível verificar se é um ip privado, se é um tipo de ip especial, o tamanho provável da rede etc. '''

def identificar_classe(ip_obj):
    primeiro_octeto = int(str(ip_obj).split('.')[0])
    if 1 <= primeiro_octeto <= 126:
        return "Classe A"
    elif 128 <= primeiro_octeto <= 191:
        return "Classe B"
    elif 192 <= primeiro_octeto <= 223:
        return "Classe C"
    elif 224 <= primeiro_octeto <= 239:
        return "Classe D (Multicast)"
    elif 240 <= primeiro_octeto <= 255:
        return "Classe E (Reservado)"
    else:
        return "Indefinida"

# Confere se o IP se enquadra como "especial" usado para algum dos segmentos abaixo
def verificar_especial(ip_obj):
    if ip_obj.is_loopback:
        return "Loopback"
    if ip_obj.is_multicast:
        return "Multicast"
    if ip_obj.is_reserved:
        return "Reservado"
    if ip_obj.is_unspecified:
        return "Indefinido (0.0.0.0)"
    if ip_obj.is_link_local:
        return "Link Local (APIPA)"
    return "Normal"

# Analisa o IP dado e a sua máscara, que permitem calcular o IP de rede, broadcast, quantos hosts cabem e o intervalo de IPs válidos.
def analisar_rede(ip_str, mascara="/24"):
    rede = ipaddress.ip_network(ip_str + mascara, strict=False)
    return {
        "Rede": str(rede.network_address),
        "Broadcast": str(rede.broadcast_address),
        "Total de hosts": rede.num_addresses - 2,
        "Intervalo de hosts": f"{list(rede.hosts())[0]} - {list(rede.hosts())[-1]}"
    }

# Se for um IP público, é enviado uma solicitação HTTP ao site "ipinfo" e o código traz as informações de localização diretamente da API.
def geolocalizar_ip(ip):
    try:
        resposta = requests.get(f"https://ipinfo.io/{ip}/json")
        if resposta.status_code == 200:
            dados = resposta.json()
            return {
                "País": dados.get("country"),
                "Região": dados.get("region"),
                "Cidade": dados.get("city"),
                "Organização": dados.get("org"),
                "ASN": dados.get("asn", {}).get("asn", "Desconhecido"),
                "Localização": dados.get("loc"),
                "Provedor": dados.get("org"),
                "Hostname": dados.get("hostname")
            }
        else:
            return {"Erro": "Falha ao consultar IP"}
    except Exception as e:
        return {"Erro": str(e)}
    

# Execução para interação através do terminal e impressão das informações
while True:
    ip_input = input("Digite um IPv4 para análise: ")
    ip_obj = validar_ip(ip_input)
    if ip_obj:
        break


if ip_obj:
    print(f"\nIP válido: {ip_obj}")
    print(f"Tipo: {'Privado' if verificar_privado(ip_obj) else 'Público'}")
    print(f"Classe: {identificar_classe(ip_obj)}")
    print(f"Categoria especial: {verificar_especial(ip_obj)}")

    if not ip_obj.is_private:
        print("\nGeolocalização e ASN:")
        geo = geolocalizar_ip(str(ip_obj))
        for chave, valor in geo.items():
            print(f"{chave}: {valor}")

    print("\nInformações de Rede (/24):")
    rede_info = analisar_rede(str(ip_obj))
    for chave, valor in rede_info.items():
        print(f"{chave}: {valor}")
