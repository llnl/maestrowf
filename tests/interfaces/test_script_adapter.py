###############################################################################
# Copyright (c) 2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by Francesco Di Natale, dinatale3@llnl.gov.
#
# LLNL-CODE-734340
# All rights reserved.
# This file is part of MaestroWF, Version: 1.0.0.
#
# For details, see https://github.com/LLNL/maestrowf.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################
"""
This module is intended to test maestrowf.interfacesmodule. It is setup to
use nose or pytest to do that testing.

This was created to verify existing functionality of the ScriptAdapterFactory
as it was converted to dynamically load all ScriptAdapters using a namespace
plugin methodology.
"""
import inspect
import warnings

import pytest

from maestrowf.abstracts.interfaces.flux import FluxInterface
from maestrowf.interfaces import ScriptAdapterFactory, iter_adapters
from maestrowf.interfaces.script import FluxFactory


def test_factory():
    """
    Test to verify that the ScriptAdapterFactory loads correctly
    """
    saf = ScriptAdapterFactory
    assert(saf.factories is not None)


def test_get_valid_adapters():
    """
    Test to verify that the keys in the internal factory is the same set as
    the results from get_valid_adapters()
    """
    saf = ScriptAdapterFactory
    assert(saf.factories.keys() == ScriptAdapterFactory.get_valid_adapters())


def test_adapter_none_found():
    """
    Test to verify that an Exception is raised when an non-existing adapter
    is requested from the factory
    """
    with pytest.raises(Exception):
        ScriptAdapterFactory.get_adapter('empty-adapter')


def test_iter_adapters_finds_builtin_adapters():
    """
    Test to verify that discovery finds every adapter shipped in
    maestrowf.interfaces.script, keyed the way specifications name them.
    """
    keys = set(adapter.key for adapter in iter_adapters())
    assert {'local', 'slurm', 'lsf', 'flux'} <= keys


def test_iter_adapters_returns_the_registered_classes():
    """
    Test to verify that discovery hands back the very classes the factory
    registered at import, rather than re-executing the adapter modules.
    (Discovery through Loader.load_module() re-ran each module on every
    call, so a second call produced a fresh set of classes.)
    """
    for adapter in iter_adapters():
        assert ScriptAdapterFactory.get_adapter(adapter.key) is adapter


def test_iter_adapters_avoids_deprecated_import_machinery():
    """
    Test to verify that discovery raises no DeprecationWarning: it must not
    rely on pkgutil.get_loader (removed in Python 3.14) or on
    Loader.load_module (slated for removal in Python 3.15).
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert iter_adapters()


def test_flux_factory_finds_builtin_interfaces():
    """
    Test to verify that FluxFactory discovers the concrete versioned
    interfaces in maestrowf.interfaces.script._flux, the one it calls
    latest among them, and registers each under its own key.
    """
    discovered = FluxFactory._iter_flux()
    assert discovered
    assert FluxFactory.latest in FluxFactory.get_valid_interfaces()
    for interface in discovered:
        assert issubclass(interface, FluxInterface)
        assert not inspect.isabstract(interface)
        assert FluxFactory.get_interface(interface.key) is interface


def test_flux_factory_avoids_deprecated_import_machinery():
    """
    Test to verify that the Flux interface discovery raises no
    DeprecationWarning either (same import machinery as iter_adapters).
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert FluxFactory._iter_flux()
