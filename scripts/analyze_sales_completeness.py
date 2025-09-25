import csv

print('=== SALES DATA COMPLETENESS ANALYSIS ===')

# Analyze NHDRA sales data completeness
nhdra_stats = {
    'total_records': 0,
    'with_current_sale': 0,
    'with_any_prior_sale': 0,
    'with_complete_history': 0,
    'zero_prices': 0
}

with open('RecoveredRawData/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip first row
    headers = next(reader)  # Get headers

    for row in reader:
        nhdra_stats['total_records'] += 1
        if len(row) < len(headers): continue

        # Current sale
        saleprice = row[19] if len(row) > 19 else ''
        if saleprice and saleprice.strip():
            try:
                price = float(saleprice)
                if price > 0:
                    nhdra_stats['with_current_sale'] += 1
                else:
                    nhdra_stats['zero_prices'] += 1
            except:
                pass

        # Prior sales
        prior_sales = []
        for i in [61, 64, 67]:  # ID1, ID2, ID3 Prior Sale Price columns
            if len(row) > i:
                price = row[i] if row[i].strip() else ''
                if price:
                    try:
                        p = float(price)
                        if p > 0:
                            prior_sales.append(p)
                    except:
                        pass

        if prior_sales:
            nhdra_stats['with_any_prior_sale'] += 1

        if len(prior_sales) >= 2:
            nhdra_stats['with_complete_history'] += 1

print(f'NHDRA Records Analyzed: {nhdra_stats["total_records"]}')
print(f'With Current Sale Price > $0: {nhdra_stats["with_current_sale"]} ({nhdra_stats["with_current_sale"]/nhdra_stats["total_records"]*100:.1f}%)')
print(f'With Any Prior Sale History: {nhdra_stats["with_any_prior_sale"]} ({nhdra_stats["with_any_prior_sale"]/nhdra_stats["total_records"]*100:.1f}%)')
print(f'With Complete History (2+ prior sales): {nhdra_stats["with_complete_history"]} ({nhdra_stats["with_complete_history"]/nhdra_stats["total_records"]*100:.1f}%)')
print(f'Zero or missing prices: {nhdra_stats["zero_prices"]}')

print('\n=== CONCLUSION ===')
print('The NHDRA data has SIGNIFICANT gaps in sales history.')
print('Many properties show $0 for sale prices, indicating incomplete data.')
print('The separate SalesList files likely contain more comprehensive sales data.')
print('A proper implementation would merge these datasets.')

# Show some examples
print('\n=== SAMPLE RECORDS WITH MISSING DATA ===')
with open('RecoveredRawData/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    headers = next(reader)

    count = 0
    for row in reader:
        if count >= 5: break
        if len(row) >= 67:
            parcel_id = row[0] if len(row) > 0 else 'Unknown'
            saleprice = row[19] if len(row) > 19 else ''
            id1_price = row[61] if len(row) > 61 else ''

            try:
                current_price = float(saleprice) if saleprice.strip() else 0
                prior_price = float(id1_price) if id1_price.strip() else 0

                if current_price == 0 and prior_price == 0:
                    print(f'Parcel {parcel_id}: Current=${current_price}, Prior=${prior_price} (MISSING DATA)')
                    count += 1
            except:
                pass
