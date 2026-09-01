# Storyboard pass — review notes (2026-09-01)

All 37 setups generated as stills in Flow (Nano Banana 2, 16:9, x2 variants,
0 credits each), one prompt per setup = shot body + lock block, with the
matching Character, board, or canal vista attached. Files land in
`board/frames/<setup>_<variant>.jpg`; `tools/board_contact.py` builds
`board/contact.html` from them. Ids are harvested from the Flow media grid,
resolved to signed CDN URLs (`flow-content.google/image/<id>?Expires…`) via
the `media.getMediaUrlRedirect` endpoint, and pulled with curl; the grid is
virtualized and only loads while the Chrome tab is visible.

## Systematic findings (feed the regen pass and the prompts)

- **Astronaut gets the astronomer's glasses.** Seen in astronaut_close
  (one variant), excavation (one variant), and both lamplight-astronaut
  variants. Twin bleed via the agent's conversation context. Guard: every
  astronaut prompt states "no glasses — only the astronomer wears glasses",
  and hero astronaut stills are generated in a fresh agent session.
- **Day where night was asked** (mars_night_wide, colony_goodnight A,
  drumwall A). The attached daytime canal vista biases the light. Guard: for
  night setups attach a night board (make one) or nothing, and lead the
  prompt with "Night."
- **Text leakage**: telescope_time_tunnel A rendered "SLOW PUSH IN" labels.
  Camera-direction phrases in the body can be drawn as annotations; keep
  motion language out of *still* prompts (it belongs in the video prompt).
- **Uninvited witness figures**: environment setups (greenhouse, drumwall,
  weather, iris, goodnight) keep adding two silver-suited men, sometimes with
  horns/saxophones. Sometimes charming (drumwall B), sometimes wrong. Guard:
  "no people" on pure environment stills; allow "two distant witnesses" only
  where the shot body asks for them.
- **Triptych/strip layouts** on continuous-move setups (chorus_plunge A)
  — reject; one frame per still.
- **Agent context contamination**: one stray desk-lamp astronaut still
  appeared inside another setup's request. Long agent sessions drift; start
  a new session per batch of ~10 setups.

## Per-setup verdicts so far (17 stills labeled)

| setup | verdict |
|---|---|
| night_iris_title | A and B both strong; A (moon over canal in iris) preferred |
| colony_goodnight_cascade | B (night, bridge figures) good; A is daytime — reject |
| telescope_time_tunnel | B good (stage apparatus); A text leak — reject |
| duet_lamplight_astronaut_sync | A, B, C all wear glasses — regen with guard; B's bunk/porthole composition is the keeper layout |
| duet_lamplight_astronomer_sync | B (desk lamp, colony painting) excellent; A is just her portrait — reject |
| canal_junction_turn | A and B both excellent top-down brass junctions |
| chorus_plunge | B usable (splash + underwater cross-section); A triptych — reject |
| drumwall_colony | B (night fountains) excellent; A daytime jazz band — reject |

Remaining 29 setups: stills exist in Flow; download and labeling pending.
