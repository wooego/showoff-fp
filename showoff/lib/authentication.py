#coding:utf-8
import os, bcrypt

def hash_password(seed, plaintext):
    """Encrypt given password using seed as an extra salt"""
    return bcrypt.hashpw(('%s%s' % (seed, plaintext)).encode('utf-8'), bcrypt.gensalt())


def validate_password(seed, plaintext, hashed):
    """Validation function for blowfish encrypted password"""
    return bcrypt.hashpw(('%s%s' % (seed, plaintext)).encode('utf-8'), hashed.encode('utf-8')).decode('utf-8') == hashed
