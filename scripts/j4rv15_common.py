#!/usr/bin/env python3
"""
J4RV15 Common Utilities
Shared functions and constants used across J4RV15 scripts
Version: 1.0.0
"""

import os
import stat
from pathlib import Path
from typing import List, Tuple


# =====================================================
# SHARED CONSTANTS
# =====================================================

J4RV15_ROOT = Path.home() / ".J.4.R.V.1.5"
SECRETS_DIR_NAME = "60_secrets"

# Standard permissions
SECURE_DIR_PERMS = 0o700
SECURE_FILE_PERMS = 0o600
STANDARD_DIR_PERMS = 0o755
STANDARD_FILE_PERMS = 0o644


# =====================================================
# SHARED UTILITY FUNCTIONS
# =====================================================

def get_secrets_path(base_path: Path = None) -> Path:
    """
    Get the path to the secrets directory.
    
    Args:
        base_path: Optional base path. If None, uses J4RV15_ROOT
        
    Returns:
        Path to the secrets directory
    """
    if base_path is None:
        base_path = J4RV15_ROOT
    return base_path / SECRETS_DIR_NAME


def normalize_permissions(root_path: Path, 
                          dir_perms: int = SECURE_DIR_PERMS,
                          file_perms: int = SECURE_FILE_PERMS,
                          skip_symlinks: bool = True) -> List[str]:
    """
    Normalize permissions for all files and directories in a tree.
    
    Args:
        root_path: Root directory to normalize
        dir_perms: Permissions to set on directories (default: 0o700)
        file_perms: Permissions to set on files (default: 0o600)
        skip_symlinks: Whether to skip symbolic links (default: True)
        
    Returns:
        List of paths that were modified
    """
    if not root_path.exists():
        return []
    
    normalized_items = []
    
    for root, dirs, files in os.walk(root_path):
        # Normalize directory permissions
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if skip_symlinks and dir_path.is_symlink():
                continue
                
            current_perms = stat.S_IMODE(dir_path.stat().st_mode)
            if current_perms != dir_perms:
                dir_path.chmod(dir_perms)
                normalized_items.append(str(dir_path))
        
        # Normalize file permissions
        for file_name in files:
            file_path = Path(root) / file_name
            if skip_symlinks and file_path.is_symlink():
                continue
                
            current_perms = stat.S_IMODE(file_path.stat().st_mode)
            if current_perms != file_perms:
                file_path.chmod(file_perms)
                normalized_items.append(str(file_path))
    
    return normalized_items


def check_incorrect_permissions(root_path: Path,
                                expected_dir_perms: int = SECURE_DIR_PERMS,
                                expected_file_perms: int = SECURE_FILE_PERMS,
                                skip_symlinks: bool = True) -> Tuple[List[str], List[str]]:
    """
    Check for files and directories with incorrect permissions.
    
    Args:
        root_path: Root directory to check
        expected_dir_perms: Expected permissions for directories (default: 0o700)
        expected_file_perms: Expected permissions for files (default: 0o600)
        skip_symlinks: Whether to skip symbolic links (default: True)
        
    Returns:
        Tuple of (incorrect_dirs, incorrect_files)
    """
    if not root_path.exists():
        return [], []
    
    incorrect_dirs = []
    incorrect_files = []
    
    for root, dirs, files in os.walk(root_path):
        # Check directory permissions
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if skip_symlinks and dir_path.is_symlink():
                continue
                
            current_perms = stat.S_IMODE(dir_path.stat().st_mode)
            if current_perms != expected_dir_perms:
                incorrect_dirs.append(str(dir_path))
        
        # Check file permissions
        for file_name in files:
            file_path = Path(root) / file_name
            if skip_symlinks and file_path.is_symlink():
                continue
                
            current_perms = stat.S_IMODE(file_path.stat().st_mode)
            if current_perms != expected_file_perms:
                incorrect_files.append(str(file_path))
    
    return incorrect_dirs, incorrect_files
