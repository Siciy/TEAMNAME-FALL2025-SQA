# TEAM-FALL2025-SQA

## Team Information

**Team Name:** TEAM-FALL2025-SQA

**Team Members:**
- Kabro (Team Lead)

## Project Description

This repository contains the Software Quality Assurance (SQA) project for COMP 5710/6710. The objective is to integrate software quality assurance activities into the MLForensics Python project.

## Project Structure

```
MLForensics/
├── MLForensics-farzana/
│   ├── FAME-ML/          # Main ML forensics analysis code
│   ├── mining/           # Git repository mining tools
│   └── empirical/        # Dataset statistics and reporting
├── fuzz.py               # Automated fuzzing tests
├── .github/
│   └── workflows/
│       └── ci.yml        # Continuous Integration configuration
└── SQA-REPO.md          # Project report and lessons learned
```

## SQA Activities Completed

1. ✅ **Repository Setup**: Project uploaded to GitHub
2. ✅ **Fuzzing**: Implemented automated fuzzing for 5 Python methods
3. ✅ **Forensics/Logging**: Added logging statements to 5 Python methods
4. ✅ **Continuous Integration**: Set up GitHub Actions for automated testing

## Running the Project

### Install Dependencies
```bash
pip install pandas numpy gitpython
```

### Run Fuzzing Tests
```bash
python fuzz.py
```

### Run Main Analysis
```bash
cd MLForensics/MLForensics-farzana/FAME-ML
python main.py
```

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow automatically:
- Runs fuzzing tests on every push and pull request
- Validates code quality
- Reports test results

See `.github/workflows/ci.yml` for configuration details.

## License

This project is for educational purposes as part of COMP 5710/6710 coursework.
