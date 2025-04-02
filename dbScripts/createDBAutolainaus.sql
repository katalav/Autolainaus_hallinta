-- Database: autolainaus

-- DROP DATABASE IF EXISTS autolainaus;

CREATE DATABASE autolainaus
    WITH
    OWNER = postgres
    ENCODING = 'WIN1252'
    LC_COLLATE = 'Finnish_Finland.1252'
    LC_CTYPE = 'Finnish_Finland.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE autolainaus
    IS 'Rasekon auto-osaston ajopäiväkirja sovellus';