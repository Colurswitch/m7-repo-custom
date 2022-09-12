#!/usr/bin/python

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, HTTPError
import json
import re
import argparse
import sys

URL= "https://github.com"
APIURL= "https://api.github.com/repos"
RAWURL = "https://raw.githubusercontent.com"

MASTERBRANCH = "/branches/master"


##
#  get master branch sha
#
def getSha(repo_path):

    url = APIURL + repo_path + MASTERBRANCH

    try:

        if sys.version_info >= (3, 0):
            content= urlopen(url)
            data = content.read()
            encoding = content.info().get_content_charset('utf-8')
            JSON_object = json.loads(data.decode(encoding))
            return JSON_object['commit']['sha']
        else:
            data = json.load(urlopen(url))
            return data['commit']['sha']

    except:
        return False


##
#  return repo path and strips returns
#
def repoPath(url):
    return url.replace(URL, '').replace('\n','').replace('\r','')



##
#  get plugin.json
#
def getPluginJson(repo_path, sha):

    url = RAWURL + repo_path + "/" + sha + "/plugin.json"

    try:

        if sys.version_info >= (3, 0):
            content= urlopen(url)
            data = content.read()
            encoding = content.info().get_content_charset('utf-8')
            JSON_object = json.loads(data.decode(encoding))
            return JSON_object
        else:
            data = json.load(urlopen(url))
            return data
    except:
       return False


##
#  get icon url
#
def getIcon(repo_path, sha, icon_name):
    return RAWURL + repo_path + "/" + sha + "/" + icon_name


##
#  The main function
#
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="name of file with a list of git repositories")
    parser.add_argument("-t", "--title", help="Title")
    parser.add_argument("-o", "--outputfile", help="Name of output file")
    args = parser.parse_args()

    if (not args.inputfile and not args.outputfile):
        parser.print_help()
        parser.exit(1)

    res = {u"version": 1, u"plugins": []}

    if args.title:
        res[u"title"] = args.title

    print ("Opening " + args.inputfile)
    file = open(args.inputfile, "r") 

    for line in file: 

        print ("Searching for plugin in " + line)

        repo_path = repoPath(line)
        sha = getSha(repo_path)

        if sha == False:
            print ("could not find plugin")
        else :
            print ("Getting plugin.json file")
            plugin_json = getPluginJson(repo_path,sha)

            print ("Setting downloadUrl")
            plugin_json['downloadURL']= URL + repo_path + "/archive/" + sha + ".zip"
            print ("Setting icon")
            plugin_json['icon']= getIcon(repo_path, sha, plugin_json['icon'])

            res['plugins'].append(plugin_json)

    print ("Writing " + args.outputfile)
    with open(args.outputfile, "w") as write_file:
        json.dump(res, write_file)

    print ("Done")

if __name__== "__main__":
    main()

