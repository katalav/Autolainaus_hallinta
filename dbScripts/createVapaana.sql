-- View: public.vapaana

-- DROP VIEW public.vapaana;

CREATE OR REPLACE VIEW public.vapaana
 AS
 SELECT rekisterinumero,
    merkki,
    malli,
    automaatti,
    henkilomaara
   FROM auto
  WHERE NOT (rekisterinumero::text IN ( SELECT ajossa.rekisterinumero
           FROM ajossa))
  ORDER BY rekisterinumero;

ALTER TABLE public.vapaana
    OWNER TO postgres;

GRANT SELECT ON TABLE public.vapaana TO autolainaus;
GRANT ALL ON TABLE public.vapaana TO postgres;
