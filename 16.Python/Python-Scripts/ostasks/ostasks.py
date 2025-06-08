#!/usr/bin/python3
import os
import pwd
import grp
import subprocess
import logging
import sys
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_root():
    """Check if script is running with root privileges."""
    return os.geteuid() == 0

def user_exists(username):
    """Check if a user exists using pwd module."""
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def group_exists(groupname):
    """Check if a group exists using grp module."""
    try:
        grp.getgrnam(groupname)
        return True
    except KeyError:
        return False

def create_user(username):
    """Create a new user using subprocess."""
    try:
        subprocess.run(['useradd', username], check=True)
        logger.info(f"User {username} created successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create user {username}: {e}")
        raise

def create_group(groupname):
    """Create a new group using subprocess."""
    try:
        subprocess.run(['groupadd', groupname], check=True)
        logger.info(f"Group {groupname} created successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create group {groupname}: {e}")
        raise

def add_user_to_group(username, groupname):
    """Add user to a group using subprocess."""
    try:
        subprocess.run(['usermod', '-G', groupname, username], check=True)
        logger.info(f"Added user {username} to group {groupname}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add user {username} to group {groupname}: {e}")
        raise

def main():
    """Main function to handle user and group management."""
    if not is_root():
        logger.error("This script must be run as root")
        sys.exit(1)

    userlist = ["alpha", "beta", "gamma"]
    science_group = "science"
    science_dir = "/opt/science_dir"

    logger.info("Starting user management operations")

    # Process users
    for user in userlist:
        if user_exists(user):
            logger.info(f"User {user} already exists, skipping creation")
        else:
            logger.info(f"Creating user {user}")
            create_user(user)

    # Process science group
    if group_exists(science_group):
        logger.info(f"Group {science_group} already exists, skipping creation")
    else:
        logger.info(f"Creating group {science_group}")
        create_group(science_group)

    # Add users to science group
    for user in userlist:
        add_user_to_group(user, science_group)

    # Create and set up science directory
    if os.path.isdir(science_dir):
        logger.info(f"Directory {science_dir} already exists")
    else:
        logger.info(f"Creating directory {science_dir}")
        os.makedirs(science_dir, mode=0o770)

    # Set ownership and permissions
    try:
        shutil.chown(science_dir, group=science_group)
        os.chmod(science_dir, 0o770)
        logger.info(f"Successfully set ownership and permissions for {science_dir}")
    except OSError as e:
        logger.error(f"Failed to set ownership/permissions for {science_dir}: {e}")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)