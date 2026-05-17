#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: guowendong
@Desc: file operations: Excel, JSON, YAML read/write, based on DATA_DIR
"""
import json
from pathlib import Path

import pandas as pd
import yaml

from common.log_utils import log
from config.global_config import DATA_DIR


class FileUtil:

    @staticmethod
    def _get_full_path(file_name: str) -> Path:
        """Convert the relative path to an absolute path within the data directory"""
        return DATA_DIR / file_name

    # ======================================= Excel operations ===========================================
    @staticmethod
    def read_excel(file_name, sheet_name=0):
        file_path = FileUtil._get_full_path(file_name)
        if not file_path.exists():
            log.error(f"❌ EXCEL Read failure: File does not exist {file_path}")
            raise FileNotFoundError(f"Excel file does not exist: {file_path}")
        try:
            if file_name.endswith(".xls"):
                engine = "xlrd"
            else:
                engine = "openpyxl"
            data_file = pd.read_excel(file_path, sheet_name=sheet_name, engine=engine)  # noqa
            data_file = data_file.fillna("")
            log.info(f"✅ EXCEL read successfully: {file_path}")
            return data_file.to_dict("records")
        except Exception as e:
            log.error(f"❌ EXCEL Read failure: {file_path}, error: {str(e)}")
            raise

    @staticmethod
    def write_excel(file_name, data):
        file_path = FileUtil._get_full_path(file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not data:
            log.warning(f"⚠️ EXCEL write warning: Data is empty, file: {file_path}")
        try:
            data_file = pd.DataFrame(data).fillna("")
            data_file.to_excel(file_path, index=False, engine="openpyxl")
            log.info(f"✅ EXCEL write successfully: {file_path}")
        except Exception as e:
            log.error(f"❌ EXCEL write failure: {file_path}, error: {str(e)}")
            raise

    # ======================================== JSON operations =============================================
    @staticmethod
    def read_json(file_name, encoding="utf-8"):
        file_path = FileUtil._get_full_path(file_name)
        if not file_path.exists():
            log.error(f"❌ JSON read failure: File does not exist {file_path}")
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        try:
            with open(file_path, "r", encoding=encoding) as f:
                data = json.load(f)
            log.info(f"✅ JSON read successfully: {file_path}")
            return data
        except Exception as e:
            log.error(f"❌ JSON read failure: {file_path}, error: {e}")
            raise

    @staticmethod
    def write_json(file_name, data, encoding="utf-8"):
        file_path = FileUtil._get_full_path(file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            log.info(f"✅ JSON write successfully: {file_path}")
        except Exception as e:
            log.error(f"❌ JSON write failure: {file_path}, error: {e}")
            raise

    # ======================================== YAML operations ================================================
    @staticmethod
    def read_yaml(file_name, encoding="utf-8"):
        file_path = FileUtil._get_full_path(file_name)
        if not file_path.exists():
            log.error(f"❌ YAML read failure: File does not exist {file_path}")
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        try:
            with open(file_path, "r", encoding=encoding) as f:
                data = yaml.safe_load(f) or {}
            log.info(f"✅ YAML read successfully: {file_path}")
            return data
        except Exception as e:
            log.error(f"❌ YAML read failure: {file_path}, error: {e}")
            raise

    @staticmethod
    def write_yaml(file_name, data, encoding="utf-8"):
        file_path = FileUtil._get_full_path(file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding=encoding) as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            log.info(f"✅ YAML write successfully: {file_path}")
        except Exception as e:
            log.error(f"❌ YAML write failure: {file_path}, error: {e}")
            raise
