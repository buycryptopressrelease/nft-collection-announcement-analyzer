#!/usr/bin/env node
"use strict";
process.exitCode = require("./analyzer.js").main(process.argv.slice(2));
