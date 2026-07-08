# Prequalification leads inbox

All Pure Capital prequalification form submissions land here for CRM import on **aminaspeace.com**.

## Server path

```
/var/www/Pure-Finance/submissions/prequalification/
```

## Layout

| Path | Purpose |
|------|---------|
| `index.jsonl` | Append-only feed — one JSON object per line (newest at bottom). Ideal for CRM polling. |
| `leads/{submission_id}/lead.json` | Full submission payload |
| `leads/{submission_id}/crm.json` | Flattened fields for CRM mapping |
| `leads/{submission_id}/files/` | Uploaded bank statements, ID, voided check, signatures |

## CRM polling

1. Tail or watch `index.jsonl` for new lines.
2. Each line includes `submission_id`, `lead_dir`, and key contact fields.
3. Load `crm.json` or `lead.json` from `lead_dir` for full detail and file paths.

## Permissions

Directory should be readable by the CRM process user (e.g. `www-data` or a shared `crm` group). Web access is denied via `.htaccess`.
