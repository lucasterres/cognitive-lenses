# Task 3 — Export button (product)

> "Several customers keep asking for an 'export to Excel' button on the reports page. Should we build it this sprint?"

## baseline

Yes, this is a reasonable quick win — export is a common table-stakes feature and repeated customer requests are a strong signal. Scope it tightly: server-side generation of .xlsx for the current report view, respect active filters, cap row counts to protect the backend, and queue large exports with an email link. A couple of days of work, visible customer value, and it reduces support tickets asking for data pulls.

## latent

*Primed with: Child-Curiosity, Empathy, Minimalist, Divergent, Risk questions. Slots enforced.*

Build *something* this sprint, but check what the button is a proxy for first. **Challenged premise:** customers asking for Excel export are usually asking to *do something in Excel* — pivot, join with their own data, feed a BI tool, or email a boss. A raw .xlsx of the current view serves the last case only; a scheduled email report or a CSV/API endpoint may serve the real jobs better and cost the same. Ask the three loudest requesters what they do with the file — one call each. **Named risk:** export is a data-exfiltration surface — respect row-level permissions in the export path (not just the UI), log who exported what, and cap sizes so a 2 M-row report doesn't take the workers down. **Confidence:** high that some export ships well this sprint; moderate on which shape — three customer calls decide it.

## engine

**Planner:** product decision, Standard tier. Child Curiosity (3), Empathy (2), Minimalist (2), Divergent (2), Risk (1), Security (1).

**Lens findings (condensed):** Child Curiosity — why Excel? → to manipulate data → why manipulate? → the report view doesn't answer their actual question → root need: *the data in their tool*, not a file (0.8). Empathy — requesters are power users; the silent majority may need better filters instead; admins inherit a new permission surface (0.7). Divergent — alternatives serving the root need: scheduled email reports, CSV endpoint, direct BI connector; the button is the least flexible of the four (0.7). Minimalist — CSV of the current view is 20% of the .xlsx effort and satisfies most pivot/join jobs (0.75). Security — exports bypass UI-level redaction unless permissions are enforced in the export path; add audit logging (0.8). Risk — unbounded exports as a self-DoS vector (0.7).

**Consensus:** agreement that the request is a proxy for "data in my tool." Conflict — ship-now (momentum, small ask) vs. discover-first (wrong shape risk): resolved by sequencing, since a CSV endpoint underlies every candidate shape anyway.

**Final:** Ship a permission-enforcing, size-capped, audit-logged **CSV export of the current view** this sprint — it is the common substrate of every likely real need. In parallel, call the three loudest requesters and ask what they do with the file; let that pick the follow-up (xlsx polish, scheduled emails, or API). High confidence in the substrate step; the calls resolve the rest.
