CREATE TABLE scraper_info(
	id SERIAL PRIMARY KEY, 
    last_month_date_url_id varchar(500) NOT NULL    
);

INSERT INTO scraper_info(last_month_date_url_id) values(0);

CREATE TABLE month_date_url(
	id SERIAL PRIMARY KEY, 
    url_month SMALLINT NOT NULL,
    url_date SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    month_date_url varchar(100) NOT NULL,
    data_scraped boolean NOT NULL DEFAULT False    
);


CREATE TABLE news_url(
	id SERIAL PRIMARY KEY, 
    month_date_url_id INTEGER NOT NULL,
    title varchar(1000) NOT NULL,
    url text NOT NULL,
    is_valid boolean NOT NULL DEFAULT False,
    UNIQUE(title)
);


CREATE TABLE classified_article(
	id SERIAL PRIMARY KEY,
    news_url_id INTEGER NOT NULL,     
    article text NOT NULL,
    UNIQUE(news_url_id)
);


CREATE TABLE visit_info(
    id SERIAL PRIMARY KEY,
    place varchar(1000) NOT NULL,
    visit_date date NOT NULL,
    UNIQUE(place,visit_date)
);