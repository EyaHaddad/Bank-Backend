--
-- PostgreSQL database dump
--

\restrict 1Jate7SeqFlc37jigF67eMLqrYMKhlBOEF8SnrM2gDvogMVETeGNcnNY5ivPDgm

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.transfers DROP CONSTRAINT IF EXISTS transfers_id_fkey;
ALTER TABLE IF EXISTS ONLY public.transfers DROP CONSTRAINT IF EXISTS transfers_beneficiary_id_fkey;
ALTER TABLE IF EXISTS ONLY public.transactions DROP CONSTRAINT IF EXISTS transactions_sender_account_id_fkey;
ALTER TABLE IF EXISTS ONLY public.otps DROP CONSTRAINT IF EXISTS otps_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.beneficiaries DROP CONSTRAINT IF EXISTS beneficiaries_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS accounts_user_id_fkey;
DROP INDEX IF EXISTS public.ix_users_phone;
DROP INDEX IF EXISTS public.ix_users_lastname;
DROP INDEX IF EXISTS public.ix_users_id;
DROP INDEX IF EXISTS public.ix_users_firstname;
DROP INDEX IF EXISTS public.ix_users_email;
DROP INDEX IF EXISTS public.ix_transfers_beneficiary_id;
DROP INDEX IF EXISTS public.ix_transactions_sender_account_id;
DROP INDEX IF EXISTS public.ix_transactions_id;
DROP INDEX IF EXISTS public.ix_otps_user_id;
DROP INDEX IF EXISTS public.ix_otps_id;
DROP INDEX IF EXISTS public.ix_notifications_user_id;
DROP INDEX IF EXISTS public.ix_notifications_id;
DROP INDEX IF EXISTS public.ix_beneficiaries_user_id;
DROP INDEX IF EXISTS public.ix_beneficiaries_id;
DROP INDEX IF EXISTS public.ix_accounts_user_id;
DROP INDEX IF EXISTS public.ix_accounts_id;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.transfers DROP CONSTRAINT IF EXISTS transfers_pkey;
ALTER TABLE IF EXISTS ONLY public.transactions DROP CONSTRAINT IF EXISTS transactions_pkey;
ALTER TABLE IF EXISTS ONLY public.otps DROP CONSTRAINT IF EXISTS otps_pkey;
ALTER TABLE IF EXISTS ONLY public.notifications DROP CONSTRAINT IF EXISTS notifications_pkey;
ALTER TABLE IF EXISTS ONLY public.beneficiaries DROP CONSTRAINT IF EXISTS beneficiaries_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS accounts_pkey;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.transfers;
DROP TABLE IF EXISTS public.transactions;
DROP TABLE IF EXISTS public.otps;
DROP TABLE IF EXISTS public.notifications;
DROP TABLE IF EXISTS public.beneficiaries;
DROP TABLE IF EXISTS public.accounts;
DROP TYPE IF EXISTS public.transferstatus;
DROP TYPE IF EXISTS public.transactiontype;
DROP TYPE IF EXISTS public.transactionstatus;
DROP TYPE IF EXISTS public.role;
DROP TYPE IF EXISTS public.otppurpose;
DROP TYPE IF EXISTS public.notificationtype;
DROP TYPE IF EXISTS public.accounttype;
DROP TYPE IF EXISTS public.accountstatus;
--
-- Name: accountstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.accountstatus AS ENUM (
    'ACTIVE',
    'BLOCKED',
    'CLOSED'
);


--
-- Name: accounttype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.accounttype AS ENUM (
    'COURANT',
    'EPARGNE'
);


--
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.notificationtype AS ENUM (
    'EMAIL',
    'SMS'
);


--
-- Name: otppurpose; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.otppurpose AS ENUM (
    'LOGIN',
    'TRANSACTION',
    'PASSWORD_RESET',
    'EMAIL_VERIFICATION',
    'PHONE_VERIFICATION',
    'ACCOUNT_ACTIVATION'
);


--
-- Name: role; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.role AS ENUM (
    'ADMIN',
    'USER'
);


--
-- Name: transactionstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.transactionstatus AS ENUM (
    'PENDING',
    'COMPLETED',
    'FAILED'
);


--
-- Name: transactiontype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.transactiontype AS ENUM (
    'DEBIT',
    'CREDIT',
    'TRANSFER'
);


--
-- Name: transferstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.transferstatus AS ENUM (
    'PENDING',
    'VALIDATED',
    'REJECTED'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    balance double precision,
    currency character varying,
    account_type public.accounttype NOT NULL,
    status public.accountstatus NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: beneficiaries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.beneficiaries (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    name character varying NOT NULL,
    bank_name character varying NOT NULL,
    iban character varying NOT NULL,
    email character varying,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    type public.notificationtype NOT NULL,
    title character varying NOT NULL,
    content text NOT NULL,
    sent_at timestamp without time zone NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: otps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.otps (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    code character varying(10) NOT NULL,
    purpose public.otppurpose NOT NULL,
    is_used boolean NOT NULL,
    attempts integer NOT NULL,
    max_attempts integer NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transactions (
    id uuid NOT NULL,
    sender_account_id uuid NOT NULL,
    reference character varying,
    type public.transactiontype NOT NULL,
    amount double precision NOT NULL,
    status public.transactionstatus NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: transfers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transfers (
    id uuid NOT NULL,
    beneficiary_id uuid NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    firstname character varying NOT NULL,
    lastname character varying NOT NULL,
    email character varying NOT NULL,
    phone character varying,
    role public.role NOT NULL,
    is_active boolean NOT NULL,
    is_email_verified boolean NOT NULL,
    password_hash character varying NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts (id, user_id, balance, currency, account_type, status, created_at, updated_at) FROM stdin;
270e899d-5d1a-438e-b969-c0ac848d5902	25527ffc-a71f-4842-adad-6acc82b2cc7a	400	TND	EPARGNE	ACTIVE	2026-01-04 12:55:50.152509	2026-01-04 13:03:36.947759
c01ecb07-879f-4dc7-8d41-dfe259d597e5	25527ffc-a71f-4842-adad-6acc82b2cc7a	4950	TND	COURANT	ACTIVE	2026-01-04 12:46:39.382666	2026-01-04 13:03:36.947759
\.


--
-- Data for Name: beneficiaries; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.beneficiaries (id, user_id, name, bank_name, iban, email, is_verified, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (id, type, title, content, sent_at, user_id, created_at, updated_at) FROM stdin;
8c27951b-0b37-46fb-ab9a-0c76f08e850c	EMAIL	Welcome to Secure Banking!	Dear admin test,\n\nWelcome to Secure Banking! Your account has been successfully created.\n\nAccount Details:\n- Email: eyahaddad450@gmail.com\n- Registration Date: 2026-01-04 11:39:26 UTC\n\nFor your security, please verify your email address using the verification code sent separately.\n\nImportant Security Tips:\n- Never share your password or OTP codes with anyone\n- Always log out when using shared devices\n- Contact our support team if you notice any suspicious activity\n\nThank you for choosing Secure Banking!\n\nBest regards,\nYour Banking Team	2026-01-04 12:39:27.922221	a4a59777-d8ba-49d4-9a7b-72a465b49a49	2026-01-04 12:39:27.924231	2026-01-04 12:39:27.924231
e78e3fcc-ae9a-4676-ab28-fc7b9a17fb92	EMAIL	Welcome to Secure Banking!	Dear Imen Haddad,\n\nWelcome to Secure Banking! Your account has been successfully created.\n\nAccount Details:\n- Email: haddad.eyamail@gmail.com\n- Registration Date: 2026-01-04 11:40:38 UTC\n\nFor your security, please verify your email address using the verification code sent separately.\n\nImportant Security Tips:\n- Never share your password or OTP codes with anyone\n- Always log out when using shared devices\n- Contact our support team if you notice any suspicious activity\n\nThank you for choosing Secure Banking!\n\nBest regards,\nYour Banking Team	2026-01-04 12:40:40.461304	25527ffc-a71f-4842-adad-6acc82b2cc7a	2026-01-04 12:40:40.461304	2026-01-04 12:40:40.461304
\.


--
-- Data for Name: otps; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.otps (id, user_id, code, purpose, is_used, attempts, max_attempts, expires_at, used_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transactions (id, sender_account_id, reference, type, amount, status, created_at, updated_at) FROM stdin;
679395cb-8210-49fd-b0fb-b054e3c43937	270e899d-5d1a-438e-b969-c0ac848d5902	INT_20260104120336_1	TRANSFER	400	COMPLETED	2026-01-04 13:03:36.953401	2026-01-04 13:03:36.953401
\.


--
-- Data for Name: transfers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transfers (id, beneficiary_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, firstname, lastname, email, phone, role, is_active, is_email_verified, password_hash, created_at, updated_at) FROM stdin;
a4a59777-d8ba-49d4-9a7b-72a465b49a49	admin	test	eyahaddad450@gmail.com	\N	ADMIN	t	t	$2b$12$D.U.OzrizWyHA5gQa.YtZOUNe.4Y1a4iQgp/7FuOW.Y3ydm7T.BTy	2026-01-04 12:39:26.26875	2026-01-04 12:39:26.26875
25527ffc-a71f-4842-adad-6acc82b2cc7a	Imen	Haddad	haddad.eyamail@gmail.com	+21693722385	USER	t	t	$2b$12$fBJG6I1jPAWrjIXvjg1qpuJRO5AZDGaZAaAGSSEJ0XX6Vc7Mm.DG2	2026-01-04 12:40:38.70953	2026-01-04 12:40:38.70953
\.


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: beneficiaries beneficiaries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.beneficiaries
    ADD CONSTRAINT beneficiaries_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: otps otps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otps
    ADD CONSTRAINT otps_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: transfers transfers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transfers
    ADD CONSTRAINT transfers_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_accounts_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_accounts_id ON public.accounts USING btree (id);


--
-- Name: ix_accounts_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_accounts_user_id ON public.accounts USING btree (user_id);


--
-- Name: ix_beneficiaries_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_beneficiaries_id ON public.beneficiaries USING btree (id);


--
-- Name: ix_beneficiaries_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_beneficiaries_user_id ON public.beneficiaries USING btree (user_id);


--
-- Name: ix_notifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);


--
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: ix_otps_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_otps_id ON public.otps USING btree (id);


--
-- Name: ix_otps_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_otps_user_id ON public.otps USING btree (user_id);


--
-- Name: ix_transactions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transactions_id ON public.transactions USING btree (id);


--
-- Name: ix_transactions_sender_account_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transactions_sender_account_id ON public.transactions USING btree (sender_account_id);


--
-- Name: ix_transfers_beneficiary_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transfers_beneficiary_id ON public.transfers USING btree (beneficiary_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_firstname; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_firstname ON public.users USING btree (firstname);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_lastname; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_lastname ON public.users USING btree (lastname);


--
-- Name: ix_users_phone; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_phone ON public.users USING btree (phone);


--
-- Name: accounts accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: beneficiaries beneficiaries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.beneficiaries
    ADD CONSTRAINT beneficiaries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: otps otps_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otps
    ADD CONSTRAINT otps_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: transactions transactions_sender_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_sender_account_id_fkey FOREIGN KEY (sender_account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: transfers transfers_beneficiary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transfers
    ADD CONSTRAINT transfers_beneficiary_id_fkey FOREIGN KEY (beneficiary_id) REFERENCES public.beneficiaries(id) ON DELETE CASCADE;


--
-- Name: transfers transfers_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transfers
    ADD CONSTRAINT transfers_id_fkey FOREIGN KEY (id) REFERENCES public.transactions(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 1Jate7SeqFlc37jigF67eMLqrYMKhlBOEF8SnrM2gDvogMVETeGNcnNY5ivPDgm

