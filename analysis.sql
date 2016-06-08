-- select counts to confirm integrity
select count(*) from events;
select count(*) from messages;
select count(*) from notices;

select * from notices where notice_id = 24953;


select * from events where cookie is null limit 100;
-- indicates that there are actual users w/o cookies, not bots/apps (based on browser distribution

select ip, cookie, count(*) as hits
from events
group by ip, cookie
order by hits desc limit 100;

-- top 3:
-- 10.47.69.133
-- 10.47.69.134
-- 10.47.69.137
select distinct(cookie), user_agent from events where ip = '10.47.69.137';
-- these are likely the mobile gateways

-- total counts of hits, by user agent (binned)
select
case
    when user_agent like '%BB10%' then 'BB10'
    when user_agent like '%iPhone%' then 'iPhone'
    when user_agent like '%iPad%' then 'iPad'
    when user_agent like '%Trident%' then 'MSIE'
    when user_agent like '%Chrome%' then 'Chrome'
    when user_agent like '%Macintosh%' then 'Mac'
    when user_agent like '%Firefox%' then 'Firefox'
    when user_agent like '%WorxWeb%' then 'WorxWeb'
    else user_agent
end as agent, count(*) as "count"
from events
group by agent
order by "count" desc;

-- as a follow up, I noticed that the number of hits by search engines (e.g., Autonomy) is pretty low
-- there are 335 notices in this sample set, and only 21 hits by Autonomy:
select * from events where user_agent = 'Autonomy+HTTPFetch';


-- counts by user agent (binned), by time of day
select
case
    when user_agent like '%BB10%' then 'Mobile'
    when user_agent like '%iPhone%' then 'Mobile'
    when user_agent like '%iPad%' then 'Mobile'
    when user_agent like '%Trident%' then 'Desktop'
    when user_agent like '%Chrome%' then 'Desktop'
    -- when user_agent like '%Macintosh%' then 'Mac'
    -- when user_agent like '%Firefox%' then 'Firefox'
    -- when user_agent like '%WorxWeb%' then 'WorxWeb'
    else null -- we don't care about the others
end as agent, strftime('%H', datetime) as hour, count(*) as "count"
from events
where agent is not null
and date(datetime) = '2016-02-02'
group by agent, hour
order by agent, hour;

select strftime('%H', datetime), * from events limit 10;

-- counts per weekday
select weekday, count(*)
from messages
group by weekday;

-- counts of numbers of notices, based on weekday sent
select m.weekday, count(*)
from messages m
join notices n on m.message_no = n.message_no
group by m.weekday;

-- counts of total events, based on weekday sent
select m.weekday, count(*)
from messages m
join notices n on m.message_no = n.message_no
join events e on e.notice_id = n.notice_id
group by m.weekday;

-- click rate of a specific notice
select * from notices limit 25; -- selected 24965, 24968, 24957

select * 
from events
where notice_id = 24968;

select substr(datetime, 1, 10) as date, count(ip)
from events
where notice_id = 24957
group by date; -- as per below, hits on 1/4 are likely from the inet home

-- calendar math uses julianday() function
select julianday('2016-02-01') - julianday('2016-01-31');

-- counts of hits by date, relative to publish (email) date
select e.notice_id, julianday(date(e.datetime)) - julianday(date(m.sent_date)) as day, count(*) as hits
from events e
join notices n on n.notice_id = e.notice_id
join messages m on m.message_no = n.message_no
-- where e.notice_id in (24957, 24965)
group by e.notice_id, day
order by e.notice_id, day; -- as per below, hits on 1/4 are likely from the inet home

-- distribution of hits, to generate mean +/- std_dev
select n.notice_id, date(m.sent_date) as sent, n.title, count(*) as total
from notices n
join events e on n.notice_id = e.notice_id
join messages m on m.message_no = n.message_no
group by n.notice_id, sent, n.title
order by total desc;

-- ordered list of notices, grouped by message
-- allows us to determine the number of hits, relative to the index
select n.message_no, n.notice_id, n.index_, count(*)
from notices n
join events e on n.notice_id = e.notice_id
group by n.message_no, n.notice_id, n.index_, n.title
order by n.message_no, n.notice_id, n.index_ asc;

--ordered list of notices, ranked by total hits
-- need to include date, as the end of the log may have bias (too few)
select date(m.sent_date) as date_, n.notice_id, n.title, count(*) as total_hits
from notices n
join events e on n.notice_id = e.notice_id
join messages m on n.message_no = m.message_no
group by n.notice_id, n.title
order by total_hits desc;

-- pull out time of day
select time(sent_date) from messages limit 10;

--time of day by user string
-- what is the question here?
--Do people read this on their mobile devices on the way to work?


-- users (ip, cookic?) and notices 
-- do some people regularly click on the same types of content?
select count(distinct(ip)) from events;
select count(distinct(cookie)) from events;

select * from notices where title like "%efferson%cience%"; -- id 25186

select cookie, count(datetime)
from events
where notice_id = 25186 
group by cookie;

select e.notice_id, n.title
from events e
join notices n on n.notice_id = e.notice_id
where e.cookie = '_ga=GA1.2.1165502229.1445884751';

--
