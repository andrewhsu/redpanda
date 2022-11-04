#!/usr/bin/env python3
import argparse
import json
import logging
import os
import re
import sys

# lint error code to error message
LINT_BODY_ERR = {
    'B01': '`## Cover Letter` section missing contents',
    'B02': 'PR to dev branch `## Backports Required` section missing contents',
    'B03': '`## Release Notes` section missing list of branches or `none`',
}

# lint section to python regex group name
LINT_SEC_GN = {
    'Cover Letter': 'cl',
    'Backports Required': 'bp',
    'UX Changes': 'ux',
    'Release Notes': 'rel'
}


def has_label(j, l):
    if 'labels' in j:
        for label in j['labels']:
            if label['name'] == l:
                return True
    return False


def get_section(j, s):
    if 'body' not in j:
        return ''

    # extract body without html comments
    pr_body = re.sub(r'(<!--.*?-->)', '', j['body'], flags=re.DOTALL)

    # remove carriage return chars
    pr_body = re.sub(r'\r', r'', pr_body)

    # reduce whitespace
    pr_body = re.sub(r'\n\s*\n', r'\n', pr_body)

    # remove leading whitespace
    pr_body = re.sub(r'^\s+', r'', pr_body)

    # remove trailing whitespace
    pr_body = re.sub(r'\s+$', r'', pr_body)

    pattern = r'^##[ ]*%s\s*([\W\w]*?)(\Z|^##[^#\n]+)' % s
    m = re.search(pattern, pr_body, flags=re.MULTILINE | re.DOTALL | re.I)
    if m is None:
        return ''
    return m.group(1)


def lint_cl(j):
    # return re.search(r'^Backport of PR ', s) is not None
    s = get_section(j, 'Cover Letter')
    print("aaa" + s + "bbb")

    # check if old default was left untouched
    if s == 'Describe in plain language the motivation (bug, feature, etc.) behind the change in this PR and how the included commits address it.\nFixes #ISSUE-NUMBER, Fixes #ISSUE-NUMBER, ...':
        return ['B01']

    if s == '':
        return ['B01']

    return []


def lint_bp(j):
    if j['baseRefName'] == 'dev':
        s = get_section(j, 'Backports Required')
        if s == '':
            return ['B02']
    return []


def lint_ux(j):
    return []


def lint_rel(j):
    if has_label(j, 'kind/backport'):
        return []
    s = get_section(j, 'Release Notes')
    if s == '* none':
        return []
    if re.match(r'^### ', s):
        return []
    return ['B03']


def lint_pr_body(j):
    """Lint the PR body.

    Simple validation of the PR body. Returns list of strings that are
    the error code keys for LINT_BODY_ERR.

    Keyword arguments:
    j -- JSON object of GitHub API call to get PR details
    """
    errs = []
    for func in (lint_cl, lint_bp, lint_ux, lint_rel):
        errs += func(j)
    return errs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Lint PR body release notes for redpanda')
    parser.add_argument('pr_filename', help='json filename of the pr, e.g. pr-999123.json')
    parser.add_argument('--log-level',
                        default='INFO',
                        help='verbosity of log messages, e.g. DEBUG')
    args = parser.parse_args()
    logging.basicConfig(
        level=args.log_level,
        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')

    errs = []
    with open(args.pr_filename) as f:
        j = json.load(f)
        errs = lint_pr_body(j)

    if len(errs) > 0:
        for err in errs:
            logging.error('%s:%s' % (err, LINT_BODY_ERR[err]))
        exit(1)
