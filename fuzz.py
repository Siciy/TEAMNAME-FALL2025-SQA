'''
Fuzz Testing for MLForensics Project
Software Quality Assurance - COMP 5710/6710
Author: Kabro
Date: November 17, 2025

This script performs automated fuzzing on 5 critical Python methods 
from the MLForensics project to discover potential bugs and edge cases.
'''

import sys
import os
import random
import string
import traceback
from datetime import datetime

# Add the MLForensics modules to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MLForensics', 'MLForensics-farzana', 'FAME-ML'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MLForensics', 'MLForensics-farzana', 'mining'))

import main
import mining

# Test results storage
test_results = {
    'passed': 0,
    'failed': 0,
    'bugs_found': []
}

def generate_random_string(length=10):
    """Generate random string for fuzzing"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_list(size=5):
    """Generate random list with mixed types"""
    types = [
        lambda: random.randint(-1000, 1000),
        lambda: random.uniform(-1000.0, 1000.0),
        lambda: generate_random_string(),
        lambda: None,
        lambda: [],
        lambda: {},
    ]
    return [random.choice(types)() for _ in range(size)]

def log_result(test_name, success, error_msg=""):
    """Log test results"""
    if success:
        test_results['passed'] += 1
        print(f"✓ {test_name} - PASSED")
    else:
        test_results['failed'] += 1
        test_results['bugs_found'].append({
            'test': test_name,
            'error': error_msg
        })
        print(f"✗ {test_name} - FAILED: {error_msg}")

# ============================================
# FUZZ TEST 1: giveTimeStamp() from main.py
# ============================================
def fuzz_giveTimeStamp():
    """
    Test the giveTimeStamp function with various scenarios
    """
    print("\n[TEST 1] Fuzzing main.giveTimeStamp()")
    
    # Test 1.1: Normal execution
    try:
        result = main.giveTimeStamp()
        assert isinstance(result, str), "Return value should be a string"
        assert len(result) > 0, "Timestamp should not be empty"
        log_result("giveTimeStamp - Normal execution", True)
    except Exception as e:
        log_result("giveTimeStamp - Normal execution", False, str(e))
    
    # Test 1.2: Multiple rapid calls (stress test)
    try:
        timestamps = [main.giveTimeStamp() for _ in range(100)]
        assert len(timestamps) == 100, "Should generate 100 timestamps"
        assert len(set(timestamps)) >= 1, "Timestamps should be generated"
        log_result("giveTimeStamp - Rapid calls", True)
    except Exception as e:
        log_result("giveTimeStamp - Rapid calls", False, str(e))

# ============================================
# FUZZ TEST 2: makeChunks() from mining.py
# ============================================
def fuzz_makeChunks():
    """
    Test the makeChunks function with various input combinations
    """
    print("\n[TEST 2] Fuzzing mining.makeChunks()")
    
    # Test 2.1: Normal list with positive chunk size
    try:
        result = list(mining.makeChunks([1, 2, 3, 4, 5], 2))
        assert len(result) == 3, "Should create 3 chunks"
        log_result("makeChunks - Normal list", True)
    except Exception as e:
        log_result("makeChunks - Normal list", False, str(e))
    
    # Test 2.2: Empty list
    try:
        result = list(mining.makeChunks([], 5))
        assert len(result) == 0, "Empty list should yield no chunks"
        log_result("makeChunks - Empty list", True)
    except Exception as e:
        log_result("makeChunks - Empty list", False, str(e))
    
    # Test 2.3: Chunk size larger than list
    try:
        result = list(mining.makeChunks([1, 2, 3], 10))
        assert len(result) == 1, "Should create 1 chunk"
        log_result("makeChunks - Large chunk size", True)
    except Exception as e:
        log_result("makeChunks - Large chunk size", False, str(e))
    
    # Test 2.4: Chunk size of 1
    try:
        test_list = [1, 2, 3]
        result = list(mining.makeChunks(test_list, 1))
        assert len(result) == len(test_list), "Each element should be its own chunk"
        log_result("makeChunks - Chunk size 1", True)
    except Exception as e:
        log_result("makeChunks - Chunk size 1", False, str(e))
    
    # Test 2.5: Zero or negative chunk size (edge case - should fail gracefully)
    try:
        result = list(mining.makeChunks([1, 2, 3], 0))
        log_result("makeChunks - Zero chunk size", False, "Should raise error for chunk size 0")
    except (ValueError, ZeroDivisionError) as e:
        log_result("makeChunks - Zero chunk size handles error", True)
    except Exception as e:
        log_result("makeChunks - Zero chunk size", False, f"Unexpected error: {str(e)}")

# ============================================
# FUZZ TEST 3: dumpContentIntoFile() from mining.py
# ============================================
def fuzz_dumpContentIntoFile():
    """
    Test the dumpContentIntoFile function with various inputs
    """
    print("\n[TEST 3] Fuzzing mining.dumpContentIntoFile()")
    
    # Test 3.1: Normal string content
    try:
        test_file = "test_output_normal.txt"
        content = "This is a test content"
        result = mining.dumpContentIntoFile(content, test_file)
        assert os.path.exists(test_file), "File should be created"
        assert int(result) > 0, "File size should be positive"
        os.remove(test_file)  # Cleanup
        log_result("dumpContentIntoFile - Normal string", True)
    except Exception as e:
        log_result("dumpContentIntoFile - Normal string", False, str(e))
    
    # Test 3.2: Empty string
    try:
        test_file = "test_output_empty.txt"
        result = mining.dumpContentIntoFile("", test_file)
        assert os.path.exists(test_file), "File should be created even with empty content"
        os.remove(test_file)  # Cleanup
        log_result("dumpContentIntoFile - Empty string", True)
    except Exception as e:
        log_result("dumpContentIntoFile - Empty string", False, str(e))
    
    # Test 3.3: Large content
    try:
        test_file = "test_output_large.txt"
        large_content = "X" * 100000  # 100K characters
        result = mining.dumpContentIntoFile(large_content, test_file)
        assert int(result) >= 100000, "File size should match content"
        os.remove(test_file)  # Cleanup
        log_result("dumpContentIntoFile - Large content", True)
    except Exception as e:
        log_result("dumpContentIntoFile - Large content", False, str(e))
    
    # Test 3.4: Special characters
    try:
        test_file = "test_output_special.txt"
        special_content = "!@#$%^&*()_+-=[]{}|;':\",./<>?\\n\\t"
        result = mining.dumpContentIntoFile(special_content, test_file)
        assert os.path.exists(test_file), "File should handle special characters"
        os.remove(test_file)  # Cleanup
        log_result("dumpContentIntoFile - Special characters", True)
    except Exception as e:
        log_result("dumpContentIntoFile - Special characters", False, str(e))

# ============================================
# FUZZ TEST 4: deleteRepo() from mining.py
# ============================================
def fuzz_deleteRepo():
    """
    Test the deleteRepo function with various scenarios
    """
    print("\n[TEST 4] Fuzzing mining.deleteRepo()")
    
    # Test 4.1: Delete existing directory
    try:
        test_dir = "test_repo_to_delete"
        os.makedirs(test_dir, exist_ok=True)
        mining.deleteRepo(test_dir, "test")
        assert not os.path.exists(test_dir), "Directory should be deleted"
        log_result("deleteRepo - Existing directory", True)
    except Exception as e:
        log_result("deleteRepo - Existing directory", False, str(e))
    
    # Test 4.2: Delete non-existent directory (should not crash)
    try:
        mining.deleteRepo("non_existent_dir_12345", "test")
        log_result("deleteRepo - Non-existent directory", True)
    except Exception as e:
        log_result("deleteRepo - Non-existent directory", False, str(e))
    
    # Test 4.3: Delete directory with files
    try:
        test_dir = "test_repo_with_files"
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, "test.txt"), 'w') as f:
            f.write("test content")
        mining.deleteRepo(test_dir, "test")
        assert not os.path.exists(test_dir), "Directory with files should be deleted"
        log_result("deleteRepo - Directory with files", True)
    except Exception as e:
        log_result("deleteRepo - Directory with files", False, str(e))

# ============================================
# FUZZ TEST 5: giveTimeStamp() from mining.py
# ============================================
def fuzz_mining_giveTimeStamp():
    """
    Test the mining module's giveTimeStamp function
    """
    print("\n[TEST 5] Fuzzing mining.giveTimeStamp()")
    
    # Test 5.1: Normal execution
    try:
        result = mining.giveTimeStamp()
        assert isinstance(result, str), "Return value should be a string"
        assert len(result) > 0, "Timestamp should not be empty"
        log_result("mining.giveTimeStamp - Normal execution", True)
    except Exception as e:
        log_result("mining.giveTimeStamp - Normal execution", False, str(e))
    
    # Test 5.2: Format validation
    try:
        result = mining.giveTimeStamp()
        # Expected format: 'YYYY-MM-DD HH:MM:SS'
        parts = result.split(' ')
        assert len(parts) == 2, "Should have date and time parts"
        date_parts = parts[0].split('-')
        assert len(date_parts) == 3, "Date should have year, month, day"
        log_result("mining.giveTimeStamp - Format validation", True)
    except Exception as e:
        log_result("mining.giveTimeStamp - Format validation", False, str(e))
    
    # Test 5.3: Consistency check
    try:
        results = [mining.giveTimeStamp() for _ in range(10)]
        assert len(results) == 10, "Should generate 10 timestamps"
        # All timestamps should be in the same general timeframe
        assert all(isinstance(r, str) for r in results), "All results should be strings"
        log_result("mining.giveTimeStamp - Consistency check", True)
    except Exception as e:
        log_result("mining.giveTimeStamp - Consistency check", False, str(e))

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("FUZZING TEST SUMMARY")
    print("="*60)
    print(f"Total Tests Passed: {test_results['passed']}")
    print(f"Total Tests Failed: {test_results['failed']}")
    print(f"Total Bugs Found: {len(test_results['bugs_found'])}")
    
    if test_results['bugs_found']:
        print("\n" + "-"*60)
        print("BUGS DISCOVERED:")
        print("-"*60)
        for i, bug in enumerate(test_results['bugs_found'], 1):
            print(f"\n{i}. Test: {bug['test']}")
            print(f"   Error: {bug['error']}")
    else:
        print("\n✓ No bugs discovered! All tests passed.")
    
    print("\n" + "="*60)
    
    # Save results to file
    with open('fuzz_results.txt', 'w') as f:
        f.write(f"Fuzzing Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n")
        f.write(f"Passed: {test_results['passed']}\n")
        f.write(f"Failed: {test_results['failed']}\n")
        f.write(f"Bugs Found: {len(test_results['bugs_found'])}\n\n")
        
        if test_results['bugs_found']:
            f.write("Bugs Discovered:\n")
            for i, bug in enumerate(test_results['bugs_found'], 1):
                f.write(f"\n{i}. {bug['test']}\n")
                f.write(f"   {bug['error']}\n")

if __name__ == "__main__":
    print("="*60)
    print("MLForensics Fuzzing Test Suite")
    print("Software Quality Assurance - COMP 5710/6710")
    print("="*60)
    
    # Run all fuzz tests
    fuzz_giveTimeStamp()
    fuzz_makeChunks()
    fuzz_dumpContentIntoFile()
    fuzz_deleteRepo()
    fuzz_mining_giveTimeStamp()
    
    # Print summary
    print_summary()
