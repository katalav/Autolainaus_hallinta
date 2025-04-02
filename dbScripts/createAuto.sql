-- Table: public.auto

-- DROP TABLE IF EXISTS public.auto;

CREATE TABLE IF NOT EXISTS public.auto
(
    rekisterinumero character varying(7) COLLATE pg_catalog."default" NOT NULL,
    merkki character varying(30) COLLATE pg_catalog."default" NOT NULL,
    malli character varying(20) COLLATE pg_catalog."default" NOT NULL,
    vuosimalli character(4) COLLATE pg_catalog."default" NOT NULL,
    henkilomaara integer,
    tyyppi character varying COLLATE pg_catalog."default",
    automaatti boolean NOT NULL,
    vastuuhenkilo character varying(30) COLLATE pg_catalog."default",
    kuva bytea,
    CONSTRAINT auto_pkey PRIMARY KEY (rekisterinumero),
    CONSTRAINT ajoneuvotyyppi_fk FOREIGN KEY (tyyppi)
        REFERENCES public.ajoneuvotyyppi (tyyppi) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.auto
    OWNER to postgres;

REVOKE ALL ON TABLE public.auto FROM autolainaus;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE public.auto TO autolainaus;

GRANT ALL ON TABLE public.auto TO postgres;

COMMENT ON TABLE public.auto
    IS 'Ajoneuvon perustiedot';