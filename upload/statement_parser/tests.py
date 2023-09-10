from pprint import pprint
from django.test import TestCase
from upload.statement_parser.parser import parse_statement_text
from upload.statement_parser.sample_statement import FULL_STATEMENT_LIST

class StringParserTest(TestCase):

    def test_parse_statement(self):
        parsed_statement = parse_statement_text(FULL_STATEMENT_LIST)
        # pprint(parsed_statement)

        self.assertIn('metadata', parsed_statement)
        metadata = parsed_statement['metadata']
        self.assertEqual(metadata['Customer Name'], "DENIS MWAI GITHINJI")
        self.assertEqual(metadata['Mobile Number'], "0712224283")
        self.assertEqual(metadata['Email Address'], "dmwaigithinji@gmail.com")
        self.assertEqual(metadata['Statement Period'], "01 Sep 2023 - 09 Sep 2023")
        self.assertEqual(metadata['Request Date'], "09 Sep 2023")

        self.assertIn('summary', parsed_statement)
        summary = parsed_statement['summary']
        self.assertEqual(summary['SEND MONEY'],{'paid_in': 0, 'paid_out': 8221})
        self.assertEqual(summary['RECEIVED MONEY'], {'paid_in': 89.80, 'paid_out': 0})
        self.assertEqual(summary['AGENT DEPOSIT'], {'paid_in': 0, 'paid_out': 0})
        self.assertEqual(summary['AGENT WITHDRAWAL'], {'paid_in': 0, 'paid_out': 0})
        self.assertEqual(summary['LIPA NA M-PESA (PAYBILL)'], {'paid_in': 0, 'paid_out': 599517})
        self.assertEqual(summary['LIPA NA M-PESA (BUY GOODS)'], {'paid_in': 0, 'paid_out': 15917})
        self.assertEqual(summary['OTHERS'], {'paid_in': 707568, 'paid_out': 84304.91})
        self.assertEqual(summary['TOTAL'], {'paid_in': 708859.97, 'paid_out': 707959.91})

        self.assertIn('transactions', parsed_statement)
        transactions = parsed_statement['transactions']
        self.assertEqual(len(transactions), 77)

        transaction1 = transactions[0]
        self.assertEqual(transaction1['mpesa_code'], 'RI99AUWQQZ')
        self.assertEqual(transaction1['transaction_description'], 'Customer Transfer to - 2547******550 ESTHER NGANGA')
        self.assertEqual(transaction1['amount'], -60)
        self.assertEqual(transaction1['balance'], 2773.25)

        transaction18 = transactions[18]
        self.assertEqual(transaction18['mpesa_code'], 'RI867I9B9W')
        self.assertEqual(transaction18['transaction_description'], 'OverDraft of Credit Party')
        self.assertEqual(transaction18['amount'], 405)
        self.assertEqual(transaction18['balance'], 405)

        transaction76 = transactions[76]
        self.assertEqual(transaction76['mpesa_code'], 'RI16MCWAAU')
        self.assertEqual(transaction76['transaction_description'], 'Merchant Payment Online to 7299147 - PRESERVING VALUE ENTERPRISES')
        self.assertEqual(transaction76['status'], 'Completed')
        self.assertEqual(transaction76['amount'], -220)
        self.assertEqual(transaction76['balance'], 1653.19)
