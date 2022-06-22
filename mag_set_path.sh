#!/bin/bash

touch .maginit_personal

echo "$PWD/magic_layout/skywater130_microtemplates_dense" | tee .maginit_personal
echo "$PWD/magic_layout/logic_generated" >> .maginit_personal
