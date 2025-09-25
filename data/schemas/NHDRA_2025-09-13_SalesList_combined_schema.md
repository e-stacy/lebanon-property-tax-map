# NHDRA 2025-09-13/SalesList_2020-2024_combined.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/NHDRA 2025-09-13/SalesList_2020-2024_combined.csv
- **Row Count**: 1,477+ rows (estimated)
- **Data Version**: NHDRA 2025-09-13

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| Year | integer | 2020, 2021, 2022 | Sale year |
| SourceFile | string | SalesList - 2020.xlsx | Source filename |
| Verno | integer | 1, 5, 11 | Version number |
| Sale Date | date | 10/1/2019, 10/2/2019 | Sale date (MM/DD/YYYY) |
| Book Page | string | 4469-0764, 4470-0046 | Book and page reference |
| Grantor | string | CADWELL, JAMES T ETA | Seller name |
| Grantee | string | TAMULONIS, ALEXANDER N | Buyer name |
| Deed Type | string | DEED | Type of deed |
| Cama Count | integer | 1 | CAMA record count |
| Acres | decimal | 0.5, 0.4, 1.03 | Property acreage |
| Address | string | 278 MERIDEN RD, 32 WELLINGTON CIR | Property address |
| Map Lot | string | 136-29-100, 118-29 | Map and lot identifier |
| Verified Price | currency | $134,000, $464,467 | Verified sale price |
| Current Assed | currency | $141,100, $406,800 | Current assessed value |
| Previous Assed | currency | $116,800, $357,200 | Previous assessed value |
| Ratio | decimal | 105.3, 87.58 | Sale ratio (price/assessment) |
| Prop Code | integer | 11, 18 | Property code |
| Mod Code | integer | 0 | Modification code |
| Special Code | integer | 0 | Special code |
| XCode1 | string |  | Exemption code 1 |
| XNotes1 | string |  | Exemption notes 1 |
| XCode2 | string |  | Exemption code 2 |
| XNotes2 | string |  | Exemption notes 2 |
| Main XCode | string |  | Main exemption code |
| MainX Notes | string |  | Main exemption notes |
| Town Notes | string | REVAL | Town-specific notes |
| State Notes | string |  | State-specific notes |

## Sample Rows (First 5)

```csv
Year,SourceFile,Verno,"Sale
Date","Book
Page",Grantor,Grantee,"Deed
Type","Cama
Count",Acres,Address,"Map
Lot","Verified
Price","Current
Assed","Previous
Assed",Ratio,"Prop
Code","Mod
Code","Special
Code",XCode1,XNotes1,XCode2,XNotes2,"Main
XCode","MainX
Notes","Town
Notes","State
Notes"
2020,SalesList - 2020.xlsx,1,10/1/2019,4469-0764,"CADWELL, JAMES T ETA; CADWELL, TRACEY ETA","TAMULONIS, ALEXANDER N",DEED,1,0.5,278 MERIDEN RD,136-29-100,"$134,000","$141,100","$116,800",105.3,11,0,0,,,,,,,REVAL,
2020,SalesList - 2020.xlsx,5,10/1/2019,4470-0046,"COOMBS, DAVID W ETA; COOMBS, JULIANN E ETA","PILCHIK, DANA M ETA; PILCHIK, EVAN J ETA",DEED,1,0.4,32 WELLINGTON CIR,118-29,"$464,467","$406,800","$357,200",87.58,11,0,0,,,,,,,REVAL,
2020,SalesList - 2020.xlsx,11,10/2/2019,4470-0181,"HASKINS, DEBRA L ETA; HASKINS, ROYCE H ETA","COOMBS, DAVID WARREN ETA; COOMBS, JULIANN ELIZABETH ETA",DEED,1,1.03,7 LAPLANTE RD,109-69,"$263,667","$259,400","$207,100",98.38,11,0,0,,,,,,,REVAL,
2020,SalesList - 2020.xlsx,13,10/2/2019,4470-0212,"LYNCH, PATRICIA M","PSOTA, JOSEPH E ETA; PSOTA, LINDA E ETA",DEED,1,0,22 RUDSBORO RD 20,56-15-2000,"$64,900","$75,300","$58,000",116.02,18,0,0,,,,,,,REVAL,
2020,SalesList - 2020.xlsx,15,10/3/2019,4470-0528,"ZENG PROPERTIES L L C, ","DESOUZA, MARIA G DANTAS",DEED,1,0,220 MASCOMA ST 77,89-8-7705,"$92,500","$86,000","$82,600",92.97,14,0,0,,,,,,,REVAL,
```

## Key Observations
- **Multi-year sales data**: Covers 2020-2024 sales
- **Complex headers**: Multi-line column headers with embedded newlines
- **Assessment ratios**: Includes sale price to assessment ratios for valuation analysis
- **Exemption tracking**: Multiple exemption code fields for tax analysis
- **Geographic coverage**: Lebanon area properties with map/lot identifiers
- **Data quality**: Comprehensive sales verification data

