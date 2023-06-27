import json

import requests


class APIService:

    def __init__(self) -> None:
        self.headers = ''
        self.master = "http://ncuaiot.ap-northeast-1.elasticbeanstalk.com/"
        # self.master = "http://ip-172-31-32-214.ap-northeast-1.compute.internal/"
        self.dev = "http://ncuaiot-dev.ap-northeast-1.elasticbeanstalk.com/"
        # self.dev = "http://ip-172-31-13-231.ap-northeast-1.compute.internal/"
        self.aimodel = "http://ip-172-31-45-198.ap-northeast-1.compute.internal/"
        self.endpoint = ''

    def setEndpoint(self, folderName):
        if 'dev' in folderName:
            self.endpoint = self.dev
        else:
            self.endpoint = self.master
        print('endpoint= ', self.endpoint)
        self.login()

    def login(self):
        login_content = {
            "password": "",
            "username": ""
        }
        try:
            login_api = requests.post(
                f'{self.endpoint}api/authenticate/login', json=login_content)
            token = login_api.json()['token']
            self.headers = {"Authorization": f'Bearer {token}'}
        except requests.exceptions.RequestException as e:
            print(e)
            raise ('login failed')

    def post_feature_value(self, feature_content):
        try:
            r = requests.post(f"{self.endpoint}api/FeatureValue",
                              json=feature_content, headers=self.headers)
            print(feature_content)
        except requests.exceptions.RequestException as e:
            raise ("post feature_value failed")

    def post_picture(self, feature_content):
        try:
            r = requests.post(f"{self.endpoint}api/FeatureValue/picture",
                              json=feature_content, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise ("post picture failed")

    def get_neccessary_var_via_motion_data_id(self, motion_data_id):
        r = requests.get(
            f'{self.endpoint}api/MotionData?MotionDataId={motion_data_id}', headers=self.headers)
        response_data = r.json()
        activity_id = response_data['Data'][0]['ActivityId']
        course_type = response_data['Data'][0]['CourseType']
        course_type_map = {"CPT": "C", "AUDIO": "A",
                           "WCST": "W", "STROOP": "S"}
        return {"activity_id": activity_id, "game_type": course_type_map.get(course_type)}

    def get_ac_model_value(self, acmodel_content):
        try:
            r = requests.post(f'{self.aimodel}acmodel', json=acmodel_content)
            r.raise_for_status()
            ai_score = int(float(r.text)*100)
            print(f"AI Value= {ai_score}")
            return ai_score
        except requests.exceptions.RequestException as e:
            print(e)
            raise ('get ai value error')
        except requests.exceptions.HTTPError as e:
            raise ('received error response from server')

    def post_ai_score(self, ai_score_content):
        try:
            r = requests.post(f'{self.endpoint}api/AiScore',
                              json=ai_score_content, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise ('insert ai score failed')
