# Thai Writing Style — customer-facing summaries

Style preferences for Thai summaries written for customer support / Jira comments / hospital staff audiences. Converted from the `feedback-thai-writing-style` auto-memory on 2026-07-22 so skills can reference it directly.

## Rules

- Avoid casual intensifiers like `เป๊ะ`, `เลย`, `มากๆ`. Plain phrasing reads more professional.
- Prefer **labeled sub-points** over inline bold emphasis. Write `จังหวะที่พบบ่อยเป็นพิเศษ: เมื่อ...` rather than `**พบบ่อยเป็นพิเศษเมื่อ**...`.
- Avoid robotic/technical metaphors (user flagged `ตัวเร่ง` as robotic). Use plain descriptive phrasing.
- Header is `**สรุปสาเหตุและแนวทางแก้**` — no `(สั้น)` suffix.
- Keep natural Thai flow — favor `คนไข้ที่เปลี่ยนไปมา ถูกแทนที่` over `คนไข้ที่ขยับมาแทนที่` when describing data row changes.

## Why

The user reviews and rewords AI-drafted Thai for customer-facing tickets before posting. Corrections consistently move toward neutral, structured prose suitable for non-technical hospital staff. Drafting in that register from the start saves round-trips.

## How to apply

When asked for a Thai summary (Jira comments, customer support, hospital staff audiences):
1. Draft with neutral phrasing — no casual intensifiers.
2. Structure callouts as `Label: content`, not `**bolded phrase**...`.
3. If a translated tech term sounds robotic (e.g. "accelerator" → `ตัวเร่ง`), pick a descriptive substitute or restructure as a labeled point.

## Example diffs (user edits on ACS-32)

- Drafted: `**พบบ่อยเป็นพิเศษเมื่อ**ตารางถูกจัดเรียง...`
- Their version: `จังหวะที่พบบ่อยเป็นพิเศษ: เมื่อตารางถูกจัดเรียง...`
- Drafted: `แถวที่สลับมาต้องมีสถานะเหมือนกันเป๊ะ`
- Their version: `แถวที่สลับมาต้องมีสถานะเหมือนกัน`
