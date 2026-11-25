# HighFlow Open Source Toolkit

An early-stage open-source toolkit for small businesses that need practical, affordable lead management and marketing automation.

## Current release: 0.1.0

The initial tool is a local Python utility that validates lead records, assigns a transparent priority score, and exports a prioritized CSV follow-up queue. It requires no API keys, paid services, or external dependencies. It does not send messages automatically.

## Quick start

Requires Python 3.10 or newer.

```sh
python lead_triage.py examples/leads.csv prioritized.csv
python -m unittest discover -s tests
```

Input columns: `lead_id`, `service`, `consent`, `urgency`, `service_area`. Consent and service area must be `yes` or `no`; urgency must be `low`, `normal`, or `high`. The output adds `score` and `next_action`. Records without contact consent are excluded from outreach, and out-of-area requests are marked for review. Scores are operational prioritization signals, not predictions of customer value.

## Privacy

Run locally with synthetic or authorized data. Do not upload real customer records, contact details, or credentials to public repositories. Obtain appropriate consent before contacting leads. Review output manually.

## Roadmap

- Configurable service-area and priority rules.
- Reusable follow-up templates and opt-in workflow integrations.
- Optional AI-assisted drafting with human review.
- Documentation and tests for additional small-business workflows.

These are planned features, not current capabilities. The project is newly established; adoption and community impact have not yet been measured.

## Contributing

Issues, documentation improvements, tests and pull requests are welcome. Please use synthetic data in examples and bug reports.

## License

MIT. See `LICENSE`.
