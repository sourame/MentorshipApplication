-- The application uses the stored procedure to find all the mentors that matches with the mentee's skill set.
CREATE DEFINER=`admin`@`%` PROCEDURE `get_mentor_match`(IN p_mentee_id INT)
BEGIN

drop table if exists mentor_attributes;
create temporary table mentor_attributes (user_id int, communication_type varchar(50),ethinicity varchar(50),
 pref_starttime varchar(50),pref_endtime varchar(50), skill int, skilltype varchar(50) ); 
insert into mentor_attributes
select  m.user_id as mentor, m.communication_type, m.pref_ethinicity, m.pref_timestart, m.pref_timeend,  ss.skill_id as mentor_skill, st.topic_category as mentor_area
from Mentor m
inner join User u on m.user_id = u.id
left join SkillSet ss on ss.user_id = m.user_id
left join SkillType st on st.id = ss.skill_id;

select  u.id, u.first_name, u.last_name, u.email, u.ethinicity, m.communication_type,
m.pref_ethinicity, m.pref_timestart, m.pref_timeend, u.street1, u.city, u.state from Mentor m
inner join  User u on m.user_id = u.id
inner join
(
	select ma.user_id,
	sum(case
		when ss.skill_id = ma.skill then 15
		when st.topic_category  = ma.skilltype then 5
		else 0
		end) +
	sum(case
		when m.communication_type = ma.communication_type then 10
		when m.pref_timestart = ma.pref_starttime then 5
		when m.pref_timeend = ma.pref_endtime then 5
		else 0 
	end) +
	sum(case when m.pref_ethinicity = ma.ethinicity then 5
		else 0
	end) as points
	from Mentee m
	inner join User u on m.user_id = u.id
	inner join SkillSet ss on ss.user_id = m.user_id
	inner join SkillType st on st.id = ss.skill_id
	cross join mentor_attributes ma	
	  where m.user_id = p_mentee_id  # mentee_id is the input parameter we pass
	group by ma.user_id
) as matching on matching.user_id = m.user_id 
order by points desc;

drop table mentor_attributes;


END