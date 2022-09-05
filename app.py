#!/usr/bin/env python3
from aws_cdk import core
from stacks.restApi_stack import RestApiStack
app = core.App()
restApiStack = RestApiStack(app,'RestApiStack')
app.synth()