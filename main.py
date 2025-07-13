#!/usr/bin/python3
"""
This script calculates the average time from creation
to merge of all merged pull requests in a repository.

"""
import github
import time
from github import Github, Auth
from prometheus_client import start_http_server, Gauge

time_chc = Gauge('time_chc', 'Average time to merge of cloud-helm-charts repo')
time_cdi = Gauge('time_cdi', 'Average time to merge of cloud-docker-images repo')
time_cda = Gauge('time_cda', 'Average time to merge of cloud-deployed-apps repo')
time_sou = Gauge('time_sou', 'Average time to merge of SCD-OpenStack-Utils repo')
time_scp = Gauge('time_chc', 'Average time to merge of st2-cloud-pack repo')
time_ccv = Gauge('time_chc', 'Average time to merge of cloud-capi-values repo')

def merge_date(pr: github.Github):
    """
    find date that pull request was merged at
    :param pr: pull request object
    """
    merged = pr.merged_at
    return merged

def create_date(pr: github.Github):
    """
    find date that pull request was created at
    :param pr: pull request object
    """
    created = pr.created_at
    return created

def average_time(prs, repo):
    """
    calculate average time that pull requests
    were merged by (in seconds)
    :param prs: list of pull request objects
    """
    diff = []
    for pull_request in prs:
        if pull_request.merged:
            md = merge_date(pull_request)
            cd = create_date(pull_request)
            diff.append((md - cd).total_seconds())

            print(f'{repo}: {pull_request.number})

    total = 0
    for num in diff:
        total += num
    total /= len(diff)

    return total

if __name__ == '__main__':

    start_http_server(8000)

    auth = Auth.Token("PERSONAL_ACCESS_TOKEN")
    g = Github(auth=auth)
    user = g.get_user("stfc")
    repos = [
        'cloud-helm-charts',
        'cloud-docker-images',
        'cloud-deployed-apps',
        'SCD-OpenStack-Utils',
        'st2-cloud-pack'
        'cloud-capi-values'
    ]

    while True:
        for repo in repos:
            r = g.get_repo(f"stfc/{repo}")
            prs = r.get_pulls(state="all")
            time_sec = average_time(prs, repo)
            if repo == repos[0]:
                time_chc.set(time_sec)
            elif repo == repos[1]:
                time_cdi.set(time_sec)
            elif repo == repos[2]:
                time_cda.set(time_sec)
            elif repo == repos[3]:
                time_sou.set(time_sec)
            elif repo == repos[4]:
                time_scp.set(time_sec)
            elif repo == repos[5]:
                time_ccv.set(time_sec)
            print(f'average time from creation to merge of {repo} repository: 
            {time_sec} seconds')

            # g.close()
