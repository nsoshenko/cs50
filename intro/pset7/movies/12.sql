SELECT title from movies
WHERE id IN (SELECT movie_id from stars
WHERE person_id = (SELECT id from people
WHERE name = "Johnny Depp"))
AND id IN (SELECT movie_id from stars
WHERE person_id = (SELECT id from people
WHERE name = "Helena Bonham Carter"))