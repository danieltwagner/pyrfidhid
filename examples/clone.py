from __future__ import print_function
from time import sleep
from rfidhid.core import RfidHid

def main():
    """Main Read Tag Function"""

    try:
        # Try to open RFID device using default vid:pid (ffff:0035)
        rfid = RfidHid()
    except Exception as e:
        print(e)
        exit()

    # Initialize device
    print('Initializing device...')
    rfid.init()
    sleep(2)
    print ('Ready to read a tag...\n')

    while True:
        payload_response = rfid.read_tag()
        if payload_response.has_id_data():
            uid = payload_response.get_tag_uid()
            cid = payload_response.get_tag_cid()
            print('uid: %s' % uid)
            print('customer_id: %s' % cid)
            print('CRC Sum: %s' % hex(payload_response.get_crc_sum()))
            w26 = payload_response.get_tag_w26()
            if w26:
                print('W26: facility code = %d, card number = %d' % w26)
            print('')
            result = raw_input('Copy this tag? (Y/n)').strip()
            if result in ['', 'y', 'Y']:
                break
            else:
                print ('Ready to read a tag...\n')
        sleep(0.1)

    print ('Ready to write tag...\n')
    while True:
        payload_response = rfid.read_tag()
        if payload_response.has_id_data():

                rfid.write_tag_from_cid_and_uid(cid, uid)
                sleep(0.1) # you cannot immediately read after a write operation

                payload_response_w = rfid.read_tag()
                # Write verification
                if payload_response_w.get_tag_cid() == cid and payload_response_w.get_tag_uid() == uid:
                    print('Write OK!')
                else:
                    print('Write ERROR!')
                break
        sleep(0.1)


if __name__ == "__main__": 
    main()
