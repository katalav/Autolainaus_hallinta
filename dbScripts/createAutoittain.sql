-- View: public.autoittain

-- DROP VIEW public.autoittain;

CREATE OR REPLACE VIEW public.autoittain
 AS
 SELECT auto.rekisterinumero,
    auto.merkki,
    auto.malli,
    lainaaja.hetu,
    lainaaja.sukunimi,
    lainaaja.etunimi,
    lainaus.lainausaika AS otto,
    lainaus.palautus
   FROM auto
     JOIN lainaus ON auto.rekisterinumero::text = lainaus.rekisterinumero::text
     JOIN lainaaja ON lainaus.hetu = lainaaja.hetu
  ORDER BY auto.rekisterinumero, lainaus.lainausaika DESC;

ALTER TABLE public.autoittain
    OWNER TO postgres;
COMMENT ON VIEW public.autoittain
    IS 'Ajopäiväkirja autokohtaisesti käänteisessä aikajärjestyksessä eli uusimmat lainaukset ensin.';

GRANT SELECT ON TABLE public.autoittain TO autolainaus;
GRANT ALL ON TABLE public.autoittain TO postgres;

