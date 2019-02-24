## 
##    python find_big_image.py --checklist_file "checklist.txt" --whitelist_file "whitelist.txt"
##
## checklist.txt
##              # oracle should not exceed 100 MB
##              oracle.*:100
##              # any image should not exceed 200 MB
##              .*:200
##
## whitelist.txt:
##              egaraev/cryptobot.*
##              .*<none>.*
##              .*shit.*
##              
#!/usr/bin/python
from contextlib import contextmanager
import sys, os
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
import pip
required_pkgs = ['docker', 'argparse']
installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]

for package in required_pkgs:
    if package not in installed_pkgs:
        with suppress_stdout():
            pip.main(['install', package])

import re
import argparse
import docker




def show_tags(client):
    tags = []
    for image in client.images.list():
        for tag in image.tags:
            tags.append(tag)
    return tags


def skip_whitelist(item_list, whitelist_file):
    ret_list = []
    skip_list = []
    with open(whitelist_file,'r') as f:
        for row in f:
            row = row.strip()
            if row == "" or row.startswith('#'):
                continue
            skip_list.append(row)
    for item in item_list:
        should_skip = False
        for skip_rule in skip_list:
            if re.search(skip_rule, item):
                should_skip = True
                print("Skip check for %s" % (item))
                break
        if should_skip is False:
            ret_list.append(item)
    return ret_list

def show_images(tags, client):
    print("Show image status:")
    print("{0:40} {1}".format("IMAGE_TAG", "SIZE"))
    for tag_name in tags:
        size_mb = list_img_size(tag_name, client)
        print("{0:40} {1}MB".format(tag_name, size_mb))


def list_img_size(tag_name, client):
    image = client.images.get(tag_name)
    size_mb = float(image.attrs['Size'])/(1024*1024)
    return round(size_mb, 2)


def check_docker_images(checklist_file, whitelist_file, client):
    huge_images_list = []
    tags = show_tags(client)
    tags = skip_whitelist(tags, whitelist_file)

    checklist = []
    with open(checklist_file,'r') as f:
        for row in f:
            row = row.strip()
            if row == "" or row.startswith('#'):
                continue
            checklist.append(row)
    for tag_name in tags:
        has_matched = False
        for check_rule in checklist:
            i = check_rule.split(":")
            tag_name_pattern = ".".join(i[0:-1])
            max_size_mb = float(i[-1])
            if re.search(tag_name_pattern, tag_name):
                has_matched = True
                image_size_mb = list_img_size(tag_name, client)
                if image_size_mb > max_size_mb:
                    huge_images_list.append(tag_name)
                break
    return huge_images_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checklist_file', required=True, type=str)
    parser.add_argument('--whitelist_file', required=True, type=str)

    i = parser.parse_args()
    checklist_file = i.checklist_file
    whitelist_file = i.whitelist_file

    client = docker.from_env()
    huge_images_list = check_docker_images(checklist_file, whitelist_file, client)
    if len(huge_images_list) == 0:
        print("OK: all docker images are not so big")
    else:
        print("Those are big images")
        show_images(huge_images_list, client)
        sys.exit(1)