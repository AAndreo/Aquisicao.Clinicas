-- Métricas de Credenciamento no Trial
with clinicas_unicas_periodo_trial as
(
	select cli.*
	from clinics cli
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
)
, clinicas_credenciadas_convertidas as
(
	select cli.*
	from clinics cli
	right join subscriptions as sub on sub.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
	and cli.is_accreditation_approved is true
	and sub.stripe_subscription_id is not null	
)
, clinicas_nao_credenciadas_convertidas as
(
	select cli.*
	from clinics cli
	right join subscriptions as sub on sub.clinic_id = cli.clinic_id
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
	and cli.is_accreditation_approved is not true
	and sub.stripe_subscription_id is not null	
)
, clinicas_credenciadas as
(
	select cli.*
	from clinics cli
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
	and cli.is_accreditation_approved is true
)
, clinicas_nao_credenciadas as
(
	select cli.*
	from clinics cli
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
	and cli.is_accreditation_approved is not true
)

-- # Percentual de clínicas que solicitaram credenciamento durante o trial.
select cut.has_asked_for_accreditation
, count(*) as frequencia
,round((count(*)::numeric / (select count(*) from clinicas_unicas_periodo_trial)*100),2) as porcentagem
from clinicas_unicas_periodo_trial cut
where cut.has_asked_for_accreditation is true
group by cut.has_asked_for_accreditation

-- # Conversão de clínicas credenciadas versus não credenciadas.  
-- Credenciadas
select num_total_clinicas_credenciadas
,num_clinicas_credenciadas_convertidas
,perc_clinicas_credenciadas_convertidas
from
(select count(*) num_total_clinicas_credenciadas from clinicas_credenciadas),
(select count(*) num_clinicas_credenciadas_convertidas from clinicas_credenciadas_convertidas),
(select round((count(*)::numeric / (select count(*) num_total_clinicas_credenciadas 
							  from clinicas_credenciadas)*100),2) as perc_clinicas_credenciadas_convertidas 
 from clinicas_credenciadas_convertidas)
 
 -- Não credenciadas
select num_total_clinicas_nao_credenciadas
,num_clinicas_nao_credenciadas_convertidas
,perc_clinicas_nao_credenciadas_convertidas
from
(select count(*) num_total_clinicas_nao_credenciadas from clinicas_nao_credenciadas),
(select count(*) num_clinicas_nao_credenciadas_convertidas from clinicas_nao_credenciadas_convertidas),
(select round((count(*)::numeric / (select count(*) num_total_clinicas_nao_credenciadas 
							  from clinicas_nao_credenciadas)*100),2) as perc_clinicas_nao_credenciadas_convertidas 
 from clinicas_nao_credenciadas_convertidas) 

