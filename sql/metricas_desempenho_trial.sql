-- Métricas de Desempenho do Trial
with clinicas_unicas_periodo_trial as
(
	select cli.*
	from clinics cli
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
)

-- # Percentual de clínicas que param de usar o produto durante o trial (não realizaram a assinatura do produto - não foram convertidas).  
select count(*) as frequencia
, round((count(*)::numeric / (select count(*) from clinicas_unicas_periodo_trial))*100,2) as porcentagem
from clinicas_unicas_periodo_trial cut
where not exists (select sub.clinic_id from subscriptions as sub where sub.clinic_id = cut.clinic_id)

-- # Percentual de clínicas que param de usar o produto após o trial (realizaram a assinatura do produto, porem não esta mais ativa).  
select count(*) as frequencia
, round((count(*)::numeric / (select count(*) from clinicas_unicas_periodo_trial))*100,2) as porcentagem
from clinicas_unicas_periodo_trial cut
inner join subscriptions sub on sub.clinic_id = cut.clinic_id
where sub.subscription_status != 'active'
