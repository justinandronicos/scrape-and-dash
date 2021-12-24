# Scrape & Dash

An e-commerce data scraping and dashboard app for competitor tracking.

This repository is a mirror of the project's private repository that has been **cleaned of sensitive data** including the **config file** required to run the app. This is kept **in sync** with the private repo via a GitHub Action using [Git Sync](https://github.com/wei/git-sync).

## Contents

- [Scrape & Dash](#scrape--dash)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Features](#features)
    - [**Scraping**](#scraping)
    - [**Dashboard**](#dashboard)
    - [**Product Matching**](#product-matching)
    - [**Database**](#database)
  - [Deployment](#deployment)
  - [Known Issues and Future Optimisations](#known-issues-and-future-optimisations)
  - [Dependencies](#dependencies)
  
## Overview

Scrape & Dash is a Python project that combines 3 distinct components into an automated e-commerce competitor tracking solution. It is comprised of a scraping service using [Scrapy](https://github.com/scrapy/scrapy), a dashboard web app using [Dash](https://github.com/plotly/dash) and [Flask](https://github.com/pallets/flask), and a machine learning-based product matching service using [dedupe](https://github.com/dedupeio/dedupe). These all share the same relational database as loosely coupled microservices for independent resource scaling is not needed for the applied use case.

## Features

### **Scraping**

The scraping service uses a brand spider, a product spider, and a category spider for each competitor website. These run in asynchronous batches (brands > products > categories). Scrapy was chosen due to its event-driven asynchronous architecture that supports concurrency.

A file parsing module is used to process a product pricing file for the base website to enable comparison (separately contained within the web app backend to support file uploads).

- [x] Support for 4 e-commerce retailers
- [x] Brands sold
- [x] Products sold and stock status
- [x] Product pricing
- [x] Best-selling products per category
- [x] Highest-rated products per category

### **Dashboard**

The dashboard web app provides multiple pages for analytics on each website and comparative views. It supports authentication and user creation as well as data extraction via CSV downloads on each page. Dash was chosen due to its abstraction of React components and Plotly.js graphing into a Flask-based web app using reactive and functional Python callbacks.

- [x] Website comparison by brand
- [x] Brand viewer
- [x] Product viewer
- [x] Best-selling products viewer
- [x] Highest-rated products viewer
- [x] Product file upload
- [x] User creation and authentication using Flask-Login
- [ ] Product search
- [ ] Aggregation graphing (e.g. price time-series comparison)

### **Product Matching**

Product matching will be achieved through a process of data cleaning and transformation, and entity resolution using the dedupe machine learning library to link products stored in the database across websites. Dedupe was chosen due to its efficient active learning approach using hierarchical clustering with centroid linkage (based on Mikhail Yuryevich Bilenko's PhD dissertation), and extensibleness.

- [x] Proof of concept test on local data
- [ ] Data cleaning and transformation pipeline
- [ ] Clustering
- [ ] Data fusion (merging matches)
- [ ] Incremental record linkage (new products added)

### **Database**

A PostgreSQL relational database is used due to the inherent data relations between websites (brands, products, prices).

Each website has the following tables:

- Brands
- Products
- Current prices
- Historical prices
- Highest-rated products (if applicable)
- Best-selling products (if applicable)

A *BrandUrlDict* table is used to store a JSON of Brand:URL key-value pairs used by product spiders to store brands.
A *price file info* table is used to store file related information for the base website to only update the tables when the file has been updated.
A *RegisteredUser* table is also used to store created users for authentication purposes.

## Deployment

Scrape & Dash will be deployed onto AWS using scheduled serverless compute (Lambda) for the scraping and product matching services, and an EC2 instance running the containerised dashboard web app. The scraping service can be configured to run daily and the product matching service will then be triggered to run after scraping is finished. All 3 components will be connected to an Amazon RDS instance.

This approach allows 24/7 uptime and responsiveness for the web app while taking advantage of the intermittent running of the scraping and product matching services where cold start times will not be an issue.

## Known Issues and Future Optimisations

- [x] Further reduce requests from spiders to minimise load on websites
- [ ] Convert models schema file and items file to a PyPI package due to shared schema
- [ ] Batch queries for scraper pipelines
- [ ] Database Indexing
- [ ] Typed data classes with Pydantic for scraper Items
- [ ] Improve asynchronous running of spiders
- [ ] Reduce initial database calls in dashboard and implement caching to improve performance as database size scales
- [ ] Add tests & spider contracts


## Dependencies

- [Alembic](https://github.com/sqlalchemy/alembic)
- [Dash](https://github.com/plotly/dash)
- [Dash Bootstrap Components](https://github.com/facultyai/dash-bootstrap-components)
- [Dedupe](https://github.com/dedupeio/dedupe)
- [Flask-Login](https://github.com/maxcountryman/flask-login)
- [NumPy](https://github.com/numpy/numpy)
- [Pandas](https://github.com/pandas-dev/pandas)
- [Psycopg 2](https://github.com/psycopg/psycopg2)
- [PyYAML](https://github.com/yaml/pyyaml)
- [Requests](https://github.com/psf/requests)
- [Scrapy](https://github.com/scrapy/scrapy)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [Werkzeug](https://github.com/pallets/werkzeug)
