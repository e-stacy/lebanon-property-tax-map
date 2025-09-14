# v2025-09-05/nhdra.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/v2025-09-05/nhdra.csv
- **Row Count**: 5,600+ rows (estimated)
- **Data Version**: v2025-09-05

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| Unnamed: 0 | string | rem mblu map, 1, 2, 3 | Row index or blank |
| Unnamed: 1 | string | rem mblu map cut, , 15 | Map cut identifier |
| Unnamed: 2 | string | rem mblu block, 1, 2 | Block identifier |
| Unnamed: 3 | string | rem mblu block cut, , | Block cut (often empty) |
| Unnamed: 4 | string | rem mblu lot, ,  | Lot identifier |
| Unnamed: 5 | string | rem mblu lot cut, , | Lot cut (often empty) |
| Unnamed: 6 | string | , , | Empty column |
| Unnamed: 7 | string | rem mblu unit, , | Unit identifier |
| Unnamed: 8 | string | rem mblu unit cut, , | Unit cut (often empty) |
| Unnamed: 9 | string | rem prcl locn street, FARAWAY, N MAIN | Street location |
| Unnamed: 10 | string | rem prcl locn, 17 FARAWAY LN, 434 N MAIN ST | Property location |
| Unnamed: 11 | string | own name, "BEATTY, JOHN J &","MASOR, LOIS" | Owner name |
| Unnamed: 12 | string | co own name, ,MASOR, LOIS | Co-owner name |
| Unnamed: 13 | string | address1, 17 FARAWAY LN | Mailing address |
| Unnamed: 14 | string | address2, , | Address line 2 (often empty) |
| Unnamed: 15 | string | city, WEST LEBANON, NEW YORK | City |
| Unnamed: 16 | string | state, NH | State |
| Unnamed: 17 | string | zip, 03784, 10003-1502 | ZIP code |
| Unnamed: 18 | string | book pg, 0/0, 4813/0100 | Book/page reference |
| Unnamed: 19 | string | saleprice, 0, 2013000 | Sale price |
| Unnamed: 20 | datetime | saledate, 2017-10-23 00:00:00 | Sale date |
| Unnamed: 21 | string | qualified, Q, U | Sale qualification |
| Unnamed: 22 | string | grantor, "GREENHALGH, LEONARD " | Grantor name |
| Unnamed: 23 | string | rem use code, 1010, 3520 | Property use code |
| Unnamed: 24 | string | lnd zone, R3 | Zoning code |
| Unnamed: 25 | decimal | prc ttl lnd area acres, 2.34, 0.74 | Land area in acres |
| Unnamed: 26 | integer | prc ttl assess bldg, 283100, 897100 | Building assessment |
| Unnamed: 27 | integer | prc ttl assess xf, 0, 0 | Exempt assessment |
| Unnamed: 28 | integer | prc ttl assess lnd, 163900, 257500 | Land assessment |
| Unnamed: 29 | integer | prc ttl assess ob, 14900, 22900 | Outbuilding assessment |
| Unnamed: 30 | integer | prc ttl assess, 461900, 1177500 | Total assessment |
| Unnamed: 31 | integer | cns area living, 2332, 3368 | Living area |
| Unnamed: 32 | integer | vns ayb, 1963, 1960 | Year built |
| Unnamed: 33 | string | vns style desc, CONTEMPORY, SCHOOL | Building style |
| Unnamed: 34 | string | rem pid, 1, 2 | Property ID |
| Unnamed: 35 | string | vns grade, C-, B+ | Grade code |
| Unnamed: 36 | string | vns grade desc, AVG. (-), Good (+) | Grade description |
| Unnamed: 37 | string | vns roof struct desc, GABLE, GABLE | Roof structure |
| Unnamed: 38 | string | vns roof cover desc, STD SEAM, ASPHALT SH | Roof covering |
| Unnamed: 39 | string | vns int flr1 desc, CARPET, CARPET | Floor covering |
| Unnamed: 40 | string | vns int wall1 desc, DRYWALL, DRYWALL | Wall material |
| Unnamed: 41 | string | vns ext wall1 desc, TEX 111, CLAPBOARD | Exterior wall |
| Unnamed: 42 | integer | cns area effective, 2632, 4743 | Effective area |
| Unnamed: 43 | integer | vns tot rooms, 7,  | Total rooms |
| Unnamed: 44 | integer | vns num bedrm, 3,  | Bedrooms |
| Unnamed: 45 | integer | vns num baths, 2,  | Bathrooms |
| Unnamed: 46 | integer | vns num hbaths, 0,  | Half bathrooms |
| Unnamed: 47 | string | vns bathrm style desc, GOOD,  | Bathroom style |
| Unnamed: 48 | string | vns kitchen style desc, AVERAGE,  | Kitchen style |
| Unnamed: 49 | string | vns heat type desc, FORCED H/A, FORCED H/A | Heating type |
| Unnamed: 50 | string | vns heat fuel desc, OIL, OIL | Heating fuel |
| Unnamed: 51 | string | vns ac type desc, ,  | AC type (often empty) |
| Unnamed: 52 | decimal | cns pct good, 79, 68 | Percent good |
| Unnamed: 53 | string | cns eyb code, A, VG | Effective year built code |
| Unnamed: 54 | string | lnd nbhd, R2, R5 | Land neighborhood |
| Unnamed: 55 | integer | vns stories, 2, 1 | Stories |
| Unnamed: 56 | integer | ahd ttl assess bldg, 283100, 822700 | Adjusted building assessment |
| Unnamed: 57 | integer | ahd ttl assess xf, 0, 0 | Adjusted exempt assessment |
| Unnamed: 58 | integer | ahd ttl assess lnd, 163900, 257600 | Adjusted land assessment |
| Unnamed: 59 | integer | ahd ttl assess ob, 14900, 22600 | Adjusted outbuilding assessment |
| Unnamed: 60 | integer | ahd ttl assess, 461900, 1102900 | Adjusted total assessment |
| Unnamed: 61 | integer | ID1 Prior Sale Price, 0, 365000 | Prior sale 1 price |
| Unnamed: 62 | datetime | ID1 Prior Sale Date, 2001-11-05 00:00:00 | Prior sale 1 date |
| Unnamed: 63 | string | ID1 Prior Book Page, 2602/0661, 2885/0916 | Prior sale 1 book/page |
| Unnamed: 64 | integer | ID2 Prior Sale Price, 0, 365000 | Prior sale 2 price |
| Unnamed: 65 | datetime | ID2 Prior Sale Date, 2001-07-25 00:00:00 | Prior sale 2 date |
| Unnamed: 66 | string | ID2 Prior Book Page, 2567/0326, 2524/0982 | Prior sale 2 book/page |
| Unnamed: 67 | integer | ID3 Prior Sale Price, 260000, 0 | Prior sale 3 price |
| Unnamed: 68 | datetime | ID3 Prior Sale Date, 1989-01-26 00:00:00 | Prior sale 3 date |
| Unnamed: 69 | string | ID3 Prior Book Page, 1794/0965, 1650/0626 | Prior sale 3 book/page |

## Sample Rows (First 3 data rows)

```csv
Unnamed: 0,Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4,Unnamed: 5,Unnamed: 6,Unnamed: 7,Unnamed: 8,Unnamed: 9,Unnamed: 10,Unnamed: 11,Unnamed: 12,Unnamed: 13,Unnamed: 14,Unnamed: 15,Unnamed: 16,Unnamed: 17,Unnamed: 18,Unnamed: 19,Unnamed: 20,Unnamed: 21,Unnamed: 22,Unnamed: 23,Unnamed: 24,Unnamed: 25,Unnamed: 26,Unnamed: 27,Unnamed: 28,Unnamed: 29,Unnamed: 30,Unnamed: 31,Unnamed: 32,Unnamed: 33,Unnamed: 34,Unnamed: 35,Unnamed: 36,Unnamed: 37,Unnamed: 38,Unnamed: 39,Unnamed: 40,Unnamed: 41,Unnamed: 42,Unnamed: 43,Unnamed: 44,Unnamed: 45,Unnamed: 46,Unnamed: 47,Unnamed: 48,Unnamed: 49,Unnamed: 50,Unnamed: 51,Unnamed: 52,Unnamed: 53,Unnamed: 54,Unnamed: 55,Unnamed: 56,Unnamed: 57,Unnamed: 58,Unnamed: 59,Unnamed: 60,Unnamed: 61,Unnamed: 62,Unnamed: 63,Unnamed: 64,Unnamed: 65,Unnamed: 66,Unnamed: 67,Unnamed: 68,Unnamed: 69
rem mblu map,rem mblu map cut,rem mblu block,rem mblu block cut,rem mblu lot,rem mblu lot cut,,rem mblu unit,rem mblu unit cut,rem prcl locn street,rem prcl locn,own name,co own name,address1,address2,city,state,zip,book pg,saleprice,saledate,qualified,grantor,rem use code,lnd zone,prc ttl lnd area acres,prc ttl assess bldg,prc ttl assess xf,prc ttl assess lnd,prc ttl assess ob,prc ttl assess,cns area living,vns ayb,vns style desc,rem pid,vns grade,vns grade desc,vns roof struct desc,vns roof cover desc,vns int flr1 desc,vns int wall1 desc,vns ext wall1 desc,cns area effective,vns tot rooms,vns num bedrm,vns num baths,vns num hbaths,vns bathrm style desc,vns kitchen style desc,vns heat type desc,vns heat fuel desc,vns ac type desc,cns pct good,cns eyb code,lnd nbhd,vns stories,ahd ttl assess bldg,ahd ttl assess xf,ahd ttl assess lnd,ahd ttl assess ob,ahd ttl assess,ID1 Prior Sale Price,ID1 Prior Sale Date,ID1 Prior Book Page,ID2 Prior Sale Price,ID2 Prior Sale Date,ID2 Prior Book Page,ID3 Prior Sale Price,ID3 Prior Sale Date,ID3 Prior Book Page
1, ,1, , , ,, , ,FARAWAY,17 FARAWAY LN ,"BEATTY, JOHN J &","MASOR, LOIS",17 FARAWAY LN,,WEST LEBANON,NH,03784,0/0,0,2017-10-23 00:00:00,Q,"GREENHALGH, LEONARD ",1010,R3,2.34,283100,0,163900,14900,461900,2332,1963,CONTEMPORY,1,C-,AVG. (-),GABLE,STD SEAM,CARPET,DRYWALL,TEX 111,2632,7,3,2,0,GOOD,AVERAGE,FORCED H/A,OIL,,79,A,R2,2,283100,0,163900,14900,461900,0,2001-11-05 00:00:00,2602/0661,0,2001-07-25 00:00:00,2567/0326,260000,1989-01-26 00:00:00,1794/0965
2, ,15, , , ,, , ,N MAIN,434 N MAIN ST ,TINY SEEDS VILLAGE LLC,,228 PARK AVE S,,NEW YORK,NY,10003-1502,4813/0100,2013000,2023-07-17 00:00:00,Q,CENTURION PROP INC,3520,R3,0.74,897100,0,257500,22900,1177500,3368,1960,SCHOOL,2,B+,Good (+),GABLE,ASPHALT SH,CARPET,DRYWALL,CLAPBOARD,4743,,,,,,,FORCED H/A,OIL,,68,VG,R5,1,822700,0,257600,22600,1102900,365000,2002-05-01 00:00:00,2885/0916,365000,2001-03-23 00:00:00,2524/0982,0,1987-01-22 00:00:00,1650/0626
```

## Key Observations
- **Unusual structure**: Headers are in row 2, actual column names in row 3
- **Many empty columns**: Several Unnamed columns are consistently empty
- **Wide table**: 70 columns with extensive property data
- **Data quality issues**: Missing values in many fields (especially building characteristics for non-residential)
- **Complex data types**: Mix of strings, numbers, dates, and empty values

