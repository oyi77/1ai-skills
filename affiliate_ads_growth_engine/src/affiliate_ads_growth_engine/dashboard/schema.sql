CREATE TABLE workspaces (
 id serial primary key,
 slug text unique not null,
 name text not null,
 config jsonb not null,
 created_at timestamp default now()
);

CREATE TABLE facebook_ads_insights (
 id serial primary key,
 workspace_id int references workspaces(id),
 ad_id text,
 date date,
 spend numeric,
 impressions int,
 clicks int,
 actions jsonb,
 created_at timestamp default now()
);

CREATE TABLE shopee_affiliate_orders (
 id serial primary key,
 workspace_id int references workspaces(id),
 order_id text,
 product_id text,
 commission numeric,
 status text,
 order_time timestamp,
 created_at timestamp default now()
);
