#!/usr/bin/env node

// index.js
const { spawn } = require("child_process");

// Path to your Python script
const pythonScriptPath = "scripts/main.py";

// Spawn a new Python process
const pythonProcess = spawn("python", [pythonScriptPath]);

// Capture stdout from the Python script
pythonProcess.stdout.on("data", (data) => {
  console.log(`stdout: ${data}`);
});

// Capture stderr from the Python script
pythonProcess.stderr.on("data", (data) => {
  console.error(`stderr: ${data}`);
});

// Capture exit code from the Python script
pythonProcess.on("close", (code) => {
  console.log(`Python script exited with code ${code}`);
});
