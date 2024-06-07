from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT
  date,
  repo.name AS repo_name,
  scorecard,
  check.name AS check_name,
  check.score AS check_score,
  check.reason AS check_reason
FROM
  `openssf.scorecardcron.scorecard-v2`,
  UNNEST(checks) AS check
WHERE
  repo.name = "github.com/pallets/flask"

  LIMIT 100
"""
# AND scorecard.version = "v4.13.1-242-g153e06d9"

query_job = client.query(query)

results = query_job.result()

for row in results:
    print("date:", row.date)
    print("repo_name:", row.repo_name)
    print("scorecard:", row.scorecard)
    print("check_name:", row.check_name)
    print("check_score:", row.check_score)
    print("check_reason:", row.check_reason)