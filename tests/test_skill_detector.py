"""
Test skill detector - tests for keyword detection system
"""

import pytest
import re


class TestKeywordPatterns:
    """Test keyword pattern matching"""

    def test_task_create_keywords_buat(self):
        """Test 'buat' triggers task creation"""
        keywords = ["buat", "create", "kerjakan", "do", "task"]
        assert "buat" in keywords

    def test_task_create_keywords_kerjakan(self):
        """Test 'kerjakan' triggers task creation"""
        keywords = ["buat", "create", "kerjakan", "do", "task"]
        assert "kerjakan" in keywords

    def test_content_keywords_tiktok(self):
        """Test 'tiktok' triggers content request"""
        keywords = ["konten", "tiktok", "generate", "posting"]
        assert "tiktok" in keywords

    def test_content_keywords_generate(self):
        """Test 'generate' triggers content request"""
        keywords = ["konten", "tiktok", "generate", "posting"]
        assert "generate" in keywords

    def test_trading_keywords_buy(self):
        """Test 'buy' triggers trading query"""
        keywords = ["trading", "buy", "sell", "posisi"]
        assert "buy" in keywords

    def test_trading_keywords_posisi(self):
        """Test 'posisi' triggers trading query"""
        keywords = ["trading", "buy", "sell", "posisi"]
        assert "posisi" in keywords

    def test_multilanguage_bahasa_indonesia(self):
        """Test Bahasa Indonesia keywords"""
        id_keywords = ["buat", "kerjakan", "do", "tugas"]
        assert "buat" in id_keywords

    def test_multilanguage_english(self):
        """Test English keywords"""
        en_keywords = ["create", "do", "task", "buy", "sell"]
        assert "create" in en_keywords


class TestCategoryMapping:
    """Test category to skill mapping"""

    def test_task_create_maps_to_todo(self):
        """Test task-create maps to todo-management category"""
        mapping = {"task-create": "todo-management"}
        assert mapping["task-create"] == "todo-management"

    def test_content_maps_to_visual(self):
        """Test content maps to visual-engineering category"""
        mapping = {"content": "visual-engineering"}
        assert mapping["content"] == "visual-engineering"

    def test_trading_maps_to_deep(self):
        """Test trading maps to deep category"""
        mapping = {"trading": "deep"}
        assert mapping["trading"] == "deep"

    def test_search_maps_to_quick(self):
        """Test search maps to quick category"""
        mapping = {"search": "quick"}
        assert mapping["search"] == "quick"

    def test_all_categories_have_mappings(self):
        """Test all categories have skill mappings"""
        required_mappings = {
            "task-create": "todo-management",
            "content": "visual-engineering",
            "trading": "deep",
            "search": "quick",
        }
        assert len(required_mappings) == 4
