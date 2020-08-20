SELECT title FROM movies WHERE id IN

(SELECT movie_id FROM stars WHERE person_id IN

(SELECT id FROM people WHERE (name LIKE "Johnny Depp") OR (name LIKE "Helena Bonham Carter"))

GROUP BY movie_id 
HAVING COUNT(movie_id) > 1
)
;

