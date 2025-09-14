# parcels.csv Schema Analysis

## File Information
- **File Path**: data/parcels.csv
- **File Size**: 3.0MB
- **Row Count**: 5,637+ rows (estimated)

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| parcel_id | string | 1-1, 1-2, 1-3-100 | Primary key, alphanumeric with dashes |
| situs_address | string | 17 FARAWAY LN, 19 FARAWAY LN | Physical property address |
| owner_name | string | "BEATTY, JOHN J ", "LACA, KRISTINE & HERNAN" | Owner names with quotes and formatting |
| mailing_address1 | string | 17 FARAWAY LN, PO BOX 533 | Mailing address line 1 |
| mailing_city | string | WEST LEBANON, HANOVER | Mailing city |
| mailing_state | string | NH | Mailing state (2-letter codes) |
| mailing_zip | string | 03784, 03755 | Mailing ZIP codes |
| class_code | string | 1010, 1300, 9090 | Property classification codes |
| lot_size_acres | decimal | 2.34, 2.29, 1.56 | Lot size in acres |
| land_value | integer | 163900, 148100, 161800 | Assessed land value |
| building_value | integer | 283100, 467700, 359600 | Assessed building value |
| total_value | integer | 461900, 628600, 521900 | Total assessed value |
| nhdra_rem prcl locn street | string | FARAWAY, HILLTOP | NHDRA street location |
| nhdra_rem prcl locn | string | 17 FARAWAY LN, 19 FARAWAY LN | NHDRA property location |
| nhdra_own name | string | "BEATTY, JOHN J &","MASOR, LOIS" | NHDRA owner name |
| nhdra_co own name | string | ,MASOR, LOIS | NHDRA co-owner name (often empty) |
| nhdra_address1 | string | 17 FARAWAY LN | NHDRA mailing address |
| nhdra_city | string | WEST LEBANON | NHDRA city |
| nhdra_state | string | NH | NHDRA state |
| nhdra_zip | string | 03784 | NHDRA ZIP |
| nhdra_book pg | string | 0/0, 2708/0343 | Book/page reference |
| nhdra_saleprice | decimal | 0.0, 419000.0 | Sale price (0 when no recent sale) |
| nhdra_saledate | datetime | 2017-10-23 00:00:00 | Sale date (1900-01-01 when no sale) |
| nhdra_qualified | string | Q, U | Sale qualification (Q=qualified, U=unqualified) |
| nhdra_grantor | string | "GREENHALGH, LEONARD " | Grantor name |
| nhdra_rem use code | string | 1010, 1300 | Property use code |
| nhdra_lnd zone | string | R3, R2 | Zoning code |
| nhdra_prc ttl lnd area acres | decimal | 2.34, 2.29 | Land area in acres |
| nhdra_prc ttl assess bldg | integer | 283100, 467700 | Building assessment |
| nhdra_prc ttl assess xf | integer | 0, 13900 | Exempt assessment |
| nhdra_prc ttl assess lnd | integer | 163900, 148100 | Land assessment |
| nhdra_prc ttl assess ob | integer | 14900, 12800 | Outbuilding assessment |
| nhdra_prc ttl assess | integer | 461900, 628600 | Total assessment |
| nhdra_cns area living | integer | 2332, 2306 | Living area square footage |
| nhdra_vns ayb | integer | 1963, 1976 | Actual year built |
| nhdra_vns style desc | string | CONTEMPORY, RANCH | Building style description |
| nhdra_rem pid | string | 1, 3804 | Property ID |
| nhdra_vns grade | string | C-, B- | Grade code |
| nhdra_vns grade desc | string | AVG. (-), GOOD (-) | Grade description |
| nhdra_vns roof struct desc | string | GABLE, FLAT | Roof structure |
| nhdra_vns roof cover desc | string | STD SEAM, METAL | Roof covering |
| nhdra_vns int flr1 desc | string | CARPET, HARDWOOD | Floor covering |
| nhdra_vns int wall1 desc | string | DRYWALL, PANEL | Wall material |
| nhdra_vns ext wall1 desc | string | TEX 111, WOOD | Exterior wall material |
| nhdra_cns area effective | integer | 2632, 3043 | Effective area |
| nhdra_vns tot rooms | integer | 7, 6 | Total rooms |
| nhdra_vns num bedrm | integer | 3, 2 | Number of bedrooms |
| nhdra_vns num baths | integer | 2, 1 | Number of bathrooms |
| nhdra_vns num hbaths | integer | 0, 1 | Number of half bathrooms |
| nhdra_vns bathrm style desc | string | GOOD, AVERAGE | Bathroom style |
| nhdra_vns kitchen style desc | string | AVERAGE, GOOD | Kitchen style |
| nhdra_vns heat type desc | string | FORCED H/A, FORCED H/W | Heating type |
| nhdra_vns heat fuel desc | string | OIL, GAS | Heating fuel |
| nhdra_cns pct good | decimal | 79.0, 86.0 | Percent good condition |
| nhdra_cns eyb code | string | A, VG | Effective year built code |
| nhdra_lnd nbhd | string | R2, R5 | Land neighborhood |
| nhdra_vns stories | integer | 2, 1 | Number of stories |
| nhdra_ahd ttl assess bldg | integer | 283100, 496100 | Adjusted building assessment |
| nhdra_ahd ttl assess xf | integer | 0, 7100 | Adjusted exempt assessment |
| nhdra_ahd ttl assess lnd | integer | 163900, 148100 | Adjusted land assessment |
| nhdra_ahd ttl assess ob | integer | 14900, 11200 | Adjusted outbuilding assessment |
| nhdra_ahd ttl assess | integer | 461900, 655400 | Adjusted total assessment |
| nhdra_ID1 Prior Sale Price | integer | 0, 260000 | Prior sale 1 price |
| nhdra_ID1 Prior Sale Date | datetime | 2001-11-05 00:00:00 | Prior sale 1 date |
| nhdra_ID1 Prior Book Page | string | 2602/0661, 2567/0326 | Prior sale 1 book/page |
| nhdra_ID2 Prior Sale Price | integer | 0, 2001 | Prior sale 2 price |
| nhdra_ID2 Prior Sale Date | datetime | 2001-07-25 00:00:00 | Prior sale 2 date |
| nhdra_ID2 Prior Book Page | string | 2567/0326, 1899/0785 | Prior sale 2 book/page |
| nhdra_ID3 Prior Sale Price | integer | 260000, 142500 | Prior sale 3 price |
| nhdra_ID3 Prior Sale Date | datetime | 1989-01-26 00:00:00 | Prior sale 3 date |
| nhdra_ID3 Prior Book Page | string | 1794/0965, 0/0 | Prior sale 3 book/page |

## Sample Rows (First 5)

```csv
parcel_id,situs_address,owner_name,mailing_address1,mailing_city,mailing_state,mailing_zip,class_code,lot_size_acres,land_value,building_value,total_value,nhdra_rem prcl locn street,nhdra_rem prcl locn,nhdra_own name,nhdra_co own name,nhdra_address1,nhdra_city,nhdra_state,nhdra_zip,nhdra_book pg,nhdra_saleprice,nhdra_saledate,nhdra_qualified,nhdra_grantor,nhdra_rem use code,nhdra_lnd zone,nhdra_prc ttl lnd area acres,nhdra_prc ttl assess bldg,nhdra_prc ttl assess xf,nhdra_prc ttl assess lnd,nhdra_prc ttl assess ob,nhdra_prc ttl assess,nhdra_cns area living,nhdra_vns ayb,nhdra_vns style desc,nhdra_rem pid,nhdra_vns grade,nhdra_vns grade desc,nhdra_vns roof struct desc,nhdra_vns roof cover desc,nhdra_vns int flr1 desc,nhdra_vns int wall1 desc,nhdra_vns ext wall1 desc,nhdra_cns area effective,nhdra_vns tot rooms,nhdra_vns num bedrm,nhdra_vns num baths,nhdra_vns num hbaths,nhdra_vns bathrm style desc,nhdra_vns kitchen style desc,nhdra_vns heat type desc,nhdra_vns heat fuel desc,nhdra_cns pct good,nhdra_cns eyb code,nhdra_lnd nbhd,nhdra_vns stories,nhdra_ahd ttl assess bldg,nhdra_ahd ttl assess xf,nhdra_ahd ttl assess lnd,nhdra_ahd ttl assess ob,nhdra_ahd ttl assess,nhdra_ID1 Prior Sale Price,nhdra_ID1 Prior Sale Date,nhdra_ID1 Prior Book Page,nhdra_ID2 Prior Sale Price,nhdra_ID2 Prior Sale Date,nhdra_ID2 Prior Book Page,nhdra_ID3 Prior Sale Price,nhdra_ID3 Prior Sale Date,nhdra_ID3 Prior Book Page
1-1,17 FARAWAY LN ,"BEATTY, JOHN J ",17 FARAWAY LN,WEST LEBANON,NH,03784,1010,2.34,163900,283100,461900,FARAWAY,17 FARAWAY LN ,"BEATTY, JOHN J &","MASOR, LOIS",17 FARAWAY LN,WEST LEBANON,NH,03784,0/0,0.0,2017-10-23 00:00:00,Q,"GREENHALGH, LEONARD ",1010,R3,2.34,283100,0,163900,14900,461900,2332.0,1963.0,CONTEMPORY,1,C-,AVG. (-),GABLE,STD SEAM,CARPET,DRYWALL,TEX 111,2632.0,7.0,3.0,2.0,0.0,GOOD,AVERAGE,FORCED H/A,OIL,79.0,A,R2,2,283100.0,0.0,163900.0,14900.0,461900.0,0.0,2001-11-05 00:00:00,2602/0661,0.0,2001-07-25 00:00:00,2567/0326,260000.0,1989-01-26 00:00:00,1794/0965
1-2,19 FARAWAY LN ,"LACA, KRISTINE & HERNAN",19 FARAWAY LN,WEST LEBANON,NH,03784,1010,2.29,148100,467700,628600,FARAWAY,19 FARAWAY LN ,"LACA, KRISTINE & HERNAN",,19 FARAWAY LN,WEST LEBANON,NH,03784,2708/0343,419000.0,2002-08-30 00:00:00,Q,"GUGGENHEIM, KATO & FRED",1010,R3,2.29,467700,0,148100,12800,628600,2306.0,1976.0,CONTEMPORY,3804,B-,GOOD (-),GABLE,METAL,HARDWOOD,DRYWALL,WOOD,3043.0,6.0,2.0,2.0,1.0,AVERAGE,AVERAGE,FORCED H/W,OIL,86.0,AG,R2,1,496100.0,0.0,148100.0,11200.0,655400.0,0.0,1992-02-14 00:00:00,1952/0373,0.0,1991-02-28 00:00:00,1899/0785,142500.0,1901-01-01 00:00:00,0/0
1-3-100,23 FARAWAY LN,"LUNTER, M & SABOURIN, H CO-TTEES",23 FARAWAY LN,WEST LEBANON,NH,03784,1010,1.56,161800,359600,521900,FARAWAY,23 FARAWAY LN,"LUNTER, M & SABOURIN, H CO-TTEES",LUNTER/SABOURIN REV TRUST,23 FARAWAY LN,WEST LEBANON,NH,03784,4517/132,0.0,2020-05-01 00:00:00,U,"SABOURIN, HEATHER L ",1010,R3,1.56,359600,0,161800,500,521900,1494.0,1940.0,RANCH,3805,B,GOOD,GABLE,STD SEAM,HARDWOOD,DRYWALL,ALUMINUM,2266.0,5.0,3.0,3.0,0.0,AVERAGE,AVERAGE,FORCED H/W,OIL,83.0,VG,R2,1,359600.0,0.0,161800.0,500.0,521900.0,0.0,2012-08-29 00:00:00,3912/0903,0.0,2010-05-18 00:00:00,3701/190,371000.0,2006-07-10 00:00:00,3302/0562
1-3-200,25 FARAWAY LN ,"GALBRAITH, M A & M M TTEES",25 FARAWAY LN,WEST LEBANON,NH,03784,1010,6.2,176200,964300,1140500,FARAWAY,25 FARAWAY LN ,"GALBRAITH, M A & M M TTEES","GALBRAITH, MARGARET A REV TRST",25 FARAWAY LN,WEST LEBANON,NH,03784,4570/841,0.0,2020-10-28 00:00:00,U,"GALBRAITH, MICHAEL M ",1010,R3,6.2,964300,0,176200,0,1140500,3822.0,2005.0,RANCH,5017,A-,V GOOD-,GABLE,ASPHALT SH,HARDWOOD,DRYWALL,CLAPBOARD,5242.0,9.0,4.0,3.0,1.0,AVERAGE,AVERAGE,FORCED H/W,OIL,91.0,A,R2,1,975000.0,0.0,176200.0,0.0,1151200.0,0.0,2005-09-16 00:00:00,3619/0884,0.0,2004-08-19 00:00:00,3039/0907,315000.0,2004-03-01 00:00:00,2963/0832
1-6,31 FARAWAY LN ,"SOX JR, H C & C H TTEES",31 FARAWAY LN,WEST LEBANON,NH,03784,1010,6.59,271100,616700,902300,FARAWAY,31 FARAWAY LN ,"SOX JR, H C & C H TTEES","SOX JR, H C & C H TRST",31 FARAWAY LN,WEST LEBANON,NH,03784,3702/0503,0.0,2010-05-24 00:00:00,Q,"SOX JR, HAROLD C & CAROL H",1010,R3,6.59,616700,13900,271100,600,902300,2732.0,1964.0,CONTEMPORY,3806,A-,V GOOD-,FLAT,MEMBRANE,HARDWOOD,DRYWALL,WOOD,3227.0,7.0,4.0,1.0,0.0,AVERAGE,AVERAGE,RADIANT,OIL,89.0,VG,R2,1,702200.0,7100.0,215200.0,600.0,925100.0,0.0,1994-01-11 00:00:00,2072/0790,0.0,1988-12-07 00:00:00,1780/0917,399000.0,1901-01-01 00:00:00,0/0
```

## Key Observations
- **Wide table**: 74 columns with extensive property assessment data
- **Mixed data sources**: Combines local assessment data with NHDRA state data
- **Inconsistent naming**: Column names have spaces and inconsistent prefixes (some with nhdra_, some without)
- **Data quality issues**: Many null/empty values in NHDRA fields, inconsistent date formats
- **Potential linkage issues**: parcel_id should link to other tables but format may vary

