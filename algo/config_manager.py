import logging
from datetime import datetime

import xml.etree.ElementTree as ET
import xml.dom.minidom as dom

from definitions import ALGO_CONFIG
from constants import ApiKeys as k

_logger = logging.getLogger("config_manager")


def create_config_file(username: str, password: str):
    config = ET.Element(k.key_config)
    credentials = ET.SubElement(config, k.key_credentials)
    login_id = ET.SubElement(credentials, k.key_login_id)
    login_password = ET.SubElement(credentials, k.key_password)
    login_id.text = username
    login_password.text = password
    _logger.debug("Added Credentials")

    api = ET.SubElement(config, k.key_api)
    unique_id = ET.SubElement(api, k.key_unique_id)
    ref_no = ET.SubElement(api, k.key_ref_no)
    modified = ET.SubElement(api, k.key_modified)
    modified.text = datetime.now().isoformat()
    _logger.debug("Added: %s %s" % (unique_id, ref_no))

    data = dom.parseString(ET.tostring(config, encoding='unicode'))
    xml = data.toprettyxml()
    f = open(ALGO_CONFIG, 'w')
    f.write(xml)
    f.close()


def set_api_credentials(unique_id, ref_no):
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    try:
        api = root.find(k.key_api)
        api_id = api.find(k.key_unique_id)
        api_id.text = str(unique_id)
        api_ref_no = api.find(k.key_ref_no)
        api_ref_no.text = str(ref_no)
        api_modified = api.find(k.key_modified)
        api_modified.text = datetime.now().isoformat()
    except (AttributeError, ET.ParseError) as e:
        print("Unable to configure API credentials")
        print("Error: %s" % e)
    tree.write(ALGO_CONFIG)
    get_api_credentials()


def get_api_credentials():
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    api = root.find(k.key_api)
    unique_id = api.find(k.key_unique_id).text
    ref_no = api.find(k.key_ref_no).text
    modified = api.find(k.key_modified).text
    # print(unique_id, ref_no, modified)
    return unique_id, ref_no, modified


def get_credentials():
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    credentials = root.find(k.key_credentials)
    login_id = credentials[0].text
    login_password = credentials[1].text
    return login_id, login_password


if __name__ == '__main__':
    create_config_file("8288024014", "a@8888888888")
    # get_credentials()
    # set_api_credentials(97, "avsdfsv")
