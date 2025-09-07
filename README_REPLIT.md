# README — Replit bootstrap (Node)
- **Server**: `server.js` serves `docs/site` on `$PORT` (Express).
- **Data prep**: `tools/pages_ready.mjs` copies & rewrites headers into `docs/site/data/` and `docs/data/`.
- **Scripts**:
  - `npm run prepare-data`
  - `npm start`

## Header expectations (Title Case in the web app)
- parcels.csv: `Parcel, Address, Owner, Class, Acres, Land, Bldg, Total` (+ mailing fields ok)
- buildings.csv: `Parcel, Year Built, GLA`
- land.csv: `Parcel` (and `Acres` if present)

Adjust `tools/pages_ready.mjs` if your normalized headers differ.
