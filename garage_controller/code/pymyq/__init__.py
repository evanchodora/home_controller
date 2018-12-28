import requests
import json
import os


class Door:
    def __init__(self):
        self.APP_ID = "Vj8pQggXLhLy0WHahglCD4N1nAkkXQtGYpq2HrHD7H1nvmbT55KqtN6RSF4ILB/i"
        self.LOCALE = "en"

        self.HOST_URI = "myqexternal.myqdevice.com"
        self.LOGIN_ENDPOINT = "api/v4/User/Validate"
        self.DEVICE_LIST_ENDPOINT = "api/v4/UserDeviceDetails/Get"
        self.DEVICE_SET_ENDPOINT = "api/v4/DeviceAttribute/PutDeviceAttribute"

        self.USERNAME = os.environ['MYQEMAIL']
        self.PASSWORD = os.environ['MYQPASSWORD']

        self.myq_userid                  = ""
        self.myq_security_token          = ""
        self.myq_cached_login_response   = ""
        self.myq_device_id               = ""
        self.myq_status                  = ""
        self.last_time                   = ""

        # Login and Get Device ID
        self.login()
        self.get_device_id()

    def login(self):
        params = {
            'username': self.USERNAME,
            'password': self.PASSWORD
        }

        login = requests.post(
                'https://{host_uri}/{login_endpoint}'.format(
                    host_uri=self.HOST_URI,
                    login_endpoint=self.LOGIN_ENDPOINT),
                    json=params,
                    headers={
                        'MyQApplicationId': self.APP_ID
                    }
            )

        auth = login.json()
        self.myq_security_token = auth['SecurityToken']

        return True

    def get_devices(self):
        devices = requests.get(
            'https://{host_uri}/{device_list_endpoint}'.format(
                host_uri=self.HOST_URI,
                device_list_endpoint=self.DEVICE_LIST_ENDPOINT),
                headers={
                    'MyQApplicationId': self.APP_ID,
                    'SecurityToken': self.myq_security_token
                }
        )

        return devices.json()['Devices']

    def get_device_id(self):
        devices = self.get_devices()

        for dev in devices:
            if dev["MyQDeviceTypeName"] in ["VGDO", "Garage Door Opener WGDO"]:
                self.myq_device_id = str(dev["MyQDeviceId"])
                self.myq_status = int(dev["Attributes"][3]["Value"])
                self.last_time = dev["Attributes"][3]["UpdatedDate"]
                break

        return

    def status(self):
        state = self.myq_status
        time = self.last_time
        if state == 1:
            state = "Open"
        elif state == 2:
            state = "Closed"
        elif state == 3:
            state = "Stopped"
        elif state == 4:
            state = "Opening"
        elif state == 5:
            state = "Closing"
        elif state == 8:
            state = "Moving"
        elif state == 9:
            state = "Open"
        else:
            state = "Unknown, please try again"

        return {'state': state, 'last_time': time}

    def change_door_state(self):
        if self.myq_status == 2:
            open_close_state = 1
        elif self.myq_status == 1:
            open_close_state = 0
        else:
            return

        payload = {
            'attributeName': 'desireddoorstate',
            'myQDeviceId': self.myq_device_id,
            'AttributeValue': open_close_state,
        }

        device_action = requests.put(
            'https://{host_uri}/{device_set_endpoint}'.format(
                host_uri=self.HOST_URI,
                device_set_endpoint=self.DEVICE_SET_ENDPOINT),
                data=payload,
                headers={
                    'MyQApplicationId': self.APP_ID,
                    'SecurityToken': self.myq_security_token
                }
        )

        return device_action.status_code == 200
