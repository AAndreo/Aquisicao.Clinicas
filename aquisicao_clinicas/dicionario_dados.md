# **Dicionário de Dados**

## **Clinics**
* CLINIC_ID: Identificador da clinica.

* CLINIC_CREATED_AT: Data e horário em que a clínica foi cadastrada no sistema.

* BUSINESS_SEGMENTATION: Segmentação de negócio ao qual a clínica pertence.

* IS_CHAIN_CLINIC: Indica se a clínica faz parte de uma grande rede ou franquia.

* FIRST_USER_HUBSPOT_SOURCE: Fonte inicial pela qual o usuário descobriu ou foi adquirido pela clínica (por exemplo, publicidade, referência, etc.). 

* INTEREST_REASONS: Razões de interesse expressas pela clínica.

* INTEREST_CATEGORY_SIGNUP: Categoria de interesse desejada. 

* HAS_INTEREST_BNPL: Tem interesse em BNPL (Compre agora, pague depois)? 

* HAS_INTEREST_BNPL_ONLY: Tem interesse somente em BNPL (Compre agora, pague depois)? 

* HAS_INTEREST_SAAS: Tem interesse em SaaS (Software as a Service)? 

* TRIAL_DURATION: Duração do periodo trial em dias.

* TRIAL_START_DATE: Data de início do periodo trial.

* TRIAL_END_DATE: Data de término do periodo trial.

* TRIAL_START_HOUR: Hora do início do periodo trial.

* TRIAL_START_HOUR_CATEGORY: Categoria do horário de início do período de teste gratuito (manhã, tarde, noite).

* TRIAL_START_DAY_OF_WEEK: Dia da semana de início do período trial.

* TRIAL_START_DAY_OF_WEEK_CATEGORY: Categoria do dia da semana do início do perídodo trial.
    * ['Weekday' (dia da semana), 'Weekend' (fim de semana)]

* HAS_USER_CREATED: Indica se um usuário foi criado dentro do sistema da clínica. 

* MARKETING_ATTRIBUITION: Atribuição de canal de marketing relacionada à aquisição do usuário.

* MARKETING_ATTRIBUITION_CHANNEL_GROUP: Grupo de canais de marketing utilizados para a aquisição do usuário.

* MARKETING_ATTRIBUITION_CAMPAIGN: Campanha de marketing relacionada à aquisição do usuário.

* MARKETING_ATTRIBUITION_CAMPAIGN_PRODUCT: Produto atribuido da campanha de marketing que levou à aquisição do usuário.

* MARKETING_ATTRIBUITION_AD_GROUP: Grupo de anúncios da campanha de marketing que levou à aquisição do usuário.

* IS_PAID_MEDIUM: Indica se o meio pelo qual o usuário foi adquirido era pago. 

* HAS_ASKED_FOR_ACCREDITATION: Indica se a clínica pediu por credenciamento.

* IS_ACCREDITATION_APPROVED: Credenciamento da clínica foi aprovado?

* IS_ACCREDITATION_REPROVED: Credenciamento da clínica foi reprovado?

* CLINIC_ACCREDITATION_STATUS: Status de credenciamento da clinica.

* REQUEST_FINISHED_AT: Data e horário em que um determinado pedido ou ação foi concluído.

* ACCREDITATION_REQUESTED_AT: Data de solicitação de credenciamento pela clínica.

* ACCREDITATION_APPROVED_AT: Data de aprovação do credenciamento.

* ACCREDITATION_REJECTED_AT: Data de rejeição do credenciamento.

## **Subscriptions**
* CLINIC_ID: Identificador da clinica

* STRIPE_SUBSCRIPTION_ID: Identificador único da assinatura dentro do sistema de pagamento Stripe.

* SUBSCRIPTION_START_DATE: Inicio da assinatura

* SUBSCRIPTION_END_DATE: Termino da assinatura

* SUBSCRIPTION_CURRENT_PERIOD_STARTED_AT: Data de início do período atual de pagamento dentro da assinatura.

* SUBSCRIPTION_CURRENT_PERIOD_ENDS_AT: Data de término do período atual de pagamento dentro da assinatura.

* MOST_RECENT_INVOICE_CREATED_AT: Data de criação da fatura mais recente associada à assinatura.

* LAST_PAYMENT_AT: Data do ultimo pagamento realizado.

* CHECKOUT_STATUS: Status do processo de pagamento/checkout.

* SUBSCRIPTION_STATUS: Status atual da assinatura.

* BILLING_INTERVAL_IN_MONTHS: Intervalo em meses da frequência dos pagamentos
    * [ 1, 12, 6]

* FIRST_PAYMENT_METHOD_TYPE: Metodo do primeiro pagamento

* FIRST_CARD_BRAND: Bandeira do cartão utilizado no primeiro pagamento
    * ['mastercard', 'visa', nan]

* FIRST_PAYMENT_AMOUNT: Valor do primeiro pagamento

* FIRST_PAYMENT_AMOUNT_OFF: Desconto do valor do primeiro pagamento

* FIRST_PAYMENT_PROMOTION_CODE: Cupom de codigo para o primeiro pagamento

* FIRST_PAYMENT_COUPON_ID: Identificador do cupom

* FIRST_PAYMENT_AMOUNT_OFF_2: Outro desconto do valor do primeiro pagamento

## **Activity**
* CLINIC_ID: Identificador da clinica

* ACTIVITY_AT: Data e hora que a atividade foi feita

* ACTIVITY_TYPE: Tipo da atividade

* FEATURE: Funcionalidade do sistema onde a atividade esta relacionada.

* MODULE: Módulo do sistema ou parte do produto em que a atividade ocorreu.

* ANALYTICS_DOMAIN: Domínio analítico (categoria da atividade realizada)
    * ['patient', 'scheduling', 'setup', 'finance', 'bnpl']

* IS_TRANSACTION: É um transação financeira?
    * [False, True]

* IS_BNPL_ACTIVITY: É uma atividade BNPL?
    * [False, True]

* IS_VALID_ACTIVITY: É uma atividade valida?
    * [True, False]

* IS_DELETION_ACTIVITY: É uma atividade de exclusão?
    * [True, False]

* IS_MANAGEMENT_ACTIVITY: É uma atividade de gerenciamento?
    * [True, False]

* IS_FINANCE_ACTIVITY: É uma atividade de finança?
    * [True, False]