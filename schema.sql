--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5
-- Dumped by pg_dump version 13.3

-- Started on 2021-11-21 19:34:26 AEDT

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
-- TOC entry 244 (class 1259 OID 26327)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO justinandronicos;

--
-- TOC entry 219 (class 1259 OID 25924)
-- Name: brand_url_dict; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.brand_url_dict (
    id integer NOT NULL,
    website character varying(30),
    data json
);


ALTER TABLE public.brand_url_dict OWNER TO justinandronicos;

--
-- TOC entry 218 (class 1259 OID 25922)
-- Name: brand_url_dict_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.brand_url_dict_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.brand_url_dict_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 218
-- Name: brand_url_dict_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.brand_url_dict_id_seq OWNED BY public.brand_url_dict.id;


--
-- TOC entry 239 (class 1259 OID 26076)
-- Name: ff_best_selling; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_best_selling (
    id integer NOT NULL,
    product_id integer,
    category character varying(50),
    ranking integer,
    time_stamp timestamp without time zone
);


ALTER TABLE public.ff_best_selling OWNER TO justinandronicos;

--
-- TOC entry 238 (class 1259 OID 26074)
-- Name: ff_best_selling_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_best_selling_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_best_selling_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3509 (class 0 OID 0)
-- Dependencies: 238
-- Name: ff_best_selling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_best_selling_id_seq OWNED BY public.ff_best_selling.id;


--
-- TOC entry 203 (class 1259 OID 25847)
-- Name: ff_brand; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_brand (
    id integer NOT NULL,
    name character varying(50),
    url character varying(150),
    wm_id integer,
    nl_id integer,
    gm_id integer
);


ALTER TABLE public.ff_brand OWNER TO justinandronicos;

--
-- TOC entry 202 (class 1259 OID 25845)
-- Name: ff_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_brand_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3510 (class 0 OID 0)
-- Dependencies: 202
-- Name: ff_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_brand_id_seq OWNED BY public.ff_brand.id;


--
-- TOC entry 223 (class 1259 OID 25951)
-- Name: ff_current_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_current_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.ff_current_price OWNER TO justinandronicos;

--
-- TOC entry 222 (class 1259 OID 25949)
-- Name: ff_current_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_current_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_current_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3511 (class 0 OID 0)
-- Dependencies: 222
-- Name: ff_current_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_current_price_id_seq OWNED BY public.ff_current_price.id;


--
-- TOC entry 243 (class 1259 OID 26102)
-- Name: ff_highest_rated; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_highest_rated (
    id integer NOT NULL,
    product_id integer,
    category character varying(50),
    ranking integer,
    time_stamp timestamp without time zone,
    rating double precision,
    review_count integer
);


ALTER TABLE public.ff_highest_rated OWNER TO justinandronicos;

--
-- TOC entry 242 (class 1259 OID 26100)
-- Name: ff_highest_rated_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_highest_rated_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_highest_rated_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 242
-- Name: ff_highest_rated_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_highest_rated_id_seq OWNED BY public.ff_highest_rated.id;


--
-- TOC entry 231 (class 1259 OID 26015)
-- Name: ff_historical_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_historical_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.ff_historical_price OWNER TO justinandronicos;

--
-- TOC entry 230 (class 1259 OID 26013)
-- Name: ff_historical_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_historical_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_historical_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 230
-- Name: ff_historical_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_historical_price_id_seq OWNED BY public.ff_historical_price.id;


--
-- TOC entry 211 (class 1259 OID 25881)
-- Name: ff_product; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.ff_product (
    id integer NOT NULL,
    code character varying(30),
    name character varying(150),
    brand_id integer,
    variant character varying(60),
    url character varying(200),
    nl_id integer,
    wm_id integer,
    gm_id integer
);


ALTER TABLE public.ff_product OWNER TO justinandronicos;

--
-- TOC entry 210 (class 1259 OID 25879)
-- Name: ff_product_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.ff_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ff_product_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 210
-- Name: ff_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.ff_product_id_seq OWNED BY public.ff_product.id;


--
-- TOC entry 205 (class 1259 OID 25855)
-- Name: gm_brand; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.gm_brand (
    id integer NOT NULL,
    name character varying(60),
    url character varying(150),
    nl_id integer,
    ff_id integer,
    wm_id integer
);


ALTER TABLE public.gm_brand OWNER TO justinandronicos;

--
-- TOC entry 204 (class 1259 OID 25853)
-- Name: gm_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.gm_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gm_brand_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 204
-- Name: gm_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.gm_brand_id_seq OWNED BY public.gm_brand.id;


--
-- TOC entry 225 (class 1259 OID 25967)
-- Name: gm_current_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.gm_current_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.gm_current_price OWNER TO justinandronicos;

--
-- TOC entry 224 (class 1259 OID 25965)
-- Name: gm_current_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.gm_current_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gm_current_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3516 (class 0 OID 0)
-- Dependencies: 224
-- Name: gm_current_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.gm_current_price_id_seq OWNED BY public.gm_current_price.id;


--
-- TOC entry 233 (class 1259 OID 26031)
-- Name: gm_historical_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.gm_historical_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.gm_historical_price OWNER TO justinandronicos;

--
-- TOC entry 232 (class 1259 OID 26029)
-- Name: gm_historical_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.gm_historical_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gm_historical_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 232
-- Name: gm_historical_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.gm_historical_price_id_seq OWNED BY public.gm_historical_price.id;


--
-- TOC entry 213 (class 1259 OID 25891)
-- Name: gm_product; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.gm_product (
    id integer NOT NULL,
    code character varying(30),
    name character varying(150),
    brand_id integer,
    variant character varying(60),
    url character varying(200),
    nl_id integer,
    ff_id integer,
    wm_id integer
);


ALTER TABLE public.gm_product OWNER TO justinandronicos;

--
-- TOC entry 212 (class 1259 OID 25889)
-- Name: gm_product_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.gm_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gm_product_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 212
-- Name: gm_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.gm_product_id_seq OWNED BY public.gm_product.id;


--
-- TOC entry 237 (class 1259 OID 26063)
-- Name: nl_best_selling; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_best_selling (
    id integer NOT NULL,
    product_id integer,
    category character varying(50),
    ranking integer,
    time_stamp timestamp without time zone
);


ALTER TABLE public.nl_best_selling OWNER TO justinandronicos;

--
-- TOC entry 236 (class 1259 OID 26061)
-- Name: nl_best_selling_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_best_selling_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_best_selling_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3519 (class 0 OID 0)
-- Dependencies: 236
-- Name: nl_best_selling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_best_selling_id_seq OWNED BY public.nl_best_selling.id;


--
-- TOC entry 201 (class 1259 OID 25839)
-- Name: nl_brand; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_brand (
    id integer NOT NULL,
    name character varying(50),
    url character varying(150),
    wm_id integer,
    ff_id integer,
    gm_id integer
);


ALTER TABLE public.nl_brand OWNER TO justinandronicos;

--
-- TOC entry 200 (class 1259 OID 25837)
-- Name: nl_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_brand_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3520 (class 0 OID 0)
-- Dependencies: 200
-- Name: nl_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_brand_id_seq OWNED BY public.nl_brand.id;


--
-- TOC entry 221 (class 1259 OID 25935)
-- Name: nl_current_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_current_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.nl_current_price OWNER TO justinandronicos;

--
-- TOC entry 220 (class 1259 OID 25933)
-- Name: nl_current_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_current_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_current_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3521 (class 0 OID 0)
-- Dependencies: 220
-- Name: nl_current_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_current_price_id_seq OWNED BY public.nl_current_price.id;


--
-- TOC entry 241 (class 1259 OID 26089)
-- Name: nl_highest_rated; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_highest_rated (
    id integer NOT NULL,
    product_id integer,
    category character varying(50),
    ranking integer,
    time_stamp timestamp without time zone,
    rating double precision,
    review_count integer
);


ALTER TABLE public.nl_highest_rated OWNER TO justinandronicos;

--
-- TOC entry 240 (class 1259 OID 26087)
-- Name: nl_highest_rated_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_highest_rated_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_highest_rated_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3522 (class 0 OID 0)
-- Dependencies: 240
-- Name: nl_highest_rated_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_highest_rated_id_seq OWNED BY public.nl_highest_rated.id;


--
-- TOC entry 229 (class 1259 OID 25999)
-- Name: nl_historical_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_historical_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.nl_historical_price OWNER TO justinandronicos;

--
-- TOC entry 228 (class 1259 OID 25997)
-- Name: nl_historical_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_historical_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_historical_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3523 (class 0 OID 0)
-- Dependencies: 228
-- Name: nl_historical_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_historical_price_id_seq OWNED BY public.nl_historical_price.id;


--
-- TOC entry 209 (class 1259 OID 25871)
-- Name: nl_product; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.nl_product (
    id integer NOT NULL,
    code character varying(30),
    name character varying(150),
    brand_id integer,
    variant character varying(60),
    url character varying(200),
    ff_id integer,
    wm_id integer,
    gm_id integer
);


ALTER TABLE public.nl_product OWNER TO justinandronicos;

--
-- TOC entry 208 (class 1259 OID 25869)
-- Name: nl_product_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.nl_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nl_product_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3524 (class 0 OID 0)
-- Dependencies: 208
-- Name: nl_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.nl_product_id_seq OWNED BY public.nl_product.id;


--
-- TOC entry 207 (class 1259 OID 25863)
-- Name: wm_brand; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.wm_brand (
    id integer NOT NULL,
    name character varying(60),
    url character varying(150),
    nl_id integer,
    ff_id integer,
    gm_id integer
);


ALTER TABLE public.wm_brand OWNER TO justinandronicos;

--
-- TOC entry 206 (class 1259 OID 25861)
-- Name: wm_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.wm_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wm_brand_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3525 (class 0 OID 0)
-- Dependencies: 206
-- Name: wm_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.wm_brand_id_seq OWNED BY public.wm_brand.id;


--
-- TOC entry 227 (class 1259 OID 25983)
-- Name: wm_current_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.wm_current_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.wm_current_price OWNER TO justinandronicos;

--
-- TOC entry 226 (class 1259 OID 25981)
-- Name: wm_current_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.wm_current_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wm_current_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3526 (class 0 OID 0)
-- Dependencies: 226
-- Name: wm_current_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.wm_current_price_id_seq OWNED BY public.wm_current_price.id;


--
-- TOC entry 235 (class 1259 OID 26047)
-- Name: wm_historical_price; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.wm_historical_price (
    id integer NOT NULL,
    product_id integer,
    time_stamp timestamp without time zone,
    retail_price numeric,
    on_sale boolean,
    current_price numeric,
    in_stock boolean
);


ALTER TABLE public.wm_historical_price OWNER TO justinandronicos;

--
-- TOC entry 234 (class 1259 OID 26045)
-- Name: wm_historical_price_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.wm_historical_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wm_historical_price_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3527 (class 0 OID 0)
-- Dependencies: 234
-- Name: wm_historical_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.wm_historical_price_id_seq OWNED BY public.wm_historical_price.id;


--
-- TOC entry 217 (class 1259 OID 25911)
-- Name: wm_price_file_info; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.wm_price_file_info (
    id integer NOT NULL,
    hash bytea,
    total_products integer,
    time_stamp timestamp without time zone
);


ALTER TABLE public.wm_price_file_info OWNER TO justinandronicos;

--
-- TOC entry 216 (class 1259 OID 25909)
-- Name: wm_price_file_info_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.wm_price_file_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wm_price_file_info_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3528 (class 0 OID 0)
-- Dependencies: 216
-- Name: wm_price_file_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.wm_price_file_info_id_seq OWNED BY public.wm_price_file_info.id;


--
-- TOC entry 215 (class 1259 OID 25901)
-- Name: wm_product; Type: TABLE; Schema: public; Owner: justinandronicos
--

CREATE TABLE public.wm_product (
    id integer NOT NULL,
    code character varying(30),
    name character varying(150),
    brand_id integer,
    variant character varying(50),
    url character varying(200),
    nl_id integer,
    ff_id integer,
    gm_id integer
);


ALTER TABLE public.wm_product OWNER TO justinandronicos;

--
-- TOC entry 214 (class 1259 OID 25899)
-- Name: wm_product_id_seq; Type: SEQUENCE; Schema: public; Owner: justinandronicos
--

CREATE SEQUENCE public.wm_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wm_product_id_seq OWNER TO justinandronicos;

--
-- TOC entry 3529 (class 0 OID 0)
-- Dependencies: 214
-- Name: wm_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: justinandronicos
--

ALTER SEQUENCE public.wm_product_id_seq OWNED BY public.wm_product.id;


--
-- TOC entry 3264 (class 2604 OID 25927)
-- Name: brand_url_dict id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.brand_url_dict ALTER COLUMN id SET DEFAULT nextval('public.brand_url_dict_id_seq'::regclass);


--
-- TOC entry 3274 (class 2604 OID 26079)
-- Name: ff_best_selling id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_best_selling ALTER COLUMN id SET DEFAULT nextval('public.ff_best_selling_id_seq'::regclass);


--
-- TOC entry 3256 (class 2604 OID 25850)
-- Name: ff_brand id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_brand ALTER COLUMN id SET DEFAULT nextval('public.ff_brand_id_seq'::regclass);


--
-- TOC entry 3266 (class 2604 OID 25954)
-- Name: ff_current_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_current_price ALTER COLUMN id SET DEFAULT nextval('public.ff_current_price_id_seq'::regclass);


--
-- TOC entry 3276 (class 2604 OID 26105)
-- Name: ff_highest_rated id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_highest_rated ALTER COLUMN id SET DEFAULT nextval('public.ff_highest_rated_id_seq'::regclass);


--
-- TOC entry 3270 (class 2604 OID 26018)
-- Name: ff_historical_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_historical_price ALTER COLUMN id SET DEFAULT nextval('public.ff_historical_price_id_seq'::regclass);


--
-- TOC entry 3260 (class 2604 OID 25884)
-- Name: ff_product id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product ALTER COLUMN id SET DEFAULT nextval('public.ff_product_id_seq'::regclass);


--
-- TOC entry 3257 (class 2604 OID 25858)
-- Name: gm_brand id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_brand ALTER COLUMN id SET DEFAULT nextval('public.gm_brand_id_seq'::regclass);


--
-- TOC entry 3267 (class 2604 OID 25970)
-- Name: gm_current_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_current_price ALTER COLUMN id SET DEFAULT nextval('public.gm_current_price_id_seq'::regclass);


--
-- TOC entry 3271 (class 2604 OID 26034)
-- Name: gm_historical_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_historical_price ALTER COLUMN id SET DEFAULT nextval('public.gm_historical_price_id_seq'::regclass);


--
-- TOC entry 3261 (class 2604 OID 25894)
-- Name: gm_product id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product ALTER COLUMN id SET DEFAULT nextval('public.gm_product_id_seq'::regclass);


--
-- TOC entry 3273 (class 2604 OID 26066)
-- Name: nl_best_selling id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_best_selling ALTER COLUMN id SET DEFAULT nextval('public.nl_best_selling_id_seq'::regclass);


--
-- TOC entry 3255 (class 2604 OID 25842)
-- Name: nl_brand id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_brand ALTER COLUMN id SET DEFAULT nextval('public.nl_brand_id_seq'::regclass);


--
-- TOC entry 3265 (class 2604 OID 25938)
-- Name: nl_current_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_current_price ALTER COLUMN id SET DEFAULT nextval('public.nl_current_price_id_seq'::regclass);


--
-- TOC entry 3275 (class 2604 OID 26092)
-- Name: nl_highest_rated id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_highest_rated ALTER COLUMN id SET DEFAULT nextval('public.nl_highest_rated_id_seq'::regclass);


--
-- TOC entry 3269 (class 2604 OID 26002)
-- Name: nl_historical_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_historical_price ALTER COLUMN id SET DEFAULT nextval('public.nl_historical_price_id_seq'::regclass);


--
-- TOC entry 3259 (class 2604 OID 25874)
-- Name: nl_product id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product ALTER COLUMN id SET DEFAULT nextval('public.nl_product_id_seq'::regclass);


--
-- TOC entry 3258 (class 2604 OID 25866)
-- Name: wm_brand id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_brand ALTER COLUMN id SET DEFAULT nextval('public.wm_brand_id_seq'::regclass);


--
-- TOC entry 3268 (class 2604 OID 25986)
-- Name: wm_current_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_current_price ALTER COLUMN id SET DEFAULT nextval('public.wm_current_price_id_seq'::regclass);


--
-- TOC entry 3272 (class 2604 OID 26050)
-- Name: wm_historical_price id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_historical_price ALTER COLUMN id SET DEFAULT nextval('public.wm_historical_price_id_seq'::regclass);


--
-- TOC entry 3263 (class 2604 OID 25914)
-- Name: wm_price_file_info id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_price_file_info ALTER COLUMN id SET DEFAULT nextval('public.wm_price_file_info_id_seq'::regclass);


--
-- TOC entry 3262 (class 2604 OID 25904)
-- Name: wm_product id; Type: DEFAULT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product ALTER COLUMN id SET DEFAULT nextval('public.wm_product_id_seq'::regclass);


--
-- TOC entry 3332 (class 2606 OID 26331)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3306 (class 2606 OID 25932)
-- Name: brand_url_dict brand_url_dict_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.brand_url_dict
    ADD CONSTRAINT brand_url_dict_pkey PRIMARY KEY (id);


--
-- TOC entry 3326 (class 2606 OID 26081)
-- Name: ff_best_selling ff_best_selling_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_best_selling
    ADD CONSTRAINT ff_best_selling_pkey PRIMARY KEY (id);


--
-- TOC entry 3280 (class 2606 OID 25852)
-- Name: ff_brand ff_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_brand
    ADD CONSTRAINT ff_brand_pkey PRIMARY KEY (id);


--
-- TOC entry 3310 (class 2606 OID 25959)
-- Name: ff_current_price ff_current_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_current_price
    ADD CONSTRAINT ff_current_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3330 (class 2606 OID 26107)
-- Name: ff_highest_rated ff_highest_rated_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_highest_rated
    ADD CONSTRAINT ff_highest_rated_pkey PRIMARY KEY (id);


--
-- TOC entry 3318 (class 2606 OID 26023)
-- Name: ff_historical_price ff_historical_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_historical_price
    ADD CONSTRAINT ff_historical_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3290 (class 2606 OID 25888)
-- Name: ff_product ff_product_code_key; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_code_key UNIQUE (code);


--
-- TOC entry 3292 (class 2606 OID 25886)
-- Name: ff_product ff_product_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_pkey PRIMARY KEY (id);


--
-- TOC entry 3282 (class 2606 OID 25860)
-- Name: gm_brand gm_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_brand
    ADD CONSTRAINT gm_brand_pkey PRIMARY KEY (id);


--
-- TOC entry 3312 (class 2606 OID 25975)
-- Name: gm_current_price gm_current_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_current_price
    ADD CONSTRAINT gm_current_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3320 (class 2606 OID 26039)
-- Name: gm_historical_price gm_historical_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_historical_price
    ADD CONSTRAINT gm_historical_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3294 (class 2606 OID 25898)
-- Name: gm_product gm_product_code_key; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_code_key UNIQUE (code);


--
-- TOC entry 3296 (class 2606 OID 25896)
-- Name: gm_product gm_product_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_pkey PRIMARY KEY (id);


--
-- TOC entry 3324 (class 2606 OID 26068)
-- Name: nl_best_selling nl_best_selling_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_best_selling
    ADD CONSTRAINT nl_best_selling_pkey PRIMARY KEY (id);


--
-- TOC entry 3278 (class 2606 OID 25844)
-- Name: nl_brand nl_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_brand
    ADD CONSTRAINT nl_brand_pkey PRIMARY KEY (id);


--
-- TOC entry 3308 (class 2606 OID 25943)
-- Name: nl_current_price nl_current_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_current_price
    ADD CONSTRAINT nl_current_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3328 (class 2606 OID 26094)
-- Name: nl_highest_rated nl_highest_rated_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_highest_rated
    ADD CONSTRAINT nl_highest_rated_pkey PRIMARY KEY (id);


--
-- TOC entry 3316 (class 2606 OID 26007)
-- Name: nl_historical_price nl_historical_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_historical_price
    ADD CONSTRAINT nl_historical_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2606 OID 25878)
-- Name: nl_product nl_product_code_key; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_code_key UNIQUE (code);


--
-- TOC entry 3288 (class 2606 OID 25876)
-- Name: nl_product nl_product_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_pkey PRIMARY KEY (id);


--
-- TOC entry 3284 (class 2606 OID 25868)
-- Name: wm_brand wm_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_brand
    ADD CONSTRAINT wm_brand_pkey PRIMARY KEY (id);


--
-- TOC entry 3314 (class 2606 OID 25991)
-- Name: wm_current_price wm_current_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_current_price
    ADD CONSTRAINT wm_current_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3322 (class 2606 OID 26055)
-- Name: wm_historical_price wm_historical_price_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_historical_price
    ADD CONSTRAINT wm_historical_price_pkey PRIMARY KEY (id);


--
-- TOC entry 3302 (class 2606 OID 25921)
-- Name: wm_price_file_info wm_price_file_info_hash_key; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_price_file_info
    ADD CONSTRAINT wm_price_file_info_hash_key UNIQUE (hash);


--
-- TOC entry 3304 (class 2606 OID 25919)
-- Name: wm_price_file_info wm_price_file_info_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_price_file_info
    ADD CONSTRAINT wm_price_file_info_pkey PRIMARY KEY (id);


--
-- TOC entry 3298 (class 2606 OID 25908)
-- Name: wm_product wm_product_code_key; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_code_key UNIQUE (code);


--
-- TOC entry 3300 (class 2606 OID 25906)
-- Name: wm_product wm_product_pkey; Type: CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_pkey PRIMARY KEY (id);


--
-- TOC entry 3370 (class 2606 OID 26082)
-- Name: ff_best_selling ff_best_selling_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_best_selling
    ADD CONSTRAINT ff_best_selling_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3336 (class 2606 OID 26168)
-- Name: ff_brand ff_brand_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_brand
    ADD CONSTRAINT ff_brand_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_brand(id);


--
-- TOC entry 3337 (class 2606 OID 26238)
-- Name: ff_brand ff_brand_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_brand
    ADD CONSTRAINT ff_brand_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_brand(id);


--
-- TOC entry 3338 (class 2606 OID 26243)
-- Name: ff_brand ff_brand_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_brand
    ADD CONSTRAINT ff_brand_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_brand(id);


--
-- TOC entry 3362 (class 2606 OID 25960)
-- Name: ff_current_price ff_current_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_current_price
    ADD CONSTRAINT ff_current_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3372 (class 2606 OID 26108)
-- Name: ff_highest_rated ff_highest_rated_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_highest_rated
    ADD CONSTRAINT ff_highest_rated_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3366 (class 2606 OID 26024)
-- Name: ff_historical_price ff_historical_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_historical_price
    ADD CONSTRAINT ff_historical_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3350 (class 2606 OID 26163)
-- Name: ff_product ff_product_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.ff_brand(id);


--
-- TOC entry 3352 (class 2606 OID 26198)
-- Name: ff_product ff_product_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_product(id);


--
-- TOC entry 3351 (class 2606 OID 26188)
-- Name: ff_product ff_product_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3349 (class 2606 OID 26118)
-- Name: ff_product ff_product_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.ff_product
    ADD CONSTRAINT ff_product_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_product(id);


--
-- TOC entry 3339 (class 2606 OID 26123)
-- Name: gm_brand gm_brand_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_brand
    ADD CONSTRAINT gm_brand_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_brand(id);


--
-- TOC entry 3340 (class 2606 OID 26138)
-- Name: gm_brand gm_brand_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_brand
    ADD CONSTRAINT gm_brand_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_brand(id);


--
-- TOC entry 3341 (class 2606 OID 26143)
-- Name: gm_brand gm_brand_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_brand
    ADD CONSTRAINT gm_brand_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_brand(id);


--
-- TOC entry 3363 (class 2606 OID 25976)
-- Name: gm_current_price gm_current_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_current_price
    ADD CONSTRAINT gm_current_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.gm_product(id);


--
-- TOC entry 3367 (class 2606 OID 26040)
-- Name: gm_historical_price gm_historical_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_historical_price
    ADD CONSTRAINT gm_historical_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.gm_product(id);


--
-- TOC entry 3355 (class 2606 OID 26233)
-- Name: gm_product gm_product_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.gm_brand(id);


--
-- TOC entry 3356 (class 2606 OID 26248)
-- Name: gm_product gm_product_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3354 (class 2606 OID 26228)
-- Name: gm_product gm_product_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3353 (class 2606 OID 26128)
-- Name: gm_product gm_product_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.gm_product
    ADD CONSTRAINT gm_product_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_product(id);


--
-- TOC entry 3369 (class 2606 OID 26069)
-- Name: nl_best_selling nl_best_selling_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_best_selling
    ADD CONSTRAINT nl_best_selling_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3335 (class 2606 OID 26208)
-- Name: nl_brand nl_brand_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_brand
    ADD CONSTRAINT nl_brand_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_brand(id);


--
-- TOC entry 3333 (class 2606 OID 26148)
-- Name: nl_brand nl_brand_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_brand
    ADD CONSTRAINT nl_brand_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_brand(id);


--
-- TOC entry 3334 (class 2606 OID 26153)
-- Name: nl_brand nl_brand_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_brand
    ADD CONSTRAINT nl_brand_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_brand(id);


--
-- TOC entry 3361 (class 2606 OID 25944)
-- Name: nl_current_price nl_current_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_current_price
    ADD CONSTRAINT nl_current_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3371 (class 2606 OID 26095)
-- Name: nl_highest_rated nl_highest_rated_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_highest_rated
    ADD CONSTRAINT nl_highest_rated_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3365 (class 2606 OID 26008)
-- Name: nl_historical_price nl_historical_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_historical_price
    ADD CONSTRAINT nl_historical_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.nl_product(id);


--
-- TOC entry 3348 (class 2606 OID 26223)
-- Name: nl_product nl_product_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.nl_brand(id);


--
-- TOC entry 3347 (class 2606 OID 26203)
-- Name: nl_product nl_product_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3346 (class 2606 OID 26133)
-- Name: nl_product nl_product_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_product(id);


--
-- TOC entry 3345 (class 2606 OID 26113)
-- Name: nl_product nl_product_wm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.nl_product
    ADD CONSTRAINT nl_product_wm_id_fkey FOREIGN KEY (wm_id) REFERENCES public.wm_product(id);


--
-- TOC entry 3343 (class 2606 OID 26178)
-- Name: wm_brand wm_brand_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_brand
    ADD CONSTRAINT wm_brand_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_brand(id);


--
-- TOC entry 3344 (class 2606 OID 26218)
-- Name: wm_brand wm_brand_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_brand
    ADD CONSTRAINT wm_brand_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_brand(id);


--
-- TOC entry 3342 (class 2606 OID 26173)
-- Name: wm_brand wm_brand_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_brand
    ADD CONSTRAINT wm_brand_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_brand(id);


--
-- TOC entry 3364 (class 2606 OID 25992)
-- Name: wm_current_price wm_current_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_current_price
    ADD CONSTRAINT wm_current_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.wm_product(id);


--
-- TOC entry 3368 (class 2606 OID 26056)
-- Name: wm_historical_price wm_historical_price_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_historical_price
    ADD CONSTRAINT wm_historical_price_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.wm_product(id);


--
-- TOC entry 3358 (class 2606 OID 26183)
-- Name: wm_product wm_product_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.wm_brand(id);


--
-- TOC entry 3359 (class 2606 OID 26193)
-- Name: wm_product wm_product_ff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_ff_id_fkey FOREIGN KEY (ff_id) REFERENCES public.ff_product(id);


--
-- TOC entry 3360 (class 2606 OID 26213)
-- Name: wm_product wm_product_gm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_gm_id_fkey FOREIGN KEY (gm_id) REFERENCES public.gm_product(id);


--
-- TOC entry 3357 (class 2606 OID 26158)
-- Name: wm_product wm_product_nl_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: justinandronicos
--

ALTER TABLE ONLY public.wm_product
    ADD CONSTRAINT wm_product_nl_id_fkey FOREIGN KEY (nl_id) REFERENCES public.nl_product(id);


-- Completed on 2021-11-21 19:34:27 AEDT

--
-- PostgreSQL database dump complete
--

