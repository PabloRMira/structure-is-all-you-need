#!/bin/bash

set -eu

pixi run pre-commit-install
pixi run pre-commit-run
