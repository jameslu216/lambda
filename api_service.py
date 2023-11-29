import json
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv(override=True)

siteSettings = {"master": "http://ncuaiot.ap-northeast-1.elasticbeanstalk.com/", "dev": "http://ncuaiot-dev.ap-northeast-1.elasticbeanstalk.com/", "sup": "http://sup.xraihealth.com/", "supdev": "http://supdev.xraihealth.com/","www": "www.xraihealth.com/",
                "0407602": "majie.xraihealth.com/", "04189271": "ndmc.xraihealth.com/", "demo": "demo.xraihealth.com/", "develop": "develop.xraihealth.com/", "sports": "sports.xraihealth.com/"}

class APIService:

    def __init__(self) -> None:
        self.headers = ''
        #self.master = "http://ncuaiot.ap-northeast-1.elasticbeanstalk.com/"
        self.master = "http://ip-172-31-45-19.ap-northeast-1.compute.internal/"
        #self.dev = "http://ncuaiot-dev.ap-northeast-1.elasticbeanstalk.com/"
        self.dev = "http://ip-172-31-13-170.ap-northeast-1.compute.internal/"
        self.aimodel = "http://ip-172-31-45-198.ap-northeast-1.compute.internal/"
        self.endpoint = ''
    def login(self):
        print('login',self.endpoint)
        login_content = {
            "password": os.getenv("password"),
            "username": os.getenv("username")
        }
        try:
            login_api = requests.post(
                f'{self.endpoint}api/authenticate/login', json=login_content)
            login_api.raise_for_status()
            token = login_api.json()['token']
            self.headers = {"Authorization": f'Bearer {token}'}
        except requests.exceptions.HTTPError as e:
            raise (e)
        
    # def setEndpoint_old(self, folderName,motion_data_id):
    #     sup_endpoint = siteSettings["supdev"] if 'dev' in folderName else siteSettings["sup"]
    #     sup_login_content = {
    #         "username": os.getenv("sup_username"),
    #         "password": os.getenv("sup_password")
    #     }

    #     try:
    #         login_api = requests.post(
    #             f'{sup_endpoint}api/authenticate/login', json=sup_login_content,verify=False)
    #         token = login_api.json()['token']
    #         self.headers = {"Authorization": f'Bearer {token}'}
    #         #print(requests.get(f'{sup_endpoint}api/MotiondataGet/{motion_data_id}', headers=self.headers,verify=False).json())
    #         site_id = requests.get(f'{sup_endpoint}api/MotiondataGet/{motion_data_id}', headers=self.headers,verify=False).json()['SiteId']
    #         self.endpoint = siteSettings[site_id]
    #         login_api.raise_for_status()
    #         self.login()
    #     except requests.exceptions.HTTPError as e:
    #         raise (e)
        


    def setEndpoint(self, folderName):
        self.endpoint = self.dev if 'dev' in folderName else self.master
        self.login()


    def post_feature_value(self, feature_content):
        try:
            r = requests.post(f"{self.endpoint}api/FeatureValue",
                              json=feature_content, headers=self.headers)
            print(feature_content,r.status_code)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)

    def post_picture(self, feature_content):
        try:
            r = requests.post(f"{self.endpoint}api/FeatureValue/picture",
                              json=feature_content, headers=self.headers)
            print(feature_content,r.status_code)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)
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
            r.raise_for_status()
            return ai_score
        except requests.exceptions.HTTPError as e:
            raise (e)

    def post_ai_score(self, ai_score_content):
        try:
            r = requests.post(f'{self.endpoint}api/AiScore',
                              json=ai_score_content, headers=self.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)
#APIService().setEndpoint_new('dev', 100003)