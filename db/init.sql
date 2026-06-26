--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: deployment_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deployment_events (
    id integer NOT NULL,
    deployment_id uuid NOT NULL,
    status text NOT NULL,
    "time" timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.deployment_events OWNER TO postgres;

--
-- Name: deployment_events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.deployment_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.deployment_events_id_seq OWNER TO postgres;

--
-- Name: deployment_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.deployment_events_id_seq OWNED BY public.deployment_events.id;


--
-- Name: deployments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deployments (
    id uuid NOT NULL,
    cloud text NOT NULL,
    environment text NOT NULL,
    application text NOT NULL,
    status text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.deployments OWNER TO postgres;

--
-- Name: deployment_events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployment_events ALTER COLUMN id SET DEFAULT nextval('public.deployment_events_id_seq'::regclass);


--
-- Data for Name: deployment_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deployment_events (id, deployment_id, status, "time") FROM stdin;
1	9925380d-7999-48c5-bcc1-e574c3166299	REQUESTED	2026-02-03 10:33:48.042911+05:30
2	9925380d-7999-48c5-bcc1-e574c3166299	VALIDATED	2026-02-03 10:33:48.042956+05:30
3	47688f7d-7cd0-435d-be65-8791ba940c19	REQUESTED	2026-02-03 10:34:30.521341+05:30
4	47688f7d-7cd0-435d-be65-8791ba940c19	VALIDATED	2026-02-03 10:34:30.521392+05:30
5	e460e80a-c0d1-4288-8183-30e33438e81a	REQUESTED	2026-02-03 10:51:15.5448+05:30
6	e460e80a-c0d1-4288-8183-30e33438e81a	VALIDATED	2026-02-03 10:51:15.544849+05:30
7	ab4659f9-4805-46da-bf01-f059a6fe44c3	REQUESTED	2026-02-03 11:01:52.021109+05:30
8	ab4659f9-4805-46da-bf01-f059a6fe44c3	VALIDATED	2026-02-03 11:01:52.021143+05:30
9	2045e899-e634-4993-a893-c40da9438f12	REQUESTED	2026-02-03 11:03:14.452314+05:30
10	2045e899-e634-4993-a893-c40da9438f12	VALIDATED	2026-02-03 11:03:14.452339+05:30
11	4c039499-9418-4a32-ac1e-7097fcf2b11e	REQUESTED	2026-02-03 11:06:07.847924+05:30
12	4c039499-9418-4a32-ac1e-7097fcf2b11e	VALIDATED	2026-02-03 11:06:07.847954+05:30
13	4c039499-9418-4a32-ac1e-7097fcf2b11e	IN_PROGRESS	2026-02-03 11:06:16.1228+05:30
14	4c039499-9418-4a32-ac1e-7097fcf2b11e	SUCCESS	2026-02-03 11:06:21.902097+05:30
15	2d65c97e-5d2b-4ee8-8075-bafe5d1ee88e	REQUESTED	2026-02-04 00:04:23.486017+05:30
16	2d65c97e-5d2b-4ee8-8075-bafe5d1ee88e	VALIDATED	2026-02-04 00:04:23.486049+05:30
17	2d65c97e-5d2b-4ee8-8075-bafe5d1ee88e	IN_PROGRESS	2026-02-04 00:04:31.935196+05:30
18	2d65c97e-5d2b-4ee8-8075-bafe5d1ee88e	SUCCESS	2026-02-04 00:04:37.687318+05:30
19	f7cc0068-ac9c-4517-8098-1f8ea76b9412	REQUESTED	2026-02-04 00:12:39.324118+05:30
20	f7cc0068-ac9c-4517-8098-1f8ea76b9412	VALIDATED	2026-02-04 00:12:39.324141+05:30
21	f7cc0068-ac9c-4517-8098-1f8ea76b9412	IN_PROGRESS	2026-02-04 00:12:45.913329+05:30
22	f7cc0068-ac9c-4517-8098-1f8ea76b9412	SUCCESS	2026-02-04 00:12:51.68402+05:30
23	617f72b5-c089-4cde-9884-6dbefa5c4b48	REQUESTED	2026-02-04 13:43:27.170688+05:30
24	617f72b5-c089-4cde-9884-6dbefa5c4b48	VALIDATED	2026-02-04 13:43:27.170725+05:30
25	617f72b5-c089-4cde-9884-6dbefa5c4b48	IN_PROGRESS	2026-02-04 13:43:34.951534+05:30
26	617f72b5-c089-4cde-9884-6dbefa5c4b48	SUCCESS	2026-02-04 13:43:40.761396+05:30
\.


--
-- Data for Name: deployments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deployments (id, cloud, environment, application, status, created_at) FROM stdin;
9925380d-7999-48c5-bcc1-e574c3166299	aws	dev	app	VALIDATED	2026-02-03 10:33:48.042911+05:30
47688f7d-7cd0-435d-be65-8791ba940c19	aws	dev	app	VALIDATED	2026-02-03 10:34:30.521341+05:30
e460e80a-c0d1-4288-8183-30e33438e81a	aws	dev	app1	VALIDATED	2026-02-03 10:51:15.5448+05:30
ab4659f9-4805-46da-bf01-f059a6fe44c3	aws	dev	app2	VALIDATED	2026-02-03 11:01:52.021109+05:30
2045e899-e634-4993-a893-c40da9438f12	azure	test	app3	VALIDATED	2026-02-03 11:03:14.452314+05:30
4c039499-9418-4a32-ac1e-7097fcf2b11e	aws	test	app4	SUCCESS	2026-02-03 11:06:07.847924+05:30
2d65c97e-5d2b-4ee8-8075-bafe5d1ee88e	azure	test	app5	SUCCESS	2026-02-04 00:04:23.486017+05:30
f7cc0068-ac9c-4517-8098-1f8ea76b9412	aws	dev	app6	SUCCESS	2026-02-04 00:12:39.324118+05:30
617f72b5-c089-4cde-9884-6dbefa5c4b48	azure	test	app7	SUCCESS	2026-02-04 13:43:27.170688+05:30
\.


--
-- Name: deployment_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.deployment_events_id_seq', 26, true);


--
-- Name: deployment_events deployment_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployment_events
    ADD CONSTRAINT deployment_events_pkey PRIMARY KEY (id);


--
-- Name: deployments deployments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployments
    ADD CONSTRAINT deployments_pkey PRIMARY KEY (id);


--
-- Name: idx_events_deployment_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_events_deployment_id ON public.deployment_events USING btree (deployment_id);


--
-- Name: deployment_events deployment_events_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployment_events
    ADD CONSTRAINT deployment_events_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployments(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

