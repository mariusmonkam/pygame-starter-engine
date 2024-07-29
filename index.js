#!/usr/bin/env node

const { execSync, spawn } = require("child_process");

// Ensure Pipenv is installed
execSync("pip install pipenv", { stdio: "inherit" });

// Install dependencies using Pipenv
execSync("pipenv install", { stdio: "inherit" });

// Path to your Python script
const pythonScriptPath = "scripts/main.py";

// Spawn a new Python process with Pipenv
const pythonProcess = spawn("pipenv", ["run", "python", pythonScriptPath]);

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
