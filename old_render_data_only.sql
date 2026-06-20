--
-- PostgreSQL database dump
--

\restrict x8YEplrzA9FuYEaZSvJk0HMJdUnCgoK7nqKePV92BJKOmEuWY34l7JXstIpbJ8o

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_content_type (id, app_label, model) VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (2, 'auth', 'group');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (3, 'auth', 'permission');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (4, 'auth', 'user');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (6, 'sessions', 'session');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (7, 'customers_app', 'application');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (8, 'customers_app', 'applicationstatushistory');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (9, 'customers_app', 'customer');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (10, 'customers_app', 'grievance');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (11, 'customers_app', 'grievancehistory');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add permission', 3, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change permission', 3, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete permission', 3, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view permission', 3, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add group', 2, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change group', 2, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete group', 2, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view group', 2, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add customer', 9, 'add_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change customer', 9, 'change_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete customer', 9, 'delete_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view customer', 9, 'view_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add application', 7, 'add_application');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change application', 7, 'change_application');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete application', 7, 'delete_application');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view application', 7, 'view_application');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add application status history', 8, 'add_applicationstatushistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change application status history', 8, 'change_applicationstatushistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete application status history', 8, 'delete_applicationstatushistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view application status history', 8, 'view_applicationstatushistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add grievance', 10, 'add_grievance');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change grievance', 10, 'change_grievance');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete grievance', 10, 'delete_grievance');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view grievance', 10, 'view_grievance');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add grievance history', 11, 'add_grievancehistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change grievance history', 11, 'change_grievancehistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete grievance history', 11, 'delete_grievancehistory');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view grievance history', 11, 'view_grievancehistory');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (11, 'pbkdf2_sha256$1200000$LhG9Co73rFlIVa5cCjAmBQ$FzRPvDWW6dvLMPRfn72qtRyp0tSPCbTj9o0dcpT2Uoc=', '2026-05-22 11:19:05.359806+05:30', false, 'sanjay8578', '', '', '', false, true, '2026-05-22 11:17:12.61397+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (7, 'pbkdf2_sha256$1200000$zbFkbHbGiXoBRVbPmbiZ1W$VHksH8aFwrqEdFZpgc/gUq0B3heQEvrWPu5bNSYNph0=', '2026-05-22 12:05:19.676206+05:30', false, 'rubi4661', '', '', '', false, true, '2026-05-20 10:34:47.408979+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (12, 'pbkdf2_sha256$1200000$6828oJ08sDZFRG6pEFLh1P$1Cb77zHfhLcdJhvUUAcJE8QEyEXWO6cb+2JD9x+d+Gc=', '2026-05-22 17:34:06.908919+05:30', false, 'ashok2145', '', '', '', false, true, '2026-05-22 17:33:31.250057+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (2, 'pbkdf2_sha256$1200000$RhNfDqnO5FqNaZweN9WXRj$5fxNbRDBdkN+vwG8q/Yq8i+7Aq3XlmhqzUTIeUWgDIs=', '2026-05-18 22:16:11.69092+05:30', false, 'sanjay2512', '', '', '', false, true, '2026-05-18 19:08:48.049729+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (14, 'pbkdf2_sha256$1200000$yLJVx5UgcWINV174R7kRpj$hdqfLI/7f5DyCVujwLWTa6p9dDGn2QqJWdkXjWZCbAA=', '2026-06-13 13:57:06.135209+05:30', false, 'abhi7097', '', '', '', false, true, '2026-06-01 20:34:39.948409+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (16, 'pbkdf2_sha256$1200000$7n0KVRJeZTyzptWjqYftDx$X3Ecuo6oXwCuxmZX7kpTugn1PjSYdFMr67Jw+T7opW4=', '2026-06-13 14:01:06.954087+05:30', false, 'vish9781', '', '', '', false, true, '2026-06-05 07:01:34.296177+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (6, 'pbkdf2_sha256$1200000$oRTOUlcsG9GtX76rJEQsN1$sQCIkuPsgGcZOUcLHfHtibQhSP/8XNioKkR0j6K1uk8=', '2026-05-20 10:04:14.22754+05:30', false, 'balvir5640', '', '', '', false, true, '2026-05-20 09:57:30.328151+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (13, 'pbkdf2_sha256$1200000$9lMSJ4BAPLcz0k74bEoq2W$BvR4sP9xruyP2TVoYWox1vE8v0rzBFn224jOjn4Iw1w=', '2026-05-24 20:13:58.951676+05:30', false, 'Om Prakash Prasad', '', '', '', false, true, '2026-05-24 18:06:58.997652+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (15, 'pbkdf2_sha256$1200000$oFqHJOlWVVtU8yrCLDTv98$MYOJhl4INaMfhx4Aj4A31Jp4Kn0zQ3mKOd2QRRkDJRc=', '2026-06-15 21:51:09.767154+05:30', false, 'nitish9199', '', '', '', false, true, '2026-06-02 21:06:07.828849+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (1, 'pbkdf2_sha256$1200000$G8AGyL76mAxXhAgXorZfGb$N+vAvSVfbamvME+3Pr9q/v858It4gVOajngKp+C/HjE=', '2026-06-16 17:43:57.339357+05:30', true, 'aditya0903admin', 'ADITYA', 'KUMAR', 'ak9598168@gmail.com', true, true, '2026-05-18 18:58:36+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (8, 'pbkdf2_sha256$1200000$dLJDgjEuaMhwdUpLrXssmt$SiaRkIskYOc7Khv739ZekqemHPpKByRrnA80GpiH0WU=', '2026-05-20 16:26:01.697795+05:30', false, 'runni1799', '', '', '', false, true, '2026-05-20 11:11:43.803005+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (9, 'pbkdf2_sha256$1200000$pjYcpuPNiOho47QPGSORG0$23QtS5M0BbdUxJL16xVAgKI2/QtQIuO5tUlTXCHvsCU=', '2026-05-21 11:12:19.277194+05:30', false, 'shivam5191', '', '', '', false, true, '2026-05-21 11:02:32.712731+05:30');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (10, 'pbkdf2_sha256$1200000$JMjQZSGckLUereoVQSIPeA$5U2ibyyDAUt88JaKKk7CnXZbbw33LZVzdel01wDc+EE=', '2026-05-21 11:15:04.881463+05:30', false, 'shivam6122', '', '', '', false, true, '2026-05-21 11:12:55.339715+05:30');


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: customers_app_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (3, 'REKHA DEVI', '7319866744', '713046161782', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (1, 'SANJAY KUMAR', '9060722730', '793744412031', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (4, 'Balvir Kumar', '6205795640', '928285366710', 6);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (5, 'RUBI DEVI', '7979023958', '751061354661', 7);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (6, 'RUNNI KUMARI', '7541086172', '431818781799', 8);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (9, 'SANJAY PANDIT', '9241836145', '467385018578', 11);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (8, 'Shivam parajapati', '9241836122', '823191655191', 10);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (10, 'ASHOK KUMAR', '7541254892', '487596542145', 12);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (11, 'Om Prakash Prasad', '8235860195', '313218579146', 13);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (12, 'PUMMI DEVI', '9229771533', '256245165824', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (13, 'Duggu Kumar', '7857004662', '283690746422', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (14, 'Abhikant Kumar', '7250030611', '733081227232', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (15, 'Abhishek Kumar', '8083160261', '250398967097', 14);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (16, 'Nitish Kumar', '9199891480', '662873419296', 15);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (17, 'Vishwjeet Kumar', '7004674650', '650062159781', 16);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (18, 'Ayush Kumar', '8986516775', '964903662347', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (19, 'JITU MISTRI', '9308893962', '991556990765', NULL);
INSERT INTO public.customers_app_customer (id, name, contact_no, aadhaar_no, user_id) VALUES (20, 'MANORMA DEVI', '7781865418', '762599078234', NULL);


--
-- Data for Name: customers_app_application; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (24, 'Income certificate', 'BICCO/2026/5827812', '2026-05-28', '2026-06-10 10:16:36.390765+05:30', 'Delivered', 14, 'under verification', '2026-06-10 10:16:36.390827+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (18, 'INCOME CERTIFICATE', 'BICCO/2026/5617491', '2026-05-22', '2026-06-02 19:22:18+05:30', 'Delivered', 9, 'application closed', '2026-06-02 19:23:11.513169+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (20, 'AYUSHMAN CARD', 'MT8S6N9IS', '2026-05-26', '2026-05-27 17:06:36+05:30', 'Delivered', 12, 'Application Closed', '2026-05-27 17:06:40.59138+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (19, 'Residence Certificate', 'BRCCO/2026/7149195', '2026-05-24', '2026-06-02 20:08:56.380297+05:30', 'Delivered', 11, 'approved by state office', '2026-06-02 20:08:56.3805+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (8, 'RESIDENCE CERTIFICATE', 'BRCCO/2026/7014067', '2026-05-21', '2026-06-02 20:10:11.573105+05:30', 'Delivered', 6, 'approved by RO', '2026-06-02 20:10:11.573183+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (10, 'INCOME CERTIFICATE', 'BICCO/2026/5582951', '2026-05-21', '2026-06-02 20:10:33.089854+05:30', 'Delivered', 6, 'approved by state office', '2026-06-02 20:10:33.089936+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (23, 'Caste Certificate', 'BCCCO/2026/5839140', '2026-05-28', '2026-06-10 10:16:23.798738+05:30', 'Delivered', 14, 'application closed', '2026-06-10 10:17:42.489515+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (9, 'CASTE CERTFICATE', 'BCCCO/2026/5590893', '2026-05-21', '2026-06-02 20:10:40.45564+05:30', 'Delivered', 6, 'approved by state office', '2026-06-02 20:10:40.4557+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (28, 'PAN CARD', '881133158132006', '2026-06-04', '2026-06-10 13:25:39.625918+05:30', 'Delivered', 5, 'PAN has been allotted by Income Tax Department, your PAN card is under process at Protean and will be despatched to you shortly.
Permanent Account Number (PAN)	:	LCXXXXXX3M', '2026-06-10 13:25:39.626057+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (15, 'RESIDENCE CERTIFICATE', 'BRCCO/2026/7015222', '2026-05-21', '2026-05-29 16:30:43+05:30', 'Delivered', 8, 'Application closed', '2026-05-29 16:30:46.152644+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (17, 'CASTE CERTFICATE', 'BCCCO/2026/5591864', '2026-05-21', '2026-05-29 16:30:55.086459+05:30', 'Delivered', 8, 'Application Approved by Department', '2026-05-29 16:30:55.086547+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (16, 'INCOME CERTIFICATE', 'BICCO/2026/5584094', '2026-05-21', '2026-05-29 16:31:05.354101+05:30', 'Delivered', 8, 'Application Approved by Department', '2026-05-29 16:31:05.354194+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (30, 'Pan Card', 'R017007850', '2026-06-05', '2026-06-10 13:28:46.173592+05:30', 'Delivered', 18, 'YOUR APPLICATION IS PROCESSED SUCCESSFULLY
PAN IS ALLOTTED, CARD IS UNDER PRINTING.', '2026-06-10 13:28:46.173669+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (22, 'Patliputra Addmission 2026-30', 'PPUP0056090', '2026-05-28', '2026-05-29 16:33:07+05:30', 'Delivered', 14, 'Application closed and acknowledge provided to applicant', '2026-05-29 16:33:43.093751+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (26, 'Non Creamy Layer (Central Govt)', 'BOBCCO/2026/785486', '2026-06-01', NULL, 'In Process', 15, 'forwarded to concerned official', '2026-06-10 13:28:57.588077+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (25, 'Non Creamy Layer (Bihar Govt)', 'NCLCO/2026/687252', '2026-06-01', NULL, 'In Process', 15, 'forwarded to concerned official', '2026-06-10 13:29:09.293589+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (7, 'VOTER ID CARD', 'S04178O8C2005261200008', '2026-05-20', '2026-06-04 10:07:42.455862+05:30', 'Delivered', 5, 'FVR SUBMITTED', '2026-06-04 10:07:42.455966+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (32, 'AYUSHMAN CARD', '102300139924518400000307', '2026-06-12', '2026-06-12 20:10:39.952321+05:30', 'Delivered', 20, 'Approved by NHA', '2026-06-12 20:10:39.952391+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (31, 'PENSION EKYC', '000012258880', '2026-06-11', '2026-06-13 13:50:19.571646+05:30', 'Delivered', 19, 'sent to verification', '2026-06-13 13:50:19.571813+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (29, 'Pan Card', 'K006833630', '2026-06-05', NULL, 'Approved', 17, 'application closed and will be delivered to you', '2026-06-16 17:45:36.247951+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (21, 'Aadhar Biometric Update', 'A180427120033726052716571497', '2026-05-27', '2026-06-06 13:49:20.599526+05:30', 'Delivered', 13, 'Application is in process with UIDAI with enrollment no. 271212345620826

Date - 29-05-2026
Time - 12:29:47', '2026-06-06 13:49:20.599602+05:30');
INSERT INTO public.customers_app_application (id, application_name, application_no, application_date, delivery_date, status, customer_id, remarks, status_updated_at) VALUES (27, 'Pan Card', 'R017233035', '2026-06-02', '2026-06-07 12:55:37.259261+05:30', 'Delivered', 16, 'YOUR APPLICATION IS PROCESSED SUCCESSFULLY
PAN IS ALLOTTED.
PAN No.	RL******5A', '2026-06-07 12:55:37.259407+05:30');


--
-- Data for Name: customers_app_applicationstatushistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (17, 'Pending', 'Accepted', '2026-05-20 10:38:24.922415+05:30', 7);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (23, 'PENDING', 'RESENT', '2026-05-21 10:42:06.916438+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (24, 'PENDING', 'RESENT', '2026-05-21 10:42:22.297299+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (25, 'PENDING', 'RESENT', '2026-05-21 10:42:37.244887+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (26, 'PENDING', 'ACCEPTED', '2026-05-21 11:04:35.590854+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (27, 'PENDING', 'ACCEPTED', '2026-05-21 11:04:49.195309+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (28, 'PENDING', '', '2026-05-21 11:05:01.695067+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (29, 'Pending', 'ACCEPTED', '2026-05-21 11:13:59.714041+05:30', 16);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (30, 'Pending', 'ACCEPTED', '2026-05-21 11:14:24.904097+05:30', 17);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (31, 'Submitted', 'FORWARDED TO CONCERNED OFFICIAL', '2026-05-22 11:18:40.122269+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (32, 'Submitted', 'DATA RESENT', '2026-05-22 11:24:59.422949+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (33, 'Submitted', 'FORWARDED TO CONCERNED OFFICIAL', '2026-05-22 11:25:15.703605+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (34, 'Submitted', 'FORWARDED TO CONCERNED OFFICIAL', '2026-05-22 11:25:39.72544+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (35, 'In Process', 'FVR SUBMITTED', '2026-05-22 21:28:47.733285+05:30', 7);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (36, 'Submitted', 'application sent to concerned officials', '2026-05-22 21:30:00.794657+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (37, 'Pending', 'Application uploaded to government Portal', '2026-05-24 18:21:11.426927+05:30', 19);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (38, 'In Process', 'Applcation is under verification', '2026-05-24 18:26:16.461706+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (39, 'In Process', 'Applcation is under verification', '2026-05-24 18:26:28.141868+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (40, 'In Process', 'Applcation is under verification', '2026-05-24 18:26:40.643311+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (41, 'Pending', 'application forwarded', '2026-05-26 15:25:27.145674+05:30', 20);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (42, 'In Process', 'Application under verification', '2026-05-26 15:32:35.118925+05:30', 20);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (43, 'Approved', 'Application approved please collect it from concern application center', '2026-05-26 19:54:13.941418+05:30', 20);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (44, 'Approved', 'Application Approved by Department', '2026-05-26 19:58:53.39592+05:30', 15);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (45, 'Approved', 'Application Approved by Department', '2026-05-26 19:59:06.166627+05:30', 16);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (46, 'Approved', 'Application Approved by Department', '2026-05-26 19:59:38.731232+05:30', 17);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (47, 'Pending', 'Application accepted', '2026-05-27 17:05:34.710087+05:30', 21);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (48, 'Delivered', 'Application Closed', '2026-05-27 17:06:40.593768+05:30', 20);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (49, 'Pending', 'Application accepted', '2026-05-28 21:55:14.878353+05:30', 22);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (50, 'Pending', 'accepted', '2026-05-28 22:02:54.712215+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (51, 'Submitted', 'Application submitted at PPU Samarth 2026 Portal', '2026-05-28 22:03:34.426762+05:30', 22);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (52, 'Pending', 'Accepted', '2026-05-28 22:06:42.430777+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (53, 'In Process', 'Application successfully processed by Aditya Cyber Zone', '2026-05-28 22:07:25.655428+05:30', 22);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (54, 'Submitted', 'Application forwarded to UIDAI portal for appointment booked on 29/05/2026  - 13:00PM.
Please visit to Addhar center.', '2026-05-28 22:28:15.67197+05:30', 21);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (55, 'In Process', 'Application is in process with UIDAI with enrollment no. 271212345620826

Date - 29-05-2026
Time - 12:29:47', '2026-05-29 16:28:50.227903+05:30', 21);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (56, 'Submitted', 'Forwarded to concerned officials', '2026-05-29 16:29:41.986776+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (57, 'Submitted', 'Forwarded to concerned officials', '2026-05-29 16:29:53.900032+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (58, 'Submitted', 'Forwarded to concerned officials', '2026-05-29 16:30:09.646861+05:30', 19);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (59, 'Delivered', 'Application closed', '2026-05-29 16:30:46.154762+05:30', 15);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (60, 'Delivered', 'Application Approved by Department', '2026-05-29 16:30:55.088875+05:30', 17);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (61, 'Delivered', 'Application Approved by Department', '2026-05-29 16:31:05.35658+05:30', 16);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (62, 'In Process', 'application under verification', '2026-05-29 16:32:39.554464+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (63, 'Delivered', 'Application closed and acknowledge provided to applicant', '2026-05-29 16:33:43.095051+05:30', 22);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (64, 'Approved', 'approved by RO', '2026-05-29 16:42:40.006765+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (65, 'Pending', 'accepted', '2026-06-01 20:37:20.262053+05:30', 25);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (66, 'Pending', 'accepted', '2026-06-01 20:38:07.798802+05:30', 26);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (67, 'Submitted', 'forwarded to concerned official', '2026-06-01 20:39:40.220874+05:30', 25);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (68, 'Submitted', 'forwarded to concerned official', '2026-06-01 20:39:52.016894+05:30', 26);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (69, 'Approved', 'approved by state office', '2026-06-01 20:42:45.76752+05:30', 19);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (70, 'Approved', 'approved by state office', '2026-06-01 20:45:33.514494+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (71, 'Approved', 'approved by state office', '2026-06-01 20:46:55.536343+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (72, 'Approved', 'approved by state office', '2026-06-01 20:47:54.645485+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (73, 'In Process', 'under verification', '2026-06-02 18:15:27.540081+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (74, 'In Process', 'under verification', '2026-06-02 18:15:46.171527+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (75, 'Submitted', 'under verification by revenue officer/BDO', '2026-06-02 18:41:43.580235+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (76, 'Delivered', 'ready to delivered', '2026-06-02 18:44:51.705017+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (77, 'Rejected', 'rejected by adss', '2026-06-02 18:59:47.550345+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (78, 'Pending', 'rejected by adss', '2026-06-02 19:10:50.810871+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (79, 'Submitted', 'rejected by adss', '2026-06-02 19:14:42.679658+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (80, 'Delivered', 'application closed', '2026-06-02 19:23:11.516711+05:30', 18);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (81, 'Delivered', NULL, '2026-06-02 20:08:56.384731+05:30', 19);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (82, 'Delivered', NULL, '2026-06-02 20:10:11.57626+05:30', 8);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (83, 'Delivered', NULL, '2026-06-02 20:10:33.092591+05:30', 10);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (84, 'Delivered', NULL, '2026-06-02 20:10:40.458215+05:30', 9);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (85, 'Pending', 'under process by cyber', '2026-06-02 21:11:26.314434+05:30', 27);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (86, 'Submitted', 'forwarded to UTIITSL Agency', '2026-06-02 21:36:42.4314+05:30', 27);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (87, 'In Process', 'YOUR APPLICATION IS UNDER PROCESSING
PAN UNDER ALLOTMENT, AWAITING CONFIRMATION FROM INCOME TAX DEPARTMENT.', '2026-06-03 12:11:03.343958+05:30', 27);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (88, 'In Process', NULL, '2026-06-03 12:12:11.532999+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (89, 'In Process', NULL, '2026-06-03 12:12:23.42301+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (90, 'Approved', NULL, '2026-06-03 21:33:31.915423+05:30', 7);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (91, 'Delivered', NULL, '2026-06-03 21:35:53.380077+05:30', 7);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (92, 'Approved', 'YOUR APPLICATION IS PROCESSED SUCCESSFULLY
PAN IS ALLOTTED.
PAN No.	RL******5A', '2026-06-04 09:30:22.910654+05:30', 27);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (93, 'Delivered', NULL, '2026-06-04 10:07:42.460871+05:30', 7);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (94, 'Submitted', 'forwarded to nsdl', '2026-06-04 10:57:47.698353+05:30', 28);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (95, 'Pending', 'yet to upload pan documents', '2026-06-05 07:05:19.960481+05:30', 29);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (96, 'Submitted', 'application forwarded to UTIITSL Agency', '2026-06-05 17:31:53.69651+05:30', 29);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (97, 'Pending', 'pan document yet to upload', '2026-06-05 18:06:06.170887+05:30', 30);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (98, 'Submitted', 'application forwarded to UTIITSL Agency', '2026-06-05 18:09:33.330473+05:30', 30);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (99, 'Approved', NULL, '2026-06-05 20:07:43.577405+05:30', 21);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (100, 'In Process', NULL, '2026-06-06 13:48:26.872569+05:30', 28);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (101, 'Delivered', NULL, '2026-06-06 13:49:20.602105+05:30', 21);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (102, 'Delivered', NULL, '2026-06-07 12:55:37.264894+05:30', 27);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (103, 'In Process', 'Application is received and is under verification', '2026-06-07 12:57:47.019717+05:30', 30);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (104, 'In Process', 'Application is received and is under verification', '2026-06-07 12:57:47.026881+05:30', 29);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (105, 'Approved', 'PAN has been allotted by Income Tax Department, your PAN card is under process at Protean and will be despatched to you shortly.
Permanent Account Number (PAN)	:	LCXXXXXX3M', '2026-06-08 09:20:36.703473+05:30', 28);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (106, 'Approved', NULL, '2026-06-09 09:22:37.278846+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (107, 'Approved', NULL, '2026-06-09 21:31:12.228703+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (108, 'Approved', 'YOUR APPLICATION IS PROCESSED SUCCESSFULLY
PAN IS ALLOTTED, CARD IS UNDER PRINTING.', '2026-06-10 10:15:09.579604+05:30', 30);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (109, 'Delivered', NULL, '2026-06-10 10:16:23.801785+05:30', 23);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (110, 'Delivered', NULL, '2026-06-10 10:16:36.3934+05:30', 24);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (111, 'Delivered', NULL, '2026-06-10 13:25:39.630632+05:30', 28);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (112, 'Delivered', NULL, '2026-06-10 13:28:46.176304+05:30', 30);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (113, 'In Process', NULL, '2026-06-10 13:28:57.592387+05:30', 26);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (114, 'In Process', NULL, '2026-06-10 13:29:09.298806+05:30', 25);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (115, 'Submitted', 'sent to verification', '2026-06-11 19:16:49.821445+05:30', 31);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (116, 'In Process', 'sent to verification', '2026-06-11 19:17:28.347096+05:30', 31);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (117, 'Submitted', 'forwarded to nha', '2026-06-12 16:53:21.58519+05:30', 32);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (118, 'In Process', 'forwarded to nha', '2026-06-12 17:47:55.340231+05:30', 32);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (119, 'Approved', 'Approved by NHA', '2026-06-12 20:02:40.154692+05:30', 32);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (120, 'Delivered', NULL, '2026-06-12 20:10:39.954739+05:30', 32);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (121, 'Approved', NULL, '2026-06-12 20:11:26.398293+05:30', 31);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (122, 'Delivered', NULL, '2026-06-13 13:50:19.576112+05:30', 31);
INSERT INTO public.customers_app_applicationstatushistory (id, status, remark, updated_at, application_id) VALUES (123, 'Approved', 'application closed and will be delivered to you', '2026-06-16 17:45:36.249175+05:30', 29);


--
-- Data for Name: customers_app_grievance; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers_app_grievance (id, ticket_no, description, status, remarks, created_at, category, mobile, name, priority) VALUES (5, 'GRV-00001', 'I had applied for NCL and OBC but it''s status is still in process from last 15 days. My Application numbers are mentioned below
NCLCO/2026/687252
BOBCCO/2026/785486', 'In Process', 'Please wait while your complaint is under review. We will be in touch with you within 24 hrs.', '2026-06-13 13:59:59.194076+05:30', 'Status Update Issue', '8083160261', 'Abhishek Kumar', 'Normal');


--
-- Data for Name: customers_app_grievancehistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers_app_grievancehistory (id, status, remarks, created_at, grievance_id) VALUES (4, 'Under Review', 'Please wait while your complaint is under review.', '2026-06-13 13:59:59.197107+05:30', 5);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (1, '2026-05-18 19:01:40.896867+05:30', '1', 'SANJAY KUMAR', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (2, '2026-05-18 19:02:19.895682+05:30', '1', 'PAN CARD', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (3, '2026-05-18 19:02:34.126442+05:30', '1', 'PAN CARD', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (4, '2026-05-18 19:07:16.220267+05:30', '1', 'PAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (5, '2026-05-18 19:08:50.406833+05:30', '2', 'sanjay2512', 1, '[{"added": {}}]', 4, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (6, '2026-05-18 19:15:17.496231+05:30', '2', 'ADITYA KUMAR', 2, '[{"added": {"name": "application", "object": "VOTER ID CARD"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (7, '2026-05-18 19:16:32.55678+05:30', '2', 'ADITYA KUMAR', 2, '[{"changed": {"name": "application", "object": "VOTER ID CARD", "fields": ["Status"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (8, '2026-05-18 19:18:05.297661+05:30', '3', 'VOTER ID CARD', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (9, '2026-05-18 19:20:04.66008+05:30', '3', 'PAN CARD - Approval', 2, '[{"changed": {"fields": ["Status", "Remark"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (10, '2026-05-18 19:23:21.796971+05:30', '3', 'PAN CARD - APPROVED', 2, '[{"changed": {"fields": ["Status", "Remark"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (11, '2026-05-18 19:24:14.731179+05:30', '2', 'VOTER ID CARD', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (12, '2026-05-18 19:25:48.802658+05:30', '4', 'RESIDENE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (13, '2026-05-18 19:30:39.900727+05:30', '3', 'REKHA DEVI', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (14, '2026-05-18 19:31:13.403845+05:30', '5', 'UDID', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (15, '2026-05-18 19:32:04.899931+05:30', '5', 'UDID', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (16, '2026-05-18 19:44:28.808245+05:30', '4', 'aditya0903', 3, '', 4, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (17, '2026-05-18 22:09:47.788825+05:30', '5', 'UDID', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (18, '2026-05-18 22:12:30.295783+05:30', '1', 'PAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (19, '2026-05-19 10:46:29.521421+05:30', '1', 'PAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (20, '2026-05-19 10:49:46.497015+05:30', '5', 'UDID', 2, '[{"changed": {"fields": ["Delivery date", "Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (21, '2026-05-20 09:54:24.130191+05:30', '1', 'SANJAY KUMAR', 2, '[{"changed": {"name": "application", "object": "PAN CARD", "fields": ["Status"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (22, '2026-05-20 09:59:41.572194+05:30', '4', 'Balvir Kumar', 2, '[{"changed": {"fields": ["Name"]}}, {"added": {"name": "application", "object": "CASTE CERTIFICATE"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (23, '2026-05-20 10:00:21.319481+05:30', '4', 'Balvir Kumar', 2, '[{"changed": {"name": "application", "object": "CASTE CERTIFICATE", "fields": ["Status", "Remarks"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (24, '2026-05-20 10:01:05.200022+05:30', '4', 'Balvir Kumar', 2, '[{"changed": {"name": "application", "object": "CASTE CERTIFICATE", "fields": ["Status"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (25, '2026-05-20 10:01:38.74778+05:30', '13', 'CASTE CERTIFICATE - In Process', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (26, '2026-05-20 10:02:10.023032+05:30', '6', 'CASTE CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (27, '2026-05-20 10:03:19.499997+05:30', '6', 'CASTE CERTIFICATE', 2, '[{"changed": {"fields": ["Delivery date", "Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (28, '2026-05-20 10:08:43.601169+05:30', '6', 'CASTE CERTIFICATE', 3, '', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (29, '2026-05-20 10:35:52.509832+05:30', '5', 'RUBI DEVI', 2, '[{"added": {"name": "application", "object": "VOTER ID CARD"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (30, '2026-05-20 10:38:24.991905+05:30', '17', 'VOTER ID CARD - Pending', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (31, '2026-05-20 10:49:12.905215+05:30', '5', 'UDID', 3, '', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (32, '2026-05-20 10:49:12.905261+05:30', '1', 'PAN CARD', 3, '', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (33, '2026-05-20 11:13:29.408274+05:30', '8', 'RESIDENCE CERTIFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (34, '2026-05-20 11:13:56.401688+05:30', '9', 'CASTE CERTFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (35, '2026-05-20 11:14:16.648146+05:30', '10', 'INCOME CERTIFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (36, '2026-05-21 10:37:18.373265+05:30', '10', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Application no", "Application date", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (37, '2026-05-21 10:37:58.616724+05:30', '6', 'RUNNI KUMARI', 2, '[{"changed": {"name": "application", "object": "RESIDENCE CERTIFICATE", "fields": ["Application no", "Application date", "Remarks"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (38, '2026-05-21 10:38:29.134009+05:30', '6', 'RUNNI KUMARI', 2, '[{"changed": {"name": "application", "object": "CASTE CERTFICATE", "fields": ["Application no", "Application date", "Remarks"]}}, {"changed": {"name": "application", "object": "INCOME CERTIFICATE", "fields": ["Remarks"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (39, '2026-05-21 10:39:55.312592+05:30', '20', 'INCOME CERTIFICATE - Pending', 3, '', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (40, '2026-05-21 10:39:55.312634+05:30', '19', 'CASTE CERTFICATE - Pending', 3, '', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (41, '2026-05-21 10:39:55.312653+05:30', '18', 'RESIDENCE CERTIFICATE - Pending', 3, '', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (42, '2026-05-21 10:40:19.1053+05:30', '8', 'RESIDENCE CERTIFICATE', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (43, '2026-05-21 10:41:15.994289+05:30', '11', 'RESIDENCE CERTIFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (44, '2026-05-21 10:41:23.528983+05:30', '22', 'RESIDENCE CERTIFICATE - Pending', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (45, '2026-05-21 10:41:45.499089+05:30', '22', 'RESIDENCE CERTIFICATE - Pending', 3, '', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (46, '2026-05-21 10:41:45.499129+05:30', '21', 'RESIDENCE CERTIFICATE - Pending', 3, '', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (47, '2026-05-21 10:42:06.917653+05:30', '23', 'INCOME CERTIFICATE - BICCO/2026/5582951', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (48, '2026-05-21 10:42:22.298523+05:30', '24', 'RESIDENCE CERTIFICATE - BRCCO/2026/7014067', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (49, '2026-05-21 10:42:37.295085+05:30', '25', 'CASTE CERTFICATE - BCCCO/2026/5590893', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (50, '2026-05-21 10:46:13.616538+05:30', '11', 'RESIDENCE CERTIFICATE', 3, '', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (51, '2026-05-21 11:03:47.710995+05:30', '7', 'Shivam parajapati', 2, '[{"changed": {"fields": ["Name"]}}, {"added": {"name": "application", "object": "RESIDENCE CERTIFICATE"}}, {"added": {"name": "application", "object": "CASTE CERTFICATE"}}, {"added": {"name": "application", "object": "INCOME CERTIFICATE"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (52, '2026-05-21 11:04:35.592434+05:30', '26', 'CASTE CERTFICATE - BCCCO/2026/5591864', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (53, '2026-05-21 11:04:49.19704+05:30', '27', 'INCOME CERTIFICATE - BICCO/2026/5584094', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (54, '2026-05-21 11:05:01.696918+05:30', '28', 'RESIDENCE CERTIFICATE - BRCCO/2026/7015222ACCEPTED', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (55, '2026-05-21 11:05:39.911739+05:30', '23', 'INCOME CERTIFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (56, '2026-05-21 11:05:54.628274+05:30', '24', 'RESIDENCE CERTIFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (57, '2026-05-21 11:06:01.49588+05:30', '25', 'CASTE CERTFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (58, '2026-05-21 11:06:08.504354+05:30', '26', 'CASTE CERTFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (59, '2026-05-21 11:06:15.618907+05:30', '27', 'INCOME CERTIFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (60, '2026-05-21 11:06:23.195701+05:30', '28', 'RESIDENCE CERTIFICATE - PENDING', 2, '[{"changed": {"fields": ["Status"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (61, '2026-05-21 11:08:36.571347+05:30', '7', 'Shivam parajapati', 2, '[]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (62, '2026-05-21 11:09:23.59769+05:30', '7', 'Shivam parajapati', 3, '', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (63, '2026-05-21 11:13:28.000872+05:30', '8', 'Shivam parajapati', 2, '[{"changed": {"fields": ["Name"]}}, {"added": {"name": "application", "object": "RESIDENCE CERTIFICATE"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (64, '2026-05-21 11:13:59.715325+05:30', '16', 'INCOME CERTIFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (65, '2026-05-21 11:14:24.907726+05:30', '17', 'CASTE CERTFICATE', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (66, '2026-05-22 11:18:12.766777+05:30', '9', 'SANJAY PANDIT', 2, '[{"added": {"name": "application", "object": "INCOME CERTIFICATE"}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (67, '2026-05-22 11:18:40.123713+05:30', '31', 'INCOME CERTIFICATE - Pending', 1, '[{"added": {}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (134, '2026-06-05 17:31:53.699355+05:30', '29', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (68, '2026-05-22 11:20:21.816834+05:30', '8', 'Shivam parajapati', 2, '[{"changed": {"name": "application", "object": "RESIDENCE CERTIFICATE", "fields": ["Status", "Remarks"]}}, {"changed": {"name": "application", "object": "INCOME CERTIFICATE", "fields": ["Status", "Remarks"]}}, {"changed": {"name": "application", "object": "CASTE CERTFICATE", "fields": ["Status", "Remarks"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (69, '2026-05-22 11:20:49.656029+05:30', '8', 'Shivam parajapati', 2, '[]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (70, '2026-05-22 11:21:06.316544+05:30', '17', 'CASTE CERTFICATE', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (71, '2026-05-22 11:21:12.844062+05:30', '16', 'INCOME CERTIFICATE', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (72, '2026-05-22 11:21:20.093887+05:30', '15', 'RESIDENCE CERTIFICATE', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (73, '2026-05-22 11:21:36.989922+05:30', '15', 'RESIDENCE CERTIFICATE', 2, '[]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (74, '2026-05-22 11:22:54.347057+05:30', '31', 'INCOME CERTIFICATE - Submitted', 2, '[{"changed": {"fields": ["Status", "Remark"]}}]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (75, '2026-05-22 11:24:59.424688+05:30', '10', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (76, '2026-05-22 11:25:15.705409+05:30', '9', 'CASTE CERTFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (77, '2026-05-22 11:25:39.726751+05:30', '8', 'RESIDENCE CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (78, '2026-05-22 21:28:47.738734+05:30', '7', 'VOTER ID CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (79, '2026-05-22 21:30:00.795904+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (80, '2026-05-24 18:21:11.430998+05:30', '19', 'Residence Certificate', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (81, '2026-05-24 18:21:28.486563+05:30', '37', 'Residence Certificate - Pending', 2, '[]', 8, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (82, '2026-05-24 18:26:16.464371+05:30', '8', 'RESIDENCE CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (83, '2026-05-24 18:26:28.145027+05:30', '9', 'CASTE CERTFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (84, '2026-05-24 18:26:40.644414+05:30', '10', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (85, '2026-05-26 15:24:10.15281+05:30', '12', 'PUMMI DEVI', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (86, '2026-05-26 15:25:27.146847+05:30', '20', 'AYUSHMAN CARD', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (87, '2026-05-26 15:32:35.121236+05:30', '20', 'AYUSHMAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (88, '2026-05-26 19:54:13.995157+05:30', '20', 'AYUSHMAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (89, '2026-05-26 19:58:53.397116+05:30', '15', 'RESIDENCE CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (90, '2026-05-26 19:59:06.172142+05:30', '16', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (91, '2026-05-26 19:59:38.73278+05:30', '17', 'CASTE CERTFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (92, '2026-05-27 17:04:26.601816+05:30', '13', 'Duggu Kumar', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (93, '2026-05-27 17:05:34.711279+05:30', '21', 'Aadhar Biometric Update', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (94, '2026-05-27 17:06:40.595324+05:30', '20', 'AYUSHMAN CARD', 2, '[{"changed": {"fields": ["Delivery date", "Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (95, '2026-05-28 21:53:52.803775+05:30', '14', 'Abhikant Kumar', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (96, '2026-05-28 21:55:14.930037+05:30', '22', 'Patliputra Addmission 2026-30', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (97, '2026-05-28 22:02:54.713696+05:30', '23', 'Caste Certificate', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (98, '2026-05-28 22:03:34.429745+05:30', '22', 'Patliputra Addmission 2026-30', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (99, '2026-05-28 22:06:42.431692+05:30', '24', 'Income certificate', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (100, '2026-05-28 22:07:25.656604+05:30', '22', 'Patliputra Addmission 2026-30', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (101, '2026-05-28 22:28:15.673804+05:30', '21', 'Aadhar Biometric Update', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (102, '2026-05-29 16:28:50.229508+05:30', '21', 'Aadhar Biometric Update', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (103, '2026-05-29 16:29:41.988648+05:30', '24', 'Income certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (104, '2026-05-29 16:29:53.902731+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (105, '2026-05-29 16:30:09.647887+05:30', '19', 'Residence Certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (106, '2026-05-29 16:30:46.155859+05:30', '15', 'RESIDENCE CERTIFICATE', 2, '[{"changed": {"fields": ["Delivery date", "Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (107, '2026-05-29 16:32:39.555882+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (108, '2026-05-29 16:33:43.096076+05:30', '22', 'Patliputra Addmission 2026-30', 2, '[{"changed": {"fields": ["Delivery date", "Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (109, '2026-05-29 16:42:40.008194+05:30', '8', 'RESIDENCE CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (110, '2026-06-01 20:37:20.264303+05:30', '25', 'Non Creamy Layer (Bihar Govt)', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (111, '2026-06-01 20:38:07.799851+05:30', '26', 'Non Creamy Layer (Central Govt)', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (112, '2026-06-01 20:39:40.222375+05:30', '25', 'Non Creamy Layer (Bihar Govt)', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (113, '2026-06-01 20:39:52.017949+05:30', '26', 'Non Creamy Layer (Central Govt)', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (114, '2026-06-01 20:42:45.76887+05:30', '19', 'Residence Certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (115, '2026-06-01 20:45:33.515627+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (116, '2026-06-01 20:46:55.537316+05:30', '10', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (117, '2026-06-01 20:47:54.647413+05:30', '9', 'CASTE CERTFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (118, '2026-06-02 18:15:27.612703+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (119, '2026-06-02 18:15:46.172575+05:30', '24', 'Income certificate', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (120, '2026-06-02 18:35:35.071188+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (121, '2026-06-02 18:41:22.709979+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (122, '2026-06-02 18:41:43.58151+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (123, '2026-06-02 18:44:51.706252+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (124, '2026-06-02 18:59:47.552848+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (125, '2026-06-02 19:10:50.8134+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (126, '2026-06-02 19:14:42.68454+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (127, '2026-06-02 19:23:11.518984+05:30', '18', 'INCOME CERTIFICATE', 2, '[{"changed": {"fields": ["Delivery date", "Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (128, '2026-06-02 21:11:26.320601+05:30', '27', 'Pan Card', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (129, '2026-06-02 21:36:42.432662+05:30', '27', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (130, '2026-06-03 12:11:03.351813+05:30', '27', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (131, '2026-06-04 09:30:22.998383+05:30', '27', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (132, '2026-06-04 10:57:47.699977+05:30', '28', 'PAN CARD', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (133, '2026-06-05 07:05:19.962861+05:30', '29', 'Pan Card', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (135, '2026-06-05 18:05:11.63615+05:30', '18', 'Ayush Kumar', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (136, '2026-06-05 18:06:06.172476+05:30', '30', 'Pan Card', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (137, '2026-06-05 18:09:33.333056+05:30', '30', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (138, '2026-06-05 18:43:48.83539+05:30', '1', 'ACZ-GR-0001', 2, '[{"changed": {"fields": ["Status"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (139, '2026-06-06 21:02:21.924903+05:30', '1', 'ACZ-GR-0001', 2, '[{"changed": {"fields": ["Status"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (140, '2026-06-06 21:17:43.381678+05:30', '2', 'GRV-00002', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (141, '2026-06-06 21:22:30.913822+05:30', '2', 'GRV-00002', 3, '', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (142, '2026-06-06 21:22:30.913857+05:30', '1', 'ACZ-GR-0001', 3, '', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (143, '2026-06-06 21:26:40.78169+05:30', '3', 'GRV-00001', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (144, '2026-06-06 21:27:34.642992+05:30', '2', 'In process', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (145, '2026-06-06 21:28:35.687723+05:30', '2', 'Rejected', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (146, '2026-06-06 21:29:16.596605+05:30', '3', 'GRV-00001', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (147, '2026-06-06 21:44:11.884606+05:30', '4', 'GRV-00002', 2, '[{"changed": {"fields": ["Status"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (148, '2026-06-07 12:57:47.021838+05:30', '30', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (149, '2026-06-07 12:57:47.028912+05:30', '29', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (150, '2026-06-08 09:20:36.708147+05:30', '28', 'PAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (151, '2026-06-08 13:38:44.115338+05:30', '4', 'GRV-00002', 2, '[{"changed": {"fields": ["Status"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (152, '2026-06-08 18:58:50.341306+05:30', '4', 'GRV-00002', 3, '', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (153, '2026-06-08 18:58:50.34136+05:30', '3', 'GRV-00001', 3, '', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (154, '2026-06-10 10:15:09.586001+05:30', '30', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (155, '2026-06-10 10:17:42.490884+05:30', '23', 'Caste Certificate', 2, '[{"changed": {"fields": ["Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (156, '2026-06-10 18:42:59.458521+05:30', '1', 'aditya0903admin', 2, '[{"changed": {"fields": ["First name", "Last name"]}}]', 4, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (157, '2026-06-11 19:15:53.288623+05:30', '19', 'JITU MISTRI', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (158, '2026-06-11 19:16:49.823636+05:30', '31', 'PENSION EKYC', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (159, '2026-06-11 19:17:28.348936+05:30', '31', 'PENSION EKYC', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (160, '2026-06-12 16:52:13.828852+05:30', '20', 'MANORMA DEV', 1, '[{"added": {}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (161, '2026-06-12 16:52:39.495786+05:30', '20', 'MANORMA DEVI', 2, '[{"changed": {"fields": ["Name"]}}]', 9, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (162, '2026-06-12 16:53:21.586569+05:30', '32', 'AYUSHMAN CARD', 1, '[{"added": {}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (163, '2026-06-12 17:47:55.343234+05:30', '32', 'AYUSHMAN CARD', 2, '[{"changed": {"fields": ["Status"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (164, '2026-06-12 20:02:40.157212+05:30', '32', 'AYUSHMAN CARD', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (165, '2026-06-13 14:04:19.993666+05:30', '4', 'Under Review', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 11, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (166, '2026-06-13 14:08:05.25026+05:30', '5', 'GRV-00001', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 10, 1);
INSERT INTO public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) VALUES (167, '2026-06-16 17:45:36.251267+05:30', '29', 'Pan Card', 2, '[{"changed": {"fields": ["Status", "Remarks"]}}]', 7, 1);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2026-05-18 18:37:12.410982+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (2, 'auth', '0001_initial', '2026-05-18 18:37:12.699627+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (3, 'admin', '0001_initial', '2026-05-18 18:37:12.719653+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2026-05-18 18:37:12.8014+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-18 18:37:12.809686+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2026-05-18 18:37:12.824091+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2026-05-18 18:37:12.912915+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (8, 'auth', '0003_alter_user_email_max_length', '2026-05-18 18:37:12.922668+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (9, 'auth', '0004_alter_user_username_opts', '2026-05-18 18:37:13.007591+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (10, 'auth', '0005_alter_user_last_login_null', '2026-05-18 18:37:13.017659+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (11, 'auth', '0006_require_contenttypes_0002', '2026-05-18 18:37:13.021279+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2026-05-18 18:37:13.031463+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (13, 'auth', '0008_alter_user_username_max_length', '2026-05-18 18:37:13.118529+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2026-05-18 18:37:13.127644+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (15, 'auth', '0010_alter_group_name_max_length', '2026-05-18 18:37:13.212737+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (16, 'auth', '0011_update_proxy_permissions', '2026-05-18 18:37:13.221966+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2026-05-18 18:37:13.312198+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (18, 'customers_app', '0001_initial', '2026-05-18 18:37:13.318621+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (19, 'customers_app', '0002_rename_contact_number_customer_contact_no_and_more', '2026-05-18 18:37:13.344643+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (20, 'customers_app', '0003_application_remarks_alter_application_application_no_and_more', '2026-05-18 18:37:13.429455+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (21, 'customers_app', '0004_alter_customer_aadhaar_no', '2026-05-18 18:37:13.492083+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (22, 'customers_app', '0005_alter_application_delivery_date', '2026-05-18 18:37:13.511359+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (23, 'customers_app', '0006_customer_user', '2026-05-18 18:37:13.524003+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (24, 'customers_app', '0007_applicationstatushistory', '2026-05-18 18:37:13.614148+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (25, 'customers_app', '0008_application_status_updated_at', '2026-05-18 18:37:13.62518+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (26, 'sessions', '0001_initial', '2026-05-18 18:37:13.639048+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (27, 'customers_app', '0009_grievance', '2026-06-05 18:28:34.801494+05:30');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (28, 'customers_app', '0010_remove_grievance_customer_remove_grievance_subject_and_more', '2026-06-06 21:00:06.40404+05:30');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('7h338gkbqp5fgy15bmw3tt89f104q6x4', '.eJxVzMEOwiAQBNB_4WyItLsUPHr3GwjsbqVqaFLak_HfLUkPep15M28V4rbmsFVZwsTqokCdfrMU6SmlFfyI5T5rmsu6TEk3oo-26tvM8roe9u8gx5r3tTkzdpAMOAInEXx0CLYnNCQuoeuHJJ4YsUPb2M4NwjjK4C2TJfX5AsrBN4E:1wOyLL:f-Ec7iZ_PBubF1hz1TfWw9hllyzgFC_Jf6RrSUBlz40', '2026-06-01 19:19:15.419072+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('elfww6chuj6gtck4z9iqcyah7gqirzu8', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wUzoy:K2I5L5txDyO8P-_c-F-7YlKEbtIb4S5W7f6SKrrwDmU', '2026-06-18 10:06:44.926983+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('j59h3sbi0ysn4gectb77dgydrts6dyhl', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wVJRz:1nMQ_OKVWUBkGPMtgPpwamxSYgHn6cp-c4r2_AfSJjU', '2026-06-19 07:04:19.583464+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('65eo7cpjjg6l2vg5xrz121j0k90vzw3r', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wVN44:3OvkoFAwq1SySQI-G6F8o0Tuhmxjbbqb5XE2vsoszdI', '2026-06-19 10:55:52.646276+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('890rkc732syp4zu3i2w6smfxo2ygdfkf', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wVt0C:0r43cjo88OiowY8h4HcYfUN_Mja8gcrsz1LuH5gLYgI', '2026-06-20 21:02:00.153075+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('am10aan6wakwmqamcxcoul5lrj3ffw4p', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wXDle:6iiXPi_2G793mTtuT9kz6_uNn4Zo1vgDT2sVbY2eMhs', '2026-06-24 13:24:30.265936+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('hcrxznodp7wv3xujdzho1xfwpdwk6bie', '.eJxVjEEOwiAQRe_C2hAgQ3FcuvcMZBimUjWQlHbVeHdt0oVu_3vvbyrSupS4dpnjlNVFWVCn3zERP6XuJD-o3pvmVpd5SnpX9EG7vrUsr-vh_h0U6uVbo5gBzoQ0ePEmMSAAOmSAjCEgOQrEhsOYAhpgR94SWhBKo1ifQb0_-Qk4Dw:1wY4JL:wMNzj2XU-7uNKXFbDLJ-gXOC-hH_J1d9crbUsgsitEM', '2026-06-26 21:30:47.5961+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('hmg5rvwdz6lmok718wg728nmm1hfwld5', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wYJmV:e-oOEcqNaH4S0J6-1DV5Zb5vPltoYSWgyHAB6J2BWhk', '2026-06-27 14:01:55.444408+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('6ko39a26a9qqieqibjmyew85frb6d7pk', '.eJxVjMsOwiAQRf-FtSG8KS7d-w1kZgCpGkhKuzL-uzbpQrf3nHNfLMK21riNvMQ5sTOTlp1-RwR65LaTdId265x6W5cZ-a7wgw5-7Sk_L4f7d1Bh1G9tEmlTCnlBVkklsrPGk_aTRUzOAmEQAjAEAxK9U8JMkJwImEHLAoW9PwmoOFM:1wZA3h:vvhGt6cMKaJlBzvLMN8m5NLW2WOTxQJulYR3S0Y4n8U', '2026-06-29 21:51:09.769915+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('aogz7rcvocsu9lnnmzlhfzh4zod3dqil', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wZSg1:ux8v4-NBWls6a81nk1ugZp7lt_cklIcyGChXjmagAKY', '2026-06-30 17:43:57.351736+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('t75d2i77zd5gwqrxdklfwnhv42jyezjd', '.eJxVjDsOwyAQBe9CHSEwP2_K9D4DWmAJTiIsGbuKcvdgyUXSvpl5b-Zx34rfG61-TuzKpGCX3zFgfFI9SHpgvS88LnVb58APhZ-08WlJ9Lqd7t9BwVZ67RKpMdhsDNqYhDFZKoBs0VECDVY4IIdEWuouRhoHFaIeQPUGHAr2-QIPWjgo:1wPwDQ:MQf_b2a4tGs7UYElMrw-VAQXRD6D26b5h423E0tw_AQ', '2026-06-04 11:15:04.885371+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('aaok3fcgp9q84qizezpb8sib9lniuufq', '.eJxVjMsOwiAQRf-FtSEMgSm4dO83kBkeUjWQlHZl_Hdt0oVu7znnvkSgba1hG3kJcxJnAeL0uzHFR247SHdqty5jb-sys9wVedAhrz3l5-Vw_w4qjfqtqWjjJ1Myw-QBk8EYi7KMhlAxeFc8Zc_oLBNEchqVR1sIjNXWJS3eH-h1N64:1wQIlF:k542Rktw3nlV3KI5rWi4dFSk9XvWYW6XwGdkFeNPF-E', '2026-06-05 11:19:29.958771+05:30');
INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('7duls9mc3gkza9ggujsgpytkst9z1uhp', '.eJxVjDsOwyAQBe9CHSHM16RM7zOghV2CkwgkY1dR7h5bcpG0b2bemwXY1hK2TkuYkV2ZY5ffLUJ6Uj0APqDeG0-trssc-aHwk3Y-NaTX7XT_Dgr0std6hERCj8InBdGAMd4rmazyNuZsbUY0hgadrSS0EcnBsEvCeXRZCmKfL-3eOEg:1wQJTb:Cv-7_xFzfqxApJegSyuXBFifltokRQ70t7QM6rfQd_E', '2026-06-05 12:05:19.767794+05:30');


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 16, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: customers_app_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_app_application_id_seq', 32, true);


--
-- Name: customers_app_applicationstatushistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_app_applicationstatushistory_id_seq', 123, true);


--
-- Name: customers_app_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_app_customer_id_seq', 20, true);


--
-- Name: customers_app_grievance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_app_grievance_id_seq', 5, true);


--
-- Name: customers_app_grievancehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_app_grievancehistory_id_seq', 4, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 167, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 28, true);


--
-- PostgreSQL database dump complete
--

\unrestrict x8YEplrzA9FuYEaZSvJk0HMJdUnCgoK7nqKePV92BJKOmEuWY34l7JXstIpbJ8o

