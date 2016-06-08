drop table if exists messages;
create table messages (
    count_ integer not null,    
    message_no integer primary key,
    weekday integer not null,
    sent_date text not null  
);

drop table if exists notices;
create table notices (
    index_ integer not null,
    url text not null,
    notice_id integer primary key,
    message_no integer not null,
    title text not null  
);

drop table if exists events;
create table events (
    datetime text not null,
    ip text not null,
    user_agent text not null,
    cookie text,
    notice_id integer not null,
    referer text,
    url text not null
);
