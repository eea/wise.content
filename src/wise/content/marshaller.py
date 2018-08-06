# -*- coding: utf-8 -*-
from eea.rdfmarshaller.value import Value2Surf
from plone.namedfile.interfaces import INamedBlobFile, INamedBlobImage
from wise.content.contenttypes import IRichImage
from zope.component import adapts


class File2Surf(Value2Surf):
    """IValue2Surf implementation for plone.namedfile.file.NamedBlobFile """

    adapts(INamedBlobFile)

    def __init__(self, value):
        self.value = value.filename


class Image2Surf(Value2Surf):
    """IValue2Surf implementation for plone.namedfile.file.NamedBlobImage """

    adapts(INamedBlobImage)

    def __init__(self, value):
        self.value = value.filename


class RichImage2Surf(Value2Surf):
    """IValue2Surf implementation for wise.content.contenttypes.IRichImage """

    adapts(IRichImage)

    def __init__(self, value):
        self.value = value.filename
