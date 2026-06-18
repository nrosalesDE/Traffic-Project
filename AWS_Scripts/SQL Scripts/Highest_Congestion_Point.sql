Select distinct d.point_id, MAX(congestion_ratio) as highest_congestion_ratio, point_type, d.corridor, city, direction
from fact_trafficdata_v2 f
join dim_point d on f.point_id = d.point_id
group by d.point_id, d.point_type, d.corridor, d.city, d.direction
order by highest_congestion_ratio DESC
limit 10;





