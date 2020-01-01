CREATE DATABASE dot11monitor;
\c dot11monitor

REVOKE ALL ON SCHEMA PUBLIC FROM PUBLIC;

CREATE USER dot11viewer WITH PASSWORD 'dot11password';
CREATE USER dot11admin WITH PASSWORD 'dot11password';

CREATE SCHEMA private;
CREATE SCHEMA statistic;

GRANT ALL PRIVILEGES ON SCHEMA private TO dot11admin;
GRANT ALL PRIVILEGES ON SCHEMA statistic TO dot11admin;

GRANT SELECT ON ALL TABLES IN SCHEMA statistic TO dot11viewer;
ALTER DEFAULT PRIVILEGES FOR USER dot11viewer REVOKE EXECUTE ON FUNCTIONS FROM public;
/*
REVOKE SELECT ON ALL TABLES IN SCHEMA pg_catalog FROM PUBLIC
REVOKE ALL ON DATABASE dot11monitor FROM PUBLIC;

ALTER DEFAULT PRIVILEGES FOR USER dot11viewer
REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO dot11viewer;

ALTER DEFAULT PRIVILEGES FOR USER dot11viewer IN SCHEMA public
GRANT SELECT ON TABLES TO dot11viewer;
*/