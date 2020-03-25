SELECT t.conf_name,
       t.market,
       CONCAT(t.venue_city, ", ", t.venue_state, ", ", t.venue_country) as school_city,
       UPPER(p.first_name) as first_name,
       UPPER(p.last_name) as last_name,
       p.birthplace_city,
       p.birthplace_state,
       p.birthplace_country,
       SUM(p.field_goals_made) as FGM,
       SUM(p.steals) as Steals,
       SUM(p.three_points_made) as Three_PTM,
       SUM(p.free_throws_made) as FTM,
       SUM(p.blocks) as Blocks,
       SUM(p.offensive_rebounds) as Offensive_Reb,
       SUM(p.assists) as Assists,
       SUM(p.defensive_rebounds) as Defensive_Reb,
       SUM(p.personal_fouls + p.tech_fouls) as Fouls,
       SUM(p.free_throws_att - p.free_throws_made) as FT_Miss,
       SUM(p.field_goals_att - p.field_goals_made) as FG_Miss,
       SUM(p.turnovers) as Turnovers,
       SUM(minutes_int64) as Minutes,
       g.team_games_played_2017,
       COUNTIF(played) as games_played_on_team,
       ROUND(COUNTIF(played) / g.team_games_played_2017, 2) as attendance,
       ROUND(SUM(minutes_int64) / g.team_games_played_2017, 2) as avg_mins_per_game
FROM `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` p
JOIN
  (
  SELECT id, market, conf_name, venue_city, venue_state, venue_country
  FROM `bigquery-public-data.ncaa_basketball.mbb_teams`
  ) as t
    ON t.id=p.team_id
JOIN
  (
  SELECT h_market as team, SUM(games_played) as team_games_played_2017
  FROM
    (
    SELECT h_market, COUNT(*) as games_played
    FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr`
    WHERE season = 2017
    GROUP BY h_market
    UNION ALL
    SELECT a_market, COUNT(*) as games_played
    FROM `bigquery-public-data.ncaa_basketball.mbb_games_sr`
    WHERE season = 2017
    GROUP BY a_market
    )
  GROUP BY team
  ) as g
    ON market=g.team
WHERE birth_place != "" AND season = 2017
GROUP BY t.conf_name, t.market, school_city, first_name, p.last_name,
         p.birthplace_city, p.birthplace_state, p.birthplace_country,
         birth_place, g.team_games_played_2017
HAVING attendance >= .75 AND avg_mins_per_game >= 20
ORDER BY first_name, last_name