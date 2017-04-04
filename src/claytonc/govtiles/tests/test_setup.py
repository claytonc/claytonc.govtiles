# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from claytonc.govtiles.testing import CLAYTONC_GOVTILES_INTEGRATION_TESTING  # noqa
from plone import api


class TestSetup(unittest.TestCase):
    """Test that claytonc.govtiles is properly installed."""

    layer = CLAYTONC_GOVTILES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if claytonc.govtiles is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'claytonc.govtiles'))

    def test_browserlayer(self):
        """Test that IClaytoncGovtilesLayer is registered."""
        from claytonc.govtiles.interfaces import (
            IClaytoncGovtilesLayer)
        from plone.browserlayer import utils
        self.assertIn(IClaytoncGovtilesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CLAYTONC_GOVTILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['claytonc.govtiles'])

    def test_product_uninstalled(self):
        """Test if claytonc.govtiles is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'claytonc.govtiles'))

    def test_browserlayer_removed(self):
        """Test that IClaytoncGovtilesLayer is removed."""
        from claytonc.govtiles.interfaces import IClaytoncGovtilesLayer
        from plone.browserlayer import utils
        self.assertNotIn(IClaytoncGovtilesLayer, utils.registered_layers())
