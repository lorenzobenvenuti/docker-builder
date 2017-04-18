#!/usr/bin/env python

import argparse
import yaml
import docker
import json
import sys


def to_str_dictionary(d):
    if d is None:
        return {}
    return {k: str(v) for k, v in d.items()}


def build(name, directory, images):
    client = docker.from_env(version='auto')
    for image in images:
        tags = image['tags']
        main_tag = "{}:{}".format(name, tags[0])
        curr_dir = image.get('dir', None) or directory
        build_args = image.get('args', None)
        print "Building image {}".format(main_tag)
        img = client.images.build(path=curr_dir,
                                  tag=main_tag,
                                  buildargs=to_str_dictionary(build_args),
                                  rm=True)
        for tag in tags[1:]:
            print "Tagging image {} -> {}".format(main_tag, tag)
            img.tag(name, tag)


def push(name, images):
    client = docker.from_env(version='auto')
    for image in images:
        for tag in image['tags']:
            print "Pushing image {}:{}".format(name, tag)
            client.images.push("{}:{}".format(name, tag))


def filter_images(images, selected):
    if not selected:
        return images
    return [i for i in images if i['name'] in selected]


def build_images(args):
    for curr_file in args.file:
        with open(curr_file, 'r') as yaml_file:
            data = yaml.load(yaml_file.read())
            build(data['name'], data.get('dir', None),
                  filter_images(data['images'], args.image))


def push_images(args):
    for curr_file in args.file:
        with open(curr_file, 'r') as yaml_file:
            data = yaml.load(yaml_file.read())
            push(data['name'], filter_images(data['images'], args.image))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A tool for building docker images'
    )
    subparsers = parser.add_subparsers()
    parser_build = subparsers.add_parser('build', help='Builds images')
    parser_build.add_argument('file', nargs='+', help='Configuration file')
    parser_build.add_argument('--image', '-i', action='append',
                              help='Selects images to build')
    parser_build.set_defaults(func=build_images)
    parser_push = subparsers.add_parser('push', help='Push images')
    parser_push.add_argument('file', nargs='+', help='Configuration file')
    parser_push.add_argument('--image', '-i', action='append',
                             help='Selects images to push')
    parser_push.set_defaults(func=push_images)
    args = parser.parse_args()
    args.func(args)
