# Storyboard still generation log

- `obs_dome_open` — local API client error before request: `Images.edit() got an unexpected keyword argument 'output_format'`; retrying without that optional field.
- `obs_console_macro` — local API client error before request: `Images.edit() got an unexpected keyword argument 'output_format'`; retrying without that optional field.
- `astronomer_desk_sync` — local API client error before request: `Images.edit() got an unexpected keyword argument 'output_format'`; retrying without that optional field.
- `canal_map_macro` — local API client error before request: `Images.edit() got an unexpected keyword argument 'output_format'`; retrying without that optional field.

## Regeneration pass — 2026-09-04T08:34:49-04:00

- `signal_crossing_space` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`
- `mars_night_wide` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`
- `counterfeit_parade` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`
- `rain_to_canal` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`
- `duet_lamplight_astronomer_sync` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`
- `duet_lamplight_astronaut_sync` — API error: `429 insufficient_quota / credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API.`

## Regeneration retry — 2026-09-04T08:42:54-04:00

- `signal_crossing_space` — API error on initial retry: `429 insufficient_quota / credit_balance_exhausted`; repeated after a short propagation delay and again after one minute with the same result.
- `mars_night_wide` — API error: `429 insufficient_quota / credit_balance_exhausted`.
- `counterfeit_parade` — API error: `429 insufficient_quota / credit_balance_exhausted`.
- Remaining three setup calls were not redundantly resubmitted after the delayed probes confirmed the project-scoped API key still had no visible credits.

## Successful regeneration pass — 2026-09-04T09:01:13-04:00

- `duet_lamplight_astronomer_sync` — both initial regenerated variants used the astronaut twin's loose bob instead of the astronomer's pinned French twist. The one permitted guard retry was run with an explicit hairstyle correction. The replacement pair has the pinned hairstyle, but the pencil through the twist is not clearly visible in either variant; retained as an unresolved minor continuity miss for owner review.
