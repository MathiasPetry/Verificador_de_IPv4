Desenvolvi esse projeto de back-end com Python com o intuito de poder visualizar algumas informações relevantes que podemos obter ao inserir o nosso IP, no caso deste projeto um IPv4 especificamente.
Tive essa ideia durante alguns estudos sobre redes e pensei que poderia ser algo legal para trabalhar um pouco com Python em uma aplicação diferente do que costumava produzir.

 Este projeto:
 - Verifica se o IP é válido
- Diz se é público ou privado
- Classifica o IP (Classe A, B, C...)
- Detecta IPs especiais (loopback, multicast etc.)
- Retorna geolocalização de IPs públicos via API
- Calcula rede, broadcast e intervalo de hosts

Neste projeto, a classificação do IP (A, B, C, D ou E) é usada de forma didática 
com base no primeiro octeto do endereço IPv4.

Essa abordagem, conhecida como "classful addressing", foi amplamente utilizada até a adoção do CIDR (Classless Inter-Domain Routing) nos anos 1990, que tornou as classes oficialmente obsoletas para roteamento moderno.

Apesar disso, o conceito de classes ainda é útil para fins de estudo, entendimento geral sobre faixas de IPs, identificação rápida de redes privadas e categorização básica de endereços IPv4. 

Este projeto utiliza as classes exclusivamente para esse propósito.


Desenvolvido por Mathias Petry.
