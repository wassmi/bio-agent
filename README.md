
BioAgent - Bioinformatics Workflow Assistant

BioAgent is a specialized bioinformatics AI system designed for high-throughput computational biology workflows. It provides intelligent automation and analysis capabilities for common bioinformatics tasks.

CORE CAPABILITIES

1. File Analysis
   * Deep understanding of bioinformatics file formats (.fastq, .bam, .vcf, .bed, etc.)
   * Automatic quality assessment and validation
   * Format-specific integrity checks
   * Metadata extraction and validation

2. Workflow Intelligence
   * Dynamic pipeline construction
   * Resource requirement estimation
   * Dependency resolution
   * Parallel processing optimization
   * Checkpoint/resume capabilities

3. Code Generation Standards
   * Production-grade Python code generation
   * Comprehensive error handling and recovery
   * Memory-efficient processing
   * Progress monitoring and logging
   * Resource cleanup
   * Standardized output organization

INSTALLATION

1. Clone the repository
2. Install dependencies using: pip install -r requirements.txt

CONFIGURATION

Environment Setup:
1. Create a .env file in the root directory
2. Add your GROQ API key: GROQ_API_KEY=your_api_key_here

COMMAND LINE INTERFACE

Usage: python src/main.py --run "command" file

Arguments:
--run: Specifies the analysis command to execute
file: Path to the input file for analysis

Example: python src/main.py --run "perform quality control" data/sample.fastq

OUTPUT STRUCTURE

Results are organized in timestamped directories:
bioagent_results_YYYYMMDD_HHMMSS/
- generated_script.py
- analysis_results/
- execution_logs/

LOGGING

The system maintains detailed logs:
- Timestamp-based log files
- Console output with rich formatting
- Progress indicators
- Error tracking

DEPENDENCIES MANAGEMENT

FastQC Integration:
- Automatically checks for FastQC installation
- Supports both system-wide and bundled installations
- Provides clear installation instructions if needed

Python Dependencies:
- langchain_groq
- rich
- pydantic
- black
- python-dotenv

