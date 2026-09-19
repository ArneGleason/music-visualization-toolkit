# Kling automation routes — checked 2026-09-15

Official sources inspected in browser:
- https://kling.ai/app/mcp
- https://kling.ai/app/mcp/guide
- https://kling.ai/document-api/pricing/base/video

MCP endpoint https://kling.ai/mcp. Official CLI package @klingai/cli-global. Both use OAuth and existing personal paid subscription credits, same web pricing; bonus credits, off-peak free generation and Team benefits unavailable via MCP/CLI. Guide recommends choosing CLI or MCP, not both.

CLI supports local reference upload, image_to_video, reusable Elements, motion_control, account credit checks and query_tasks. Query returns works[].url; result URLs expire after 24 hours. This provides a documented route for automatic downloads without browser Download clicks, but end-to-end downloading is not yet verified here. 5 QPS documented. Generation cannot be canceled after submission.

Separate developer API price table: Kling 3.0 no audio at 1080p is 0.8 units / second ($0.112/s), so 5 seconds = 4 API units ($0.56 list price). These API units are not web credits. Package purchase requirements/discounts not verified. Our prior web test was 40 credits.

Recommendation: official CLI for local batch generation, persistent task IDs, automatic retrieval and saving to runtime with scene/shot identifiers, then catalog and Blender assembly. Test account access and result retrieval before further rendering. No CLI/MCP installed or authorized, no API purchase, and no second render submitted during this research.
