# RPA.GraphicStock

## Investimentos e conversor de moedas
De uns anos pra cá, um assunto muito discutido nas redes sociais é investimento. Nesse universo, existem centenas de possibilidades, desde aquelas para públicos que preferem aplicações sem muitos riscos, com baixa rentabilidade, até aquelas que têm mais riscos, mas, em contrapartida, possuem rentabilidade maior. 

Outra aplicação que tem se tornado interessante, é a compra de moedas de outros países.

 RPA.GraphicStock é uma API que traz informações sobre determinado investimento e conversões de moeda. Suportando 2 paises para consulta de investimentos, ele captura informações do comportamento desses investimentos em um ano definido e devolve um gráfico de linha, em que o eixo x são os meses e o eixo y, a rentabilidade. Os dois investimentos devem estar no mesmo gráfico. A API, conta com um endpoint POST, em que, de  acordo com o parametro de moeda de retorno desejada será convertido um valor enviado em real para uma moeda USD ou vice e versa.
