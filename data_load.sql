DROP TABLE IF EXISTS employee;
CREATE TABLE employee
  (
     id   BIGSERIAL PRIMARY KEY,
     NAME VARCHAR(50)
  );
DROP TABLE IF EXISTS employee_activity;
CREATE TABLE employee_activity
  (
     id            BIGSERIAL PRIMARY KEY,
     employee_id   BIGINT,
     activity_name VARCHAR(50),
     start_time    TIMESTAMPTZ,
     end_time      TIMESTAMPTZ,
     CONSTRAINT fk_emp_id FOREIGN KEY(employee_id) REFERENCES employee(id)
  ); 

insert into employee(id, name) values(1, 'Joe');
insert into employee(id, name) values (2, 'William');
insert into employee(id, name) values (3, 'Lucy');
  
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (1, 1, 'Picking', '2021-01-24 9:05:00 -08:00', '2021-01-24 9:10:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (2, 1, 'Picking', '2021-01-24 9:15:00 -08:00', '2021-01-24 10:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (3, 2, 'Packing', '2021-01-24 9:15:00 -08:00', '2021-01-24 10:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (4, 1, 'Packing', '2021-01-24 11:00:00 -08:00', '2021-01-24 11:45:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (5, 3, 'Packing', '2021-01-24 11:30:00 -08:00', '2021-01-24 12:20:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (6, 1, 'Picking', '2021-01-24 11:50:00 -08:00', '2021-01-24 12:30:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (7, 2, 'Packing', '2021-01-24 10:30:00 -08:00', '2021-01-24 13:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (8, 3, 'Picking', '2021-01-24 12:25:00 -08:00', '2021-01-24 13:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (9, 3, 'Cleaning', '2021-01-24 13:00:00 -08:00', '2021-01-24 13:05:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (10, 3, 'Picking', '2021-01-24 13:05:00 -08:00', '2021-01-24 14:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (11, 2, 'Packing', '2021-01-24 13:30:00 -08:00', '2021-01-24 15:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (12, 2, 'Picking', '2021-01-24 15:05:00 -08:00', '2021-01-24 17:00:00 -08:00');
INSERT INTO public.employee_activity(id, employee_id, activity_name, start_time, end_time) VALUES (13, 1, 'Cleaning', '2021-01-24 23:55:00 -08:00',	'2021-01-25 12:35:00 -08:00');
