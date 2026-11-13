"""Test file for date_fetch microservice. Will test
to make sure all errors and valid input correct."""

import unittest
import multiprocessing as mp
import subprocess as sp
import zmq

#Setup socket, other data
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5561")

#run datefetch as subprocess
def run_df():
    sp.run(["python3", "./date_fetch.py"])

df = mp.Process(target=run_df)
df.start()

class Test_Df(unittest.TestCase):

    ## Test valid input

    ## Verify all output formats working
    def test_mmddyy_out(self):
        request = {
            "date": "11/10/2026",
            "input_format": "%m/%d/%Y",
            "output_format": "%m/%d/%y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertTrue(response["success"])
        self.assertEqual(response["output_date"], "11/10/26")

    def test_daymonthyearshort_out(self):
        request = {
                    "date": "11/10/2026",
                    "input_format": "%m/%d/%Y",
                    "output_format": "%a, %b %d, %Y"
                }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertTrue(response["success"])
        self.assertEqual(response["output_date"], "Tue, Nov 10, 2026")

    def test_daymonthlong_out(self):
        request = {
            "date": "11/10/2026",
            "input_format": "%m/%d/%Y",
            "output_format": "%A, %B, %j"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertTrue(response["success"])
        self.assertEqual(response["output_date"], "Tuesday, November, 314")

    ## Verify all input formats working
    def test_daymonthyearshort_in(self):
        request = {
            "date": "Tue, Nov 11, 2026",
            "input_format": "%a, %b %d, %Y",
            "output_format": "%m/%d/%y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertTrue(response["success"])
        self.assertEqual(response["output_date"], "11/11/26")

    def test_daymonthlong_in(self):
        request = {
            "date": "Tuesday, November, 314, 2026",
            "input_format": "%A, %B, %j, %Y",
            "output_format": "%m/%d/%y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertTrue(response["success"])
        self.assertEqual(response["output_date"], "11/10/26")

    ##Test errors

    ## Test valid json catching
    def test_json_error(self):
        """Test if passing a non-json object returns an error."""
        request = "Faulty Data"
        socket.send_string(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    ## Test missing key catching
    def test_date_key_error(self):
        """missing date key"""
        request = {
            "input_format": "%m/%d/%Y",
            "output_format": "%m/%d/%y"
        }
        socket.send_json(request)
        print("seeking date key error response...")
        response = socket.recv_json()
        print("response received.")
        self.assertFalse(response["success"])

    def test_inform_key_error(self):
        """missing input format key"""
        request = {
            "date": "11/10/2026",
            "output_format": "%m/%d/%Y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    def test_outform_key_error(self):
        "test missing output format key error catching"
        request = {
            "date": "11/10/2026",
            "input_format": "%m/%d/%Y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    ## Test Bad Value Catching
    def test_value_error(self):
        """Test invalid date catching"""
        request = {
            "date": "02/31/2026",
            "input_format": "%m/%d/%Y",
            "output_format": "%A, %B %d, %Y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    def test_date_type_error(self):
        """Test type error catching for date"""
        request = {
            "date": False,
            "input_format": "%m/%d/%Y",
            "output_format": "%A, %B %d, %Y"
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    def test_informat_type_error(self):
        """Test type error catching for input format"""
        request = {
                    "date": "11/11/2026",
                    "input_format": False,
                    "output_format": "%A, %B %d, %Y"
                }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])
    
    def test_outformat_type_error(self):
        """Test type error catching for output format"""
        request = {
            "date": "11/11/2026",
            "input_format": "%m/%d/%Y",
            "output_format": False
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])

    def test_zzz_end(self):
        """End datefetch"""
        request = {
            "end": True
        }
        socket.send_json(request)
        response = socket.recv_json()
        self.assertFalse(response["success"])


if __name__ == "__main__":
    unittest.main()
    df.join()
    socket.close()
