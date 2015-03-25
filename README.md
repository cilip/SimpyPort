# SimpyPort
Modelo de simulação portuária baseada em Simpy

Todo terminal portuário por ser representado abstratamente por um conjunto de 7 sistemas:
- chegada de navios;
- recepção de carga marítima;
- movimentação da carga de e para o navio;
- armazenagem;
- movimentação de e para os modais terrestres;
- recepção de carga terrestre;
- chegada de veículos pelo modal terrestre.

Pretende-se construir um modelo de simulação computacional capaz de representar genericamente um terminal portuário que contemple cada um dos 7 subsistemas. É evidente que não se pretende uma representação completa e definitiva de qualquer terminal existente, mas sim, um modelo que represente uma versão simplificada de um terminal portuário, seja válido (os parâmetros de saída sejam coerentes com dados reais) e, principalmente, que seja expansível, no sentido de que caso se necessite de uma representação mais refinada de algum dos subsistemas, isso seja possível a partir do código já construído. 
Caracterização do porto a ser modelado
O porto a ser construído terá as seguintes características:
- Carga geral, podendo movimentar três tipos de carga: granel sólido, granel líquido e contêiner;
- As embarcações podem tanto embarcar quando desembarcar qualquer um dos tipos de cargas, mas nunca simultaneamente;
- Os berços possuem restrições quanto ao porte da embarcação;
- Alguns berços, por pertencerem ao mesmo píer, podem receber 1 ou mais embarcações simultaneamente, a depender do comprimento da embarcação;
- Toda operação de carga/descarga necessita de recursos para se iniciar;
- Os estoques são limitados;
- A recepção de carga terrestre por ser por duto, caminhões ou trens;
- etc.

O modelo será desenvolvido em espiral, subdividida internamente em etapas. 
 
As etapas são aquelas que abstratamente definem um terminal portuário e são executadas em sequência. Na primeira volta da espiral de projeto, são elaborados os códigos necessários para uma versão simplificada do porto pretendido. O objetivo, nesta primeira volta, é compreender melhor o sistema e terminar com um porto mínimo: navios de tamanho constante descarregam, a carga é transferida para o estoque e sai por caminhão.
Para facilitar o desenvolvimento, a cada etapa é estabelecido um modelo conceitual que deve ser implementado e alguns parâmetros de saída que se atingidos, atestam que o objetivo da etapa foi atendido.

Este repositório está dividido por "voltas" da espiral.  Dentro de cada volta, estão os códigos desenvolvidos para aquela etapa.



