-- Métricas de Conversão no Trial
with num_clinicas_convertidas as
(
	select count(distinct cli.clinic_id) as num_clinicas_convertidas
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
)
, clinicas_convertidas as
(
	select distinct cli.clinic_id as num_clinicas_convertidas
	, subscription_start_date
	, subscription_end_date
	, trial_start_date
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
)
, num_clinicas_unicas_periodo_trial as
(
	select count(distinct cli.clinic_id) num_clinicas_unicas_periodo_trial
	from clinics cli
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
)
, clinicas_convertidas_com_atividades as
(
	select distinct cli.clinic_id,
	act.feature
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
	and act.is_valid_activity is true
)
, total_clinicas_convertidas_com_atividades as
(
	select count(distinct cli.clinic_id) as num_clinicas_convertidas
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
	and act.is_valid_activity is true
)
, num_atividades_por_clinica_convertida as
(
	select cli.clinic_id, count(*) as num_atividades
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
	and act.is_valid_activity is true
	group by cli.clinic_id
	order by 2 desc
)
, num_atividades_por_clinica_nao_convertida as
(
	select cli.clinic_id, count(*) as num_atividades
	from clinics as cli
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and act.is_valid_activity is true
	and not exists (select sub.clinic_id from subscriptions as sub where sub.clinic_id = cli.clinic_id)
	group by cli.clinic_id
	order by 2 desc
)
, trial_duration as
(
	select cli.clinic_id
	,cli.trial_duration
	,case 
		when cli.trial_duration <= 7 then 'Até 7 dias'
		when (cli.trial_duration > 7 and cli.trial_duration <= 14) then 'Entre 8 e 14 dias'
		when cli.trial_duration > 14 then 'Acima de 14 dias'
	end as trial_duration_interval
	from clinics as cli
	inner join subscriptions as sub on sub.clinic_id = cli.clinic_id
	inner join activity act on act.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and sub.stripe_subscription_id is not null
)


select * from num_clinicas_convertidas

select * from num_clinicas_unicas_periodo_trial

-- # Percentual de clínicas que convertem para assinaturas pagas após o trial. 
-- # A conversão requer um registro de assinatura onde STRIPE_SUBSCRIPTION_ID seja diferente de NaN, não importando o status.
select round((num_clinicas_convertidas::numeric / (select num_clinicas_unicas_periodo_trial from num_clinicas_unicas_periodo_trial))*100,2) as porcentagem
from num_clinicas_convertidas

-- # Tempo médio desde o início do trial até a conversão para assinatura paga.
select round(avg(subscription_start_date - trial_start_date),2) as media
from clinicas_convertidas

-- # Comparação de conversão entre clínicas que realizaram um número alto de atividades versus um número baixo.
select perc_ate_50_atividades,perc_entre_51_100_atividades,perc_acima_100_atividades
from
(select round((count(*)::numeric / (select num_clinicas_convertidas from total_clinicas_convertidas_com_atividades))*100,2) as perc_ate_50_atividades
	from  num_atividades_por_clinica_convertida
 	where num_atividades <= 50) as ate_50_atividades
,(select round((count(*)::numeric / (select num_clinicas_convertidas from total_clinicas_convertidas_com_atividades))*100,2) as perc_entre_51_100_atividades
	from  num_atividades_por_clinica_convertida
	where (num_atividades > 50 and num_atividades <= 100) ) as entre_51_100_atividades
,(select round((count(*)::numeric / (select num_clinicas_convertidas from total_clinicas_convertidas_com_atividades))*100,2) as perc_acima_100_atividades
	from  num_atividades_por_clinica_convertida
	where (num_atividades > 100)) as acima_100_atividades

-- # Identificação de atividades que têm maior correlação com a conversão (e.g., clínicas que usam a gestão financeira têm maior chance de converter).
select cc.feature,
count(*) as frequencia,
round((count(*)::numeric / (select num_clinicas_convertidas from num_clinicas_convertidas))*100,2) as porcentagem
from clinicas_convertidas_com_atividades cc
group by cc.feature
order by 2 

-- # Média da quantidade de atividades válidas de clínicas convertidas
select round(avg(num_atividades),2) as media from num_atividades_por_clinica_convertida

-- # Média da quantidade de atividades válidas de clínicas não convertidas
select round(avg(num_atividades),2) as media from num_atividades_por_clinica_nao_convertida

-- # Identificação do intervalo de período de Trial que têm maior correlação com a conversão.
select trial_duration_interval
, count(distinct td.clinic_id) as frequencia
, round((count(distinct td.clinic_id)::numeric / (select num_clinicas_convertidas from num_clinicas_convertidas))*100,2) as porcentagem
from trial_duration td
group by trial_duration_interval
order by 2

--  # Percentual de comparação de performance de conversão entre diferentes fontes de canal de marketing.
select cli.marketing_attribuition_channel_group
, count(cli.clinic_id) as frequencia
, round((count(cli.clinic_id)::numeric / (select num_clinicas_convertidas from num_clinicas_convertidas))*100,2) as porcentagem
from clinics cli
right join subscriptions as sub on sub.clinic_id = cli.clinic_id
where cli.is_chain_clinic is false
and exists (select * from activity act where act.clinic_id = cli.clinic_id )
and sub.stripe_subscription_id is not null	
group by cli.marketing_attribuition_channel_group
order by 2


