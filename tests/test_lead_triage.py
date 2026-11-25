import csv
import tempfile
import unittest
from pathlib import Path
from lead_triage import prioritize, process


class LeadTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(lead_id='demo', service='cleaning', consent='yes', urgency='high', service_area='yes')

    def test_high_priority(self):
        self.assertEqual(prioritize(self.row)['score'], 90)

    def test_no_consent(self):
        self.assertEqual(prioritize(dict(self.row, consent='no'))['next_action'], 'do_not_contact')

    def test_outside_area(self):
        self.assertEqual(prioritize(dict(self.row, service_area='no'))['next_action'], 'review_service_area')

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            prioritize(dict(self.row, urgency='unknown'))

    def test_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'output.csv'
            self.assertEqual(process('examples/leads.csv', dest), 4)
            with dest.open(newline='', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]['lead_id'], 'DEMO-002')
            with self.assertRaises(FileExistsError):
                process('examples/leads.csv', dest)


if __name__ == '__main__':
    unittest.main()
