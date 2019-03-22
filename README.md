# docker-builder

A simple tool to build Docker images.

In some cases you need to build different variations of the same Docker image. For instance, you may want to test a JEE application with different JDKs and application servers versions: in this case you can configure your build using a yaml file and build/tag all the variants automatically.

```
name: my-registry:5000/lorenzobenvenuti/wildlfy
dir: /path/to/dockerfile/dir
images:
  - name: 9.0.2
    tags:
      - 9.0.2.Final-jdk8u112
      - 9.0.2.Final-jdk8
      - 9-jdk8
      - 9
    args:
      JDK_VERSION: 8u112
      WILDFLY_VERSION: 9.0.2.Final
  - name: 10.1.0
    tags:
      - 10.1.0.Final-jdk8u112
      - 10-jdk8
      - 10.1.0.Final-jdk8
      - 10
    args:
      JDK_VERSION: 8u112
      WILDFLY_VERSION: 10.1.0.Final
```

```bash
$ docker-builder.py build wildfly.yaml
```

To push the images:

```bash
$ docker-builder.py push wildfly.yaml
```

You can specify different build directories using a `dir` entry for each image.
You can specify which images to build using the `--image`/`-i` option.
