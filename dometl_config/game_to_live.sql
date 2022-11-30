to_timestamp(game_time, 'YYYY-MM-DD HH24:MI:SS')

--SELECT COUNT(*) FROM st_game

--DELETE FROM st_game;

SELECT *
FROM st_game
WHERE
	to_timestamp(game_time, 'YYYY-MM-DD HH24:MI:SS') >= '2021-10-01' AND
	(
		((home_pts::int > away_pts::int) AND (home_fg3::int >= away_fg3::int)) OR
		((away_pts::int > home_pts::int) AND (away_fg3::int >= home_fg3::int))
	)
--ORDER BY to_timestamp(game_time, 'YYYY-MM-DD HH24:MI:SS')

--911.0/1323