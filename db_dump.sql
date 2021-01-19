--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-01-19 20:11:38

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

--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3047 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 206 (class 1259 OID 16636)
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    commentid integer NOT NULL,
    userid integer,
    postid integer,
    commentdate date NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16626)
-- Name: equipmenttool; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipmenttool (
    eqtoolid integer NOT NULL,
    eqtoolname character varying(25) NOT NULL,
    issale boolean NOT NULL,
    isshared boolean NOT NULL
);


ALTER TABLE public.equipmenttool OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16575)
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location (
    locationid integer NOT NULL,
    country character varying(20) NOT NULL,
    city character varying(25) NOT NULL,
    district character varying(25) NOT NULL
);


ALTER TABLE public.location OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16601)
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    postid integer NOT NULL,
    userid integer,
    postdate date NOT NULL,
    title character varying(25) NOT NULL,
    description text NOT NULL,
    sportsid integer,
    eqtoolid integer
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16654)
-- Name: sportplace; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sportplace (
    sportplaceid integer NOT NULL,
    locationid integer,
    sportsid integer,
    placename character varying(50) NOT NULL,
    rate integer,
    CONSTRAINT sportplace_rate_check CHECK (((rate >= 0) AND (rate <= 5)))
);


ALTER TABLE public.sportplace OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16614)
-- Name: sports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sports (
    sportsid integer NOT NULL,
    sportname character varying(30) NOT NULL,
    isteam boolean NOT NULL
);


ALTER TABLE public.sports OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16584)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    locationid integer,
    username character varying(20) NOT NULL,
    surname character varying(20) NOT NULL,
    age integer NOT NULL,
    email character varying(30) NOT NULL,
    usrpassword character varying(256) NOT NULL,
    rate integer,
    proficiency text,
    CONSTRAINT users_age_check CHECK (((age >= 10) AND (age <= 80))),
    CONSTRAINT users_rate_check CHECK (((rate >= 0) AND (rate <= 5)))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 3040 (class 0 OID 16636)
-- Dependencies: 206
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (commentid, userid, postid, commentdate, description) FROM stdin;
1	1	6	2021-01-19	Sure 
\.


--
-- TOC entry 3039 (class 0 OID 16626)
-- Dependencies: 205
-- Data for Name: equipmenttool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipmenttool (eqtoolid, eqtoolname, issale, isshared) FROM stdin;
2	Table Tennis Ball	f	t
4	Basketball	t	f
1	Tennis Racket	f	t
5	Football	t	f
6	Gloves	t	f
7	Sneakers	t	f
8	Jersey	f	t
9	Pilates Ball	f	t
10	Dumbbell	f	t
3	Helmet	f	t
\.


--
-- TOC entry 3035 (class 0 OID 16575)
-- Dependencies: 201
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location (locationid, country, city, district) FROM stdin;
1	Turkey	Istanbul	Besiktas
2	Germany	Munich	Josephsplatz
4	Turkey	Ankara	Çankaya
8	Turkey	Istanbul	Göktürk
9	Turkey	Istanbul	Karşıyaka
5	United Kingdom	London	Chelsea
11	Turkey	Istanbul	Yesilkoy
12	Turkey	Istanbul	Sinanoba
13	Turkey	Istanbul	Kurtköy
14	Turkey	Istanbul	Büyükçekmece
15	Turkey	Istanbul	Bostancı
16	Turkey	Samsun	Atakum
17	Turkey	Istanbul	Kadıköy
18	Turkey	İzmir	Narlıdere
19	Turkey	Istanbul	Merter
\.


--
-- TOC entry 3037 (class 0 OID 16601)
-- Dependencies: 203
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (postid, userid, postdate, title, description, sportsid, eqtoolid) FROM stdin;
1	2	2021-01-19	Racket	It is very new and never used	\N	1
2	2	2021-01-19	Racket	Super	\N	1
3	3	2021-01-19	Football for Every Week	I would like to play football every sunday, if you are looking for someone please drop a comment	3	\N
4	3	2021-01-19	Ball	I'm selling my ball for 30 lira	\N	5
5	4	2021-01-19	Pilates around Merter	I'm available by 8 pm, drop a comment if you want to join me	4	\N
6	4	2021-01-19	Basketball 	Let's play 1 to 1	1	\N
7	1	2021-01-19	Let's play basketball	Where are four now, looking for an extra person who likes playing basketball	1	\N
8	1	2021-01-19	Let's jog	I don't want to jog alone join me	9	\N
9	1	2021-01-19	Tennis	I'm newbie in tennis, looking for someone experienced	2	\N
10	1	2021-01-19	Giving away my Helmet	It is old but still usable	\N	3
\.


--
-- TOC entry 3041 (class 0 OID 16654)
-- Dependencies: 207
-- Data for Name: sportplace; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sportplace (sportplaceid, locationid, sportsid, placename, rate) FROM stdin;
2	4	2	Cumhuriyet Sahası	3
3	4	4	Atatürk Parkı	4
4	5	3	St. James Field	5
5	2	1	DeutscherPark	5
8	11	1	Röne Park	0
7	1	1	Atatürk Parkı	5
9	13	7	Istanbul Park	5
1	1	1	Yıldız Parkı Basket Sahası	3
10	17	1	Yoğurtçu Parkı	0
11	15	11	Bostancı Spor Salonu	4
\.


--
-- TOC entry 3038 (class 0 OID 16614)
-- Dependencies: 204
-- Data for Name: sports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sports (sportsid, sportname, isteam) FROM stdin;
1	Basketball	t
2	Tennis	f
3	Football	t
4	Pilates	f
6	Table Tennis	f
8	Badminton	f
9	Jogging	f
10	Swimming	f
11	Volleyball	t
12	Beach Volleyball	t
7	Motor Sports	t
\.


--
-- TOC entry 3036 (class 0 OID 16584)
-- Dependencies: 202
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (userid, locationid, username, surname, age, email, usrpassword, rate, proficiency) FROM stdin;
1	14	Emre	Güler	23	gulere15@itu.edu.tr	$pbkdf2-sha256$29000$jbG2llKKEeKcE0IIodQ6xw$pL113dXSUQ013UKNZCjEnpRZ5EhN1v4L8H5jVGV8D64	5	Intermediate
3	18	Ali	Akdeniz	55	aliakdeniz@gmail.com	$pbkdf2-sha256$29000$mPOe896b835vLYVQihHiHA$JgBH6SSDXqhsHBBx3mbXlsCIpXgbtqtqSXFpjoi0rCs	0	Beginner
2	16	Pelin	Kapıcıoğlu	22	pkapicioglu@sabanciuniv.edu	$pbkdf2-sha256$29000$UeodQ8g5RyiFMKa09r4X4g$inktdFTjeRhVqnYTTHmUp0OrdnYyBJSqF4MVvxgSsEc	4	Intermediate
4	19	Ayşe	Öztürk	20	ayseozturk@hotmail.com	$pbkdf2-sha256$29000$3ftfa01pba11rpWSkhLCuA$iybivpHBV9AlIoYp7YG912Qm0K.v.FJupQW17lqijuY	0	Beginner
\.


--
-- TOC entry 2894 (class 2606 OID 16643)
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (commentid);


--
-- TOC entry 2892 (class 2606 OID 16630)
-- Name: equipmenttool equipmenttool_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipmenttool
    ADD CONSTRAINT equipmenttool_pkey PRIMARY KEY (eqtoolid);


--
-- TOC entry 2880 (class 2606 OID 16579)
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (locationid);


--
-- TOC entry 2886 (class 2606 OID 16608)
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (postid);


--
-- TOC entry 2896 (class 2606 OID 16659)
-- Name: sportplace sportplace_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sportplace
    ADD CONSTRAINT sportplace_pkey PRIMARY KEY (sportplaceid);


--
-- TOC entry 2888 (class 2606 OID 16618)
-- Name: sports sports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sports
    ADD CONSTRAINT sports_pkey PRIMARY KEY (sportsid);


--
-- TOC entry 2890 (class 2606 OID 16620)
-- Name: sports sports_sportname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sports
    ADD CONSTRAINT sports_sportname_key UNIQUE (sportname);


--
-- TOC entry 2882 (class 2606 OID 16595)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 2884 (class 2606 OID 16593)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- TOC entry 2902 (class 2606 OID 16649)
-- Name: comment comment_postid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_postid_fkey FOREIGN KEY (postid) REFERENCES public.posts(postid);


--
-- TOC entry 2901 (class 2606 OID 16681)
-- Name: comment comment_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- TOC entry 2900 (class 2606 OID 16691)
-- Name: posts posts_eqtoolid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_eqtoolid_fkey FOREIGN KEY (eqtoolid) REFERENCES public.equipmenttool(eqtoolid);


--
-- TOC entry 2898 (class 2606 OID 16676)
-- Name: posts posts_sportsid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_sportsid_fkey FOREIGN KEY (sportsid) REFERENCES public.sports(sportsid);


--
-- TOC entry 2899 (class 2606 OID 16686)
-- Name: posts posts_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- TOC entry 2903 (class 2606 OID 16660)
-- Name: sportplace sportplace_locationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sportplace
    ADD CONSTRAINT sportplace_locationid_fkey FOREIGN KEY (locationid) REFERENCES public.location(locationid);


--
-- TOC entry 2904 (class 2606 OID 16665)
-- Name: sportplace sportplace_sportsid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sportplace
    ADD CONSTRAINT sportplace_sportsid_fkey FOREIGN KEY (sportsid) REFERENCES public.sports(sportsid);


--
-- TOC entry 2897 (class 2606 OID 16596)
-- Name: users users_locationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_locationid_fkey FOREIGN KEY (locationid) REFERENCES public.location(locationid);


--
-- TOC entry 3048 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE comment; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.comment TO PUBLIC;


--
-- TOC entry 3049 (class 0 OID 0)
-- Dependencies: 205
-- Name: TABLE equipmenttool; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.equipmenttool TO PUBLIC;


--
-- TOC entry 3050 (class 0 OID 0)
-- Dependencies: 201
-- Name: TABLE location; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.location TO PUBLIC;


--
-- TOC entry 3051 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE posts; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.posts TO PUBLIC;


--
-- TOC entry 3052 (class 0 OID 0)
-- Dependencies: 207
-- Name: TABLE sportplace; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.sportplace TO PUBLIC;


--
-- TOC entry 3053 (class 0 OID 0)
-- Dependencies: 204
-- Name: TABLE sports; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.sports TO PUBLIC;


--
-- TOC entry 3054 (class 0 OID 0)
-- Dependencies: 202
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.users TO PUBLIC;


-- Completed on 2021-01-19 20:11:40

--
-- PostgreSQL database dump complete
--

