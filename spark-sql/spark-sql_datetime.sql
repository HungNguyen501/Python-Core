select date_format(current_date, 'yyyyMMdd');
===> 20210911

select to_date(CAST(20210911 AS STRING), 'yyyyMMdd');
===> convert to date: 2021-09-11

select DATE_FORMAT(add_months(trunc(CURRENT_DATE, 'MM'), -3),'yyyyMMdd');
===> subtract 3 months: 20210601

select DATE_FORMAT(date_add(current_DAte, -3), 'yyyyMMdd');
===>subtract 3 days: 20210908

select DATE_FORMAT(trunc(CURRENT_DATE, 'MM'), 'yyyyMMdd');
===>go to first day of month: 20210901

select DATE_FORMAT(trunc(CURRENT_DATE, 'week'), 'yyyyMMdd');
===>go to first day of week: 20210906

select DATE_FORMAT(trunc(CURRENT_DATE, 'year'), 'yyyyMMdd');
===>go to first day of week: 20210906

select date_format(current_date, 'yyyyMMdd');
===> convert date: 20210911