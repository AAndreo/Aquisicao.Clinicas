# Análise de dados de aquisição de clínicas.

## Contexto

A Real constrói uma plataforma de trabalho (SaaS - Software as a Service) focada especificamente em clínicas odontológicas, onde os dentistas e proprietários de clínica encontram todos os serviços necessários para gerir suas operações. Nosso software oferece uma agenda moderna, prontuário eletrônico e ficha de pacientes, além de acesso a gestão financeira e muito mais!

Nosso fluxo de aquisição de novos clientes funciona assim:  o usuário pode se cadastrar diretamente ou pedir para conversar com um especialista antes disso. Uma vez cadastrado, ele tem acesso a um período de teste do produto (trial) onde pode usar todas as nossas funcionalidades antes de assinar. Uma vez terminado seu período de testes, ele só poderá usar o produto quando assinar. O foco deste case será entender o período de trial e como ele pode ser melhorado.

![alt text](<imgs/Screen Shot 2023-11-13 at 11.37.14.png>)

Uma das funcionalidades mais populares de nosso produto, e considerada um diferencial, é o **Financiamento** Real, onde a Real financia o tratamento de um paciente sem riscos para a clínica, e o paciente paga para a Real em até 36 vezes (basicamente funcionando como um empréstimo). Este produto também é conhecido internamente como **Buy now, pay later** (BNPL).

Desta forma, deve ser mencionada a existência do credenciamento. O processo de **credenciamento** é uma validação de identidade da clínica, que a Real faz antes de aprovar ela para o uso do nosso financiamento. É um processo anti-fraude e que nos permite avaliar de maneira mais assertiva os riscos de realizar financiamentos para clientes dessa clínica.

![alt text](<imgs/Screen Shot 2023-11-13 at 11.37.29.png>)

## O que precisa ser feito?
Seu objetivo é trazer as principais métricas relacionadas à aquisição de clínicas, realizando uma análise de dados exploratória com essa base, de forma a identificar gargalos e oportunidades para otimizar a entrada de clinicas na Real.

Você terá a sua disposição três datasets da Real que representam elementos de nossa base transacional de informações. Será necessário unir estes modelos da maneira correta para poder analisar o período de trial.

Os arquivos incluem as clínicas que se cadastraram nos meses de **Agosto** e **Setembro** de **2023**, e suas interações até a data de extração (18/10/2023). A tabela clinics contém informações sobre as clínicas cadastradas e alguns marcos temporais delas, como trial e credenciamento. Aqui vale citar que a Real possui algumas parcerias com grandes redes e franquias de clínicas odontológicas pelo Brasil (diferenciadas das outras por colunas como `business_segmentation` e `is_chain_clinic`). Essas clínicas usam apenas o Financiamento Real, e desta forma devem ser removidas de análises sobre conversão de assinaturas

A tabela subscriptions contém informações de **assinaturas** de clínicas. A assinatura é definida como o início de um esquema de pagamentos recorrentes, possuindo início, data de fim (caso tenha sido encerrada) e a recorrência de pagamentos. Se uma clínica começar uma assinatura, encerrar ela e depois voltar a ser assinante, ela terá múltiplas linhas de assinatura.

A tabela activity registra todas as **atividades** realizadas pela clínica, contendo registros temporais de quando a clínica desempenhou uma determinada ação. Temos diversos tipos de atividades no produto, que por sua vez estão organizadas em níveis hierarquicos para facilitar nosso trabalho com elas. Esses níveis estão disponíveis na tabela ( module , analytics_domain , feature ). As atividades também são divididas entre atividades válidas ou não, por uma questão de conveniência: algumas métricas são calculadas apenas considerando atividades “validas” e outras não. Esta extração contém apenas atividades realizadas em período de trial.

## Entregas
Os entregáveis deste case são:

Um modelo de dados que agregue informações sobre a entrada da clínica e seu período de trial até a eventual conversão. Este deve ser um modelo que facilite a construção de dashboards para aquisição e a sua análise dos dados.

Um Dashboard operacional para o time de Produto - Aquisição acompanhar este processo, com gráficos e números gerais a serem monitorados diariamente e semanalmente (aqui, a entrega pode ser uma imagem dos seus gráficos e como estão dispostos, mas usando nossos dados reais)

Uma breve apresentação de sua análise exploratória, incluindo informações relevantes sobre a operação, e oportunidades de otimização encontradas.