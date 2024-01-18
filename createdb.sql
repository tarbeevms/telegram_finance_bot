create table budget(
    user_id integer primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    user_id integer,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукты", true, "еда"),
    ("coffee", "кофе", true, ""),
    ("food", "еда", true, "столовая, кафе, ланч, мак, бургер кинг, кфц, додо"),
    ("medicine", "лекарства", true, "лекарство, аптека"),
    ("municipal","коммунальные усл.", true, "коммуналка, дом, электричество, газ, вода"),
    ("taxes","налоги", true, "налоги, налог, штраф"),
    ("transport", "общ. транспорт", true, "метро, автобус, трамвай, элька"),
    ("taxi", "такси", false, "яндекс такси"),
    ("phone", "связь", true, "теле2, телефон, билайн, beeline, tele2"),
    ("books", "книги", false, "литература, литра, лит-ра"),
    ("internet", "интернет", true, "инет"),
    ("subscriptions", "подписки", false, "подписка, яндекс плюс, плюс, иви, вк, телега"),
    ("shops", "онлайн-магазины", false, "озон, ozon, wb, wildberries, вб, вайлдберис"),
    ("other", "прочее", true, "");

--insert into budget(codename, daily_limit) values ('base', 700);
