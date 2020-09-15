createdb webscraping

\c webscraping;

create table books (
    id serial primary key,
    name text,
    date text,
    amazon decimal,
    book_depository decimal
);

create table gpus (
    id serial primary key,
    name text,
    date text,
    amazon decimal,
    msy decimal
);
