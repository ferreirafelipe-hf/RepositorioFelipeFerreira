"""Prioritize small-business leads using transparent local rules."""
import argparse
import csv
from pathlib import Path

FIELDS = ('lead_id', 'service', 'consent', 'urgency', 'service_area')
URGENCY = {'low': 10, 'normal': 20, 'high': 40}


def prioritize(row):
    clean = {field: (row.get(field) or '').strip() for field in FIELDS}
    if not clean['lead_id'] or not clean['service']:
        raise ValueError('lead_id and service are required')
    for field in ('consent', 'urgency', 'service_area'):
        clean[field] = clean[field].lower()
    if any(clean[field] not in ('yes', 'no') for field in ('consent', 'service_area')):
        raise ValueError('consent and service_area must be yes or no')
    if clean['urgency'] not in URGENCY:
        raise ValueError('urgency must be low, normal or high')
    if clean['consent'] == 'no':
        score, action = 0, 'do_not_contact'
    elif clean['service_area'] == 'no':
        score, action = 0, 'review_service_area'
    else:
        score = 50 + URGENCY[clean['urgency']]
        action = 'prioritize_follow_up' if score >= 90 else 'standard_follow_up'
    return dict(clean, score=score, next_action=action)


def process(source, destination):
    if Path(source).resolve() == Path(destination).resolve():
        raise ValueError('Input and output must be different files')
    with open(source, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError('Missing required CSV columns')
        rows, seen = [], set()
        for row in reader:
            try:
                result = prioritize(row)
                if result['lead_id'] in seen:
                    raise ValueError('Duplicate lead_id')
                seen.add(result['lead_id'])
                rows.append(result)
            except ValueError as exc:
                raise ValueError(f'CSV line {reader.line_num}: {exc}') from exc
    rows.sort(key=lambda row: -row['score'])
    def safe(value):
        if isinstance(value, str) and value.startswith(('=', '+', '-', '@', '\t', '\r', '\n')):
            return "'" + value
        return value
    with open(destination, 'x', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[*FIELDS, 'score', 'next_action'])
        writer.writeheader()
        writer.writerows({key: safe(value) for key, value in row.items()} for row in rows)
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('destination', help='New output CSV; existing files are not overwritten')
    args = parser.parse_args()
    try:
        count = process(args.source, args.destination)
    except (ValueError, OSError, csv.Error) as exc:
        parser.exit(2, f'Error: {exc}\n')
    print(f'Processed {count} leads')


if __name__ == '__main__':
    main()
