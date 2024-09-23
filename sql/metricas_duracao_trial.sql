-- Metricas duração do Trial
with clinicas_unicas_periodo_trial as
(
	select cli.*
	from clinics cli
	where cli.is_chain_clinic is false
	and exists (select * from activity act where act.clinic_id = cli.clinic_id)
)

-- # Qtde de clinicas unicas durante o periodo Trial
select count(distinct c.clinic_id) as frequencia from clinicas_unicas_periodo_trial c;

-- Duração média do período de trial para todas as clínicas.
select round(avg(c.trial_duration),2) as media from clinicas_unicas_periodo_trial c;
