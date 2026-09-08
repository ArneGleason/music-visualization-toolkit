# Lip-sync only the wide souvenir-shop take

Read handoff.json and verify input hashes. Owner approves the current alien-head emphasis and blurred punch-in. Close-up mouth timing is accepted as-is: do not submit it to Kling, alter it or regenerate anything.

Use only this folder's base.mp4 and guide.wav. Base is the untouched wide video stream, remuxed without generated audio. One Kling Lip Sync job, select the real woman, NOT her reflection or the alien-head display. Guide starts at0, full8seconds, Sound from Video OFF. No additional offset, silence trimming, TTS, audio normalization, source crop or retiming. Stop if correct face cannot be selected or cost exceeds10credits. No Flow, purchases, automatic retries or alternate submissions.

Clock: original wide source0 maps song2387 at24fps. No starts at source0.5seconds (song2399); Don't make it better starts1.0seconds (2411), ends2.083333seconds (2437). Preserve the full guide's context. Only source12..44 (0.5..1.833333seconds) is visible in the approved wide/push, before switching to the untouched close-up at2431. Inspect articulation through source50 as well, but do not extend the wide shot. Subsequent guide words are context, not permission to use more wide footage.

Download the untouched full result promptly as original_<job-id>.mp4 and a byte-identical synced.mp4. Keep native FPS/timestamps; Codex conforms by timestamps later. No assembly, FX baking, replacement audio or production edits. Work only in this folder, no commit. Check after30seconds then about20seconds, near90percent about10seconds; tool time counts. Respect rate limits, avoid long backoff or duplicate jobs.

Write RECEIPT.md with job/settings/cost, input/output hashes, progress times, native rate/count/duration/start, minimum usable coverage, word-level mouth observations and any reflection/identity/camera changes. Quiet base acting may produce weak articulation; report missing words honestly. Add claude_result and set status claude_done_ready_for_codex_verification only once file and receipt exist. Codex will reapply the approved alien-head effect and punch-in locally. No close-up lip-sync pass.
