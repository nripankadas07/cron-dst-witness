from datetime import datetime
import unittest
from zoneinfo import ZoneInfo
from cron_dst_witness import analyze, field, utc_witnesses


def data(expr='30 2 * * *',zone='America/New_York',start='2026-03-08',days=1):
    return {'expression':expr,'zone':zone,'start_date':start,'days':days}


class Tests(unittest.TestCase):
    def test_spring_forward_missing_slot(self):
        r=analyze(data());self.assertEqual(r['counts'],{'missing':1,'unique':0,'ambiguous':0});self.assertEqual(r['anomalies'][0]['witnesses'],[])
    def test_fall_back_two_exact_utc_instants(self):
        r=analyze(data('30 1 * * *',start='2026-11-01'));self.assertEqual([x['utc'] for x in r['anomalies'][0]['witnesses']],['2026-11-01T05:30:00+00:00','2026-11-01T06:30:00+00:00'])
    def test_normal_slot_deduplicates_folds(self):
        self.assertEqual(analyze(data(zone='UTC'))['counts']['unique'],1)
    def test_half_hour_fall_back(self):
        w=utc_witnesses(datetime(2026,4,5,1,45),ZoneInfo('Australia/Lord_Howe'));self.assertEqual(len(w),2);self.assertEqual(w[0]['offset_seconds']-w[1]['offset_seconds'],1800)
    def test_half_hour_spring_forward(self):
        self.assertEqual(utc_witnesses(datetime(2026,10,4,2,15),ZoneInfo('Australia/Lord_Howe')),[])
    def test_dom_dow_or_semantics(self):
        self.assertEqual(analyze(data('0 0 13 * 1','UTC','2026-10-12',2))['counts']['unique'],2)
    def test_wildcard_dom_requires_dow_match(self):
        self.assertEqual(analyze(data('0 0 * * 1','UTC','2026-10-12',2))['counts']['unique'],1)
    def test_sunday_seven_alias(self):
        self.assertEqual(analyze(data('0 0 * * 7','UTC','2026-10-11'))['counts']['unique'],1)
    def test_steps_lists_ranges(self):
        self.assertEqual(field('5/20',0,59),{5,25,45});self.assertEqual(field('1-5/2,8',0,10),{1,3,5,8})
    def test_reject_syntax_and_bounds(self):
        for expr in ['0 0 * * MON','60 0 * * *','*/0 0 * * *','0 0 * * * *']:
            with self.subTest(expr=expr),self.assertRaises(ValueError):analyze(data(expr))
    def test_invalid_zone_date_and_days(self):
        with self.assertRaises(KeyError):analyze(data(zone='Not/AZone'))
        with self.assertRaises(ValueError):analyze(data(start='2026-02-30'))
        for n in [0,32,True]:
            with self.subTest(n=n),self.assertRaises(ValueError):analyze(data(days=n))
    def test_all_minutes_bound(self):
        self.assertEqual(analyze(data('* * * * *','UTC','2026-10-13',1))['counts']['unique'],1440)


if __name__=='__main__':unittest.main()
