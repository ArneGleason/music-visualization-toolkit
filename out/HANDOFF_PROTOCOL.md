# Shared local handoff convention

One versioned folder per approved experiment. Both agents read handoff.json
before acting. Media remains outside Git; commits are not a notification system.

1. Codex prepares exact inputs, hashes, timing, authority limits and output paths;
   status: ready_for_claude_not_submitted.
2. Claude executes within those limits, preserves originals, writes RECEIPT.md,
   and adds claude_result with actual paths, hashes and measured coverage.
   Set status to claude_done_ready_for_codex_verification only after saving files.
3. User prompts Codex to check the named folder. Codex verifies hashes and timing,
   produces same-clock previews, preserves Claude's receipt/result, and adds its
   own codex_result. Status: codex_verified_ready_for_owner_review.
4. Owner playback approval and production adoption are separate decisions. Record
   each explicitly; verified audio timing is not perceptual lip-sync approval.

If blocked, record the stage and blocker; never duplicate a paid submission to
resolve an unknown download status. Preserve the exact clock and guide inputs.
For revisions, use a new version rather than silently changing prior contracts.

Shared local files are readable without a commit. Git is for backup/versioning,
not an inter-agent wake-up. No automatic polling or scheduled watcher is configured
by this convention. Neither agent should claim live awareness of the other.
