-- Métricas de Interação Durante o Trial
-- Atividades
with atividades as
(
select act.clinic_id, act.activity_type, act.feature
from clinics cli
inner join activity act on act.clinic_id = cli.clinic_id
where cli.is_chain_clinic is false
and act.is_valid_activity is True
)
,num_atividades_validas as
(
select count(*) as num_atividades_validas 
from clinics cli
inner join activity act on act.clinic_id = cli.clinic_id
where cli.is_chain_clinic is false
and act.is_valid_activity is True
)
,num_clinicas_atividades_validas as
(
select count(distinct cli.clinic_id) num_clinicas_atividades_validas
from clinics cli
inner join activity act on act.clinic_id = cli.clinic_id
where cli.is_chain_clinic is false
and act.is_valid_activity is True
)
,num_atividades_por_clinica as
(
select a.clinic_id, count(*) as freq_atividades
from atividades a
group by a.clinic_id
)

-- # Número médio de atividades realizadas por clínica durante o trial.
select round(avg(a.freq_atividades),2) as media from num_atividades_por_clinica a

-- # Distribuição do número de atividades por clínica (quantas clínicas realizaram mais de X atividades).
select * from num_atividades_por_clinica order by 2 desc limit 10

-- # Quais funcionalidades são mais usadas durante o trial.
select ati.feature
, count(ati.feature) as frequencia
, round((count(ati.feature)::numeric / (select num_atividades_validas from num_atividades_validas))*100,2) as porcentagem
from atividades as ati
group by ati.feature
order by 2 desc

-- # Percentual de clínicas que utilizam funcionalidades específicas (como prontuário eletrônico, agenda, gestão financeira).
select ati.feature, count(ati.feature) as frequencia
, round((count(ati.feature)::numeric / (select num_clinicas_atividades_validas from num_clinicas_atividades_validas))*100,2) as porcentagem
from 
(select distinct ati.feature
, ati.clinic_id
from atividades as ati) as ati
group by ati.feature
order by 2 desc
