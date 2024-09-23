-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.clinica_dim
(
    id_clinica integer NOT NULL,
    data_cadastro timestamp without time zone,
    PRIMARY KEY (id_clinica)
);

COMMENT ON TABLE public.clinica_dim
    IS 'Tabela dimensão para dados das clínicas';

CREATE TABLE IF NOT EXISTS public.funcionalidade_dim
(
    id_funcionalidade integer NOT NULL,
    nom_funcionalidade character varying(50),
    PRIMARY KEY (id_funcionalidade)
);

COMMENT ON TABLE public.funcionalidade_dim
    IS 'Tabela dimensão para dados das Funcionalidades';

CREATE TABLE IF NOT EXISTS public.trial_fato
(
    id_trial integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    id_clinica integer NOT NULL,
    id_canal integer,
    data_inicio_trial date,
    data_fim_trial date,
    num_dias_trial integer,
    total_atividades_realizadas integer,
    solicitou_credenciamento boolean,
    credenciamento_aprovado boolean,
    credenciamento_status character varying(50),
    realizou_assinatura boolean,
    data_assinatura date,
    status_assinatura character varying(50),
    num_dias_para_assinatura integer,
    CONSTRAINT pk_trial PRIMARY KEY (id_trial)
);

COMMENT ON TABLE public.trial_fato
    IS 'Tabela Fato para as ocorrências das clínicas durante o período Trial.';

CREATE TABLE IF NOT EXISTS public.canal_marketing_dim
(
    id_canal integer NOT NULL,
    nom_canal character varying(50) NOT NULL,
    PRIMARY KEY (id_canal)
);

COMMENT ON TABLE public.canal_marketing_dim
    IS 'Tabela dimensão contendo as informações dos canais de marketing de aquisição de clínicas.';

CREATE TABLE IF NOT EXISTS public.funcionalidade_utilizada_fato
(
    id_funcionalidade_utilizada integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    id_clinica integer NOT NULL,
    id_funcionalidade integer NOT NULL,
    num_qtde_vezes integer,
    CONSTRAINT pk_funcionalidade_utilizada PRIMARY KEY (id_funcionalidade_utilizada)
);

COMMENT ON TABLE public.funcionalidade_utilizada_fato
    IS 'Tabela fato das funcionalidades utilizadas e sua respectiva quantidade de vezes';

ALTER TABLE IF EXISTS public.trial_fato
    ADD CONSTRAINT fk_trial_clinica FOREIGN KEY (id_clinica)
    REFERENCES public.clinica_dim (id_clinica) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

COMMENT ON CONSTRAINT fk_trial_clinica ON public.trial_fato
    IS 'FK entre as tabelas trial_fato e dim_clinica';



ALTER TABLE IF EXISTS public.trial_fato
    ADD CONSTRAINT fk_trial_canal FOREIGN KEY (id_canal)
    REFERENCES public.canal_marketing_dim (id_canal) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

COMMENT ON CONSTRAINT fk_trial_canal ON public.trial_fato
    IS 'FK entre as tabelas trial_fato e canal_marketing_dim';



ALTER TABLE IF EXISTS public.funcionalidade_utilizada_fato
    ADD CONSTRAINT fk_funcionalidade_utilizada_funcionalidade FOREIGN KEY (id_funcionalidade)
    REFERENCES public.funcionalidade_dim (id_funcionalidade) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

COMMENT ON CONSTRAINT fk_funcionalidade_utilizada_funcionalidade ON public.funcionalidade_utilizada_fato
    IS 'FK entre as tabelas funcionalidade_utilizada_fato e funcionalidade_dim';



ALTER TABLE IF EXISTS public.funcionalidade_utilizada_fato
    ADD CONSTRAINT fk_funcionalidade_utilizada_clinica FOREIGN KEY (id_clinica)
    REFERENCES public.clinica_dim (id_clinica) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

COMMENT ON CONSTRAINT fk_funcionalidade_utilizada_clinica ON public.funcionalidade_utilizada_fato
    IS 'Fk entre as tabelas funcionalidade_utilizada e clinica';


END;