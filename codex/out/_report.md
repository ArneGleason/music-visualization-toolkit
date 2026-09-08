# Storyboard still generation report

Date: 2026-09-03

## Summary

- Manifest setups: 41
- Expected final images: 82
- Generated final images: 82
- Skipped setups: 0
- API/content-policy failures: 0
- Guard-driven regenerations: 1 setup (`signal_crossing_space`)
- Unresolved acceptance failures: 1 setup (`signal_crossing_space`)

## Generation settings

- Endpoint: OpenAI Images edit endpoint
- Model: `gpt-image-2`
- Prompt handling: each manifest prompt passed verbatim with prompt augmentation disabled
- Inputs: every reference listed by each manifest entry attached in listed order
- API output: two variants per setup, 1536x1024, high quality
- Final output: centered crop to 1536x864, JPEG quality 92, saved at the exact manifest paths

## Validation

All 82 listed outputs are present, readable JPEG files, and exactly 1536x864 pixels.

Visual review found that both initial `signal_crossing_space` variants contained people despite the explicit no-people guard. The setup was regenerated once, as permitted by the README, using the identical prompt and reference. Both replacement variants still contain people, so the latest files remain at their required output paths and the setup is recorded as an unresolved acceptance failure.

No other setup-level acceptance failure was found in the contact-sheet review and targeted full-resolution checks.

## Spend

The API client did not report actual spend. There were 42 successful two-image edit calls (84 returned images including the required retry). Scaling the README estimate of USD 15–25 for 82 images gives an approximate total of USD 15–26.

## Log

See `_log.md` for the four pre-request local client compatibility errors encountered and recovered from at startup. No API request or content-policy refusal was logged.

---

## Targeted regeneration pass — 2026-09-04

### Summary

- Setups requested: 6
- Expected replacement images: 12
- Successfully regenerated images: 0
- API failures: 6
- Existing A/B images replaced: 0
- Guard retries: 0 (no images were returned to validate)

### Requested setups

- `signal_crossing_space`
- `mars_night_wide`
- `counterfeit_parade`
- `rain_to_canal`
- `duet_lamplight_astronomer_sync`
- `duet_lamplight_astronaut_sync`

### Generation settings

- Endpoint: OpenAI Images edit endpoint
- Model: `gpt-image-2`
- API output requested: two variants per setup, 1536x1024, high quality, JPEG quality 92
- Prompt handling: original setup-specific manifest text preserved; each saved regeneration direction inserted as an explicit overriding revision note immediately before the unchanged shared lock block; prompt augmentation disabled
- Inputs: every manifest reference attached first; for the five setups with retained favorites, the selected prior still was attached last as a loose visual/compositional starting point
- Setup 21 correction: the accidentally duplicated underground-spring direction was replaced in `still_favorites.md` with the intended tourist-shop display-window direction before the request

### Result

All six calls failed with `429 insufficient_quota / credit_balance_exhausted`: the API account associated with `OPENAI_API_KEY` reported no credits remaining. No new images were returned, no old A/B still was overwritten, and all six regeneration flags and existing favorite selections remain intact for a resumable retry after billing is restored.

### Spend

The API did not report usage or actual spend for this failed pass. The preflight estimate was approximately USD 2.50–3.25 for the normal 12-image pass, with up to about USD 5.50 if all six setups required their one permitted guard retry.

### Billing retry — 2026-09-04T08:42:54-04:00

After the owner reported adding credits, the regeneration pass was retried. The first three setup requests immediately returned `429 insufficient_quota / credit_balance_exhausted`. `signal_crossing_space` was then probed twice more after short propagation waits, including a final retry more than one minute later; both probes returned the same result. The active key is project-scoped, and neither `OPENAI_ORG_ID` nor `OPENAI_PROJECT_ID` is set, so it uses the organization/project encoded by that key.

No images were returned or replaced. The six regeneration markers, five retained favorites, and all existing A/B files remain unchanged and ready for another retry once the API balance for this key's project is available. The API did not report usage or spend for these failed requests.

---

## Successful targeted regeneration — 2026-09-04

### Summary

- Setups regenerated: 6
- Replacement images installed: 12
- Successful two-image edit calls: 7 (six requested pairs plus one permitted guard retry)
- API/content-policy failures: 0
- Guard retries: 1 (`duet_lamplight_astronomer_sync`)
- Unresolved acceptance notes: 1 minor continuity detail (`duet_lamplight_astronomer_sync` pencil not clearly visible)

### Installed setups

- `signal_crossing_space`
- `mars_night_wide`
- `counterfeit_parade`
- `rain_to_canal`
- `duet_lamplight_astronomer_sync`
- `duet_lamplight_astronaut_sync`

### Generation settings

- Endpoint: OpenAI Images edit endpoint
- Model: `gpt-image-2`
- API output: two variants per setup, 1536x1024, high quality
- Final output: centered crop to 1536x864, JPEG quality 92, atomically installed at the exact manifest paths
- Prompt handling: original manifest setup text preserved; each saved regeneration direction inserted as an explicit overriding revision note immediately before the unchanged shared lock block; prompt augmentation disabled
- Inputs: every manifest reference attached first; the five retained favorites were attached last as loose visual/compositional starting references

### Validation

All 12 replacement outputs are present, readable JPEG files, and exactly 1536x864 pixels. Visual review confirmed the requested scene changes: probe signal crossing space without people; darker Mars night with one glowing fauna element; tourist-curio storefront replacing the conveyor; underground spring and wet-habitat fauna replacing rain; end-of-day television outro; and darker evening astronaut interior.

The initial `duet_lamplight_astronomer_sync` pair used the astronaut twin's loose bob. Its one allowed retry restored the astronomer's pinned hairstyle, but neither result clearly shows the pencil through the twist. The improved retry pair is installed and the remaining detail is logged for owner review.

The six completed regeneration rows were reset to unreviewed with no pending regeneration flag, leaving `still_favorites.md` at 35/41 reviewed so the owner can make fresh A/B selections in the reviewer.

### Spend

The API client did not report actual spend. Seven high-quality 1536x1024 two-image edit calls were completed; the preflight estimate was approximately USD 2.50–3.25 for the six requested pairs, plus about USD 0.40 and input-image cost for the one guard retry.
